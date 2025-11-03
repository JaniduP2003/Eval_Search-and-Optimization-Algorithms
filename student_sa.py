## student_sa.py
# Completed key SA pieces: mutation policy, acceptance, cooling schedule.
from __future__ import annotations
from typing import List, Tuple, Set, Optional, Callable
import math, random, collections

Coord = Tuple[int, int]

# (utilities and mutation operators kept as in template)
def _bfs_path(start: Coord, goal: Coord, neighbors_fn: Callable[[Coord], List[Coord]]) -> List[Coord]:
    """Feasible S→G path on unweighted grid."""
    if start == goal:
        return [start]
    q = collections.deque([start])
    parent = {start: None}
    while q:
        u = q.popleft()
        for v in neighbors_fn(u):
            if v not in parent:
                parent[v] = u
                if v == goal:
                    path = [v]
                    while path[-1] is not None:
                        p = parent[path[-1]]
                        if p is None: break
                        path.append(p)
                    path.reverse()
                    return path
                q.append(v)
    return []  # no path found

def _turns_in_path(path: List[Coord]) -> int:
    if len(path) < 3:
        return 0
    def step(a: Coord, b: Coord) -> Coord:
        return (b[0]-a[0], b[1]-a[1])
    t = 0
    for i in range(2, len(path)):
        if step(path[i-2], path[i-1]) != step(path[i-1], path[i]):
            t += 1
    return t

def _cost_default(path: List[Coord]) -> float:
    if not path:
        return float("inf")
    return float(len(path) + 0.2 * _turns_in_path(path))

def _splice(base: List[Coord], i: int, j: int, mid: List[Coord]) -> List[Coord]:
    """Return base[:i+1] + mid[1:-1] + base[j:] (keeps endpoints base[i], base[j])."""
    if not base or i < 0 or j >= len(base) or i >= j:
        return base[:]
    out = base[:i+1]
    core = mid[:]
    if core and core[0] == base[i]:
        core = core[1:]
    if core and core[-1] == base[j]:
        core = core[:-1]
    out.extend(core)
    out.extend(base[j:])
    return out

def _random_walk_connect(a: Coord, b: Coord, neighbors_fn: Callable[[Coord], List[Coord]],
                         rng: random.Random, budget: int = 24) -> List[Coord]:
    """Biased random walk that tends to move closer to b; returns a..b path or [] if failed."""
    def manhattan(u: Coord, v: Coord) -> int:
        return abs(u[0]-v[0]) + abs(u[1]-v[1])
    cur = a
    path = [cur]
    seen = {cur}
    for _ in range(budget):
        nbrs = neighbors_fn(cur)
        if not nbrs:
            break
        nbrs.sort(key=lambda x: (manhattan(x, b), rng.random()))
        chosen = None
        for cand in nbrs[:3]:
            if cand not in seen:
                chosen = cand
                break
        if chosen is None:
            chosen = rng.choice(nbrs)
        cur = chosen
        path.append(cur)
        seen.add(cur)
        if cur == b:
            return path
    return []

def _mutate_shortcut(path: List[Coord],
                     neighbors_fn: Callable[[Coord], List[Coord]],
                     rng: random.Random) -> List[Coord]:
    """Try to replace a short segment i..j by a shorter connector (exploit)."""
    n = len(path)
    if n < 6:
        return path[:]
    i = rng.randrange(1, n-3)
    j = rng.randrange(i+2, min(i+6, n-1))
    a, b = path[i], path[j]
    mid = _random_walk_connect(a, b, neighbors_fn, rng, budget=18)
    if mid and len(mid) < (j - i + 1):
        return _splice(path, i, j, mid)
    return path[:]

def _mutate_detour(path: List[Coord],
                   neighbors_fn: Callable[[Coord], List[Coord]],
                   rng: random.Random) -> List[Coord]:
    """Try a small detour i..j via an alternative connector (explore)."""
    n = len(path)
    if n < 6:
        return path[:]
    i = rng.randrange(1, n-3)
    j = rng.randrange(i+2, min(i+6, n-1))
    a, b = path[i], path[j]
    mid = _random_walk_connect(a, b, neighbors_fn, rng, budget=30)
    if mid:
        return _splice(path, i, j, mid)
    return path[:]

def simulated_annealing(
    neighbors_fn: Callable[[Coord], List[Coord]],
    objective_fn: Callable[[List[Coord]], float],
    obstacles: Set[Coord],
    seed: str,
    iters: int = 1200,
    T0: float = 1.3,
    alpha: float = 0.995
):
    """
    Return (best_path, history). History logs best-so-far cost after each iteration.
    """
    rng = random.Random(str(seed))

    # 1) Initial feasible path (BFS from typical corners; do not assume constants exist)
    common_starts = [(0,0), (0,1), (1,0)]
    common_goals  = [(5,5), (5,4), (4,5)]
    path0: List[Coord] = []
    for s in common_starts:
        for g in common_goals:
            p = _bfs_path(s, g, neighbors_fn)
            if p:
                path0 = p
                break
        if path0:
            break
    if not path0:  # fallback guess for 6x6
        p = _bfs_path((0,0), (5,5), neighbors_fn)
        if p:
            path0 = p
    if not path0:
        return []  # no feasible start

    # Objective wrapper
    def safe_cost(pth: List[Coord]) -> float:
        try:
            val = objective_fn(pth)
            if val is None or not math.isfinite(val):
                return _cost_default(pth)
            return float(val)
        except Exception:
            return _cost_default(pth)

    current = path0[:]
    best    = path0[:]
    cur_cost  = safe_cost(current)
    best_cost = cur_cost
    history: List[float] = [best_cost]
    T = float(T0)

    no_improve = 0
    for k in range(1, int(iters)+1):

        # --- (1) Mutation policy: choose exploit vs explore -----------------
        # mostly try shortcuts, occasionally detours for exploration
        if rng.random() < 0.75:
            cand = _mutate_shortcut(current, neighbors_fn, rng)
        else:
            cand = _mutate_detour(current, neighbors_fn, rng)

        cand_cost = safe_cost(cand)
        delta = cand_cost - cur_cost

        # --- (2) Acceptance probability for uphill moves --------------------
        accept = False
        if delta < 0:
            accept = True
        else:
            # classic Metropolis acceptance using temperature T
            try:
                prob = math.exp(-delta / T) if T > 0 else 0.0
            except OverflowError:
                prob = 0.0
            if rng.random() < prob:
                accept = True

        if accept:
            current = cand
            cur_cost = cand_cost

        # Track global best & stagnation
        if cur_cost < best_cost:
            best = current[:]
            best_cost = cur_cost
            no_improve = 0
        else:
            no_improve += 1

        history.append(best_cost)

        # --- (3) Cooling schedule ------------------------------------------
        T = T * alpha

        # --- (4) Optional: simple restart if stuck --------------------------
        if no_improve > 250 and k < int(iters * 0.9):
            current = best[:]
            cur_cost = best_cost
            # small shake using an exploratory mutation
            current = _mutate_detour(current, neighbors_fn, rng)
            cur_cost = safe_cost(current)
            no_improve = 0

    return best, history 
