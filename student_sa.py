# student_sa.py
from __future__ import annotations
from typing import List, Tuple, Set, Optional, Callable
import math, random, collections

Coord = Tuple[int, int]


def _quick_bfs(src: Coord, dst: Coord, nbrs: Callable[[Coord], List[Coord]]) -> List[Coord]:
    if src == dst:
        return [src]
    dq = collections.deque([src])
    prev = {src: None}
    while dq:
        cur = dq.popleft()
        for n in nbrs(cur):
            if n not in prev:
                prev[n] = cur
                if n == dst:
                    path = [n]
                    while path[-1] is not None:
                        p = prev[path[-1]]
                        if p is None:
                            break
                        path.append(p)
                    path.reverse()
                    return path
                dq.append(n)
    return []


def _count_turns(p: List[Coord]) -> int:
    if len(p) < 3:
        return 0
    def d(a: Coord, b: Coord) -> Coord:
        return (b[0] - a[0], b[1] - a[1])
    cnt = 0
    for i in range(2, len(p)):
        if d(p[i-2], p[i-1]) != d(p[i-1], p[i]):
            cnt += 1
    return cnt


def _default_cost(path: List[Coord]) -> float:
    if not path:
        return float('inf')
    return float(len(path) + 0.2 * _count_turns(path))


def _splice_segment(base: List[Coord], i: int, j: int, mid: List[Coord]) -> List[Coord]:
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


def _biased_walk(a: Coord, b: Coord, nbrs: Callable[[Coord], List[Coord]], rng: random.Random, budget: int = 24) -> List[Coord]:
    def man(u: Coord, v: Coord) -> int:
        return abs(u[0] - v[0]) + abs(u[1] - v[1])
    cur = a
    path = [cur]
    seen = {cur}
    for _ in range(budget):
        nbs = nbrs(cur)
        if not nbs:
            break
        nbs.sort(key=lambda x: (man(x, b), rng.random()))
        pick = None
        for cand in nbs[:3]:
            if cand not in seen:
                pick = cand
                break
        if pick is None:
            pick = rng.choice(nbs)
        cur = pick
        path.append(cur)
        seen.add(cur)
        if cur == b:
            return path
    return []


def _mut_shortcut(path: List[Coord], nbrs: Callable[[Coord], List[Coord]], rng: random.Random) -> List[Coord]:
    n = len(path)
    if n < 6:
        return path[:]
    i = rng.randrange(1, n-3)
    j = rng.randrange(i+2, min(i+6, n-1))
    a, b = path[i], path[j]
    mid = _biased_walk(a, b, nbrs, rng, budget=18)
    if mid and len(mid) <= (j - i + 1):
        return _splice_segment(path, i, j, mid)
    return path[:]


def _mut_detour(path: List[Coord], nbrs: Callable[[Coord], List[Coord]], rng: random.Random) -> List[Coord]:
    n = len(path)
    if n < 6:
        return path[:]
    i = rng.randrange(1, n-3)
    j = rng.randrange(i+2, min(i+6, n-1))
    a, b = path[i], path[j]
    mid = _biased_walk(a, b, nbrs, rng, budget=30)
    if mid:
        return _splice_segment(path, i, j, mid)
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
    rng = random.Random(str(seed))

    # initial feasible path search similar to original intent
    starts = [(0,0), (0,1), (1,0)]
    goals = [(5,5), (5,4), (4,5)]
    initial: List[Coord] = []
    for s in starts:
        for g in goals:
            p = _quick_bfs(s, g, neighbors_fn)
            if p:
                initial = p
                break
        if initial:
            break
    if not initial:
        p = _quick_bfs((0,0), (5,5), neighbors_fn)
        if p:
            initial = p
    if not initial:
        return []

    def _safe_cost(path: List[Coord]) -> float:
        try:
            v = objective_fn(path)
            if v is None or not math.isfinite(v):
                return _default_cost(path)
            return float(v)
        except Exception:
            return _default_cost(path)

    current = initial[:]
    best = initial[:]
    cur_cost = _safe_cost(current)
    best_cost = cur_cost
    history: List[float] = [cur_cost]
    T = float(T0)

    no_improve = 0
    for k in range(1, int(iters)+1):
        # mutation choice: mostly shortcut, occasionally detour
        if (k % 5) == 0:
            candidate = _mut_detour(current, neighbors_fn, rng)
        else:
            candidate = _mut_shortcut(current, neighbors_fn, rng)

        cand_cost = _safe_cost(candidate)
        delta = cand_cost - cur_cost

        accepted = False
        if delta < 0:
            accepted = True
        else:
            prob = math.exp(-delta / max(T, 1e-12))
            if rng.random() < prob:
                accepted = True

        if accepted:
            current = candidate
            cur_cost = cand_cost

        if cur_cost < best_cost:
            best = current[:]
            best_cost = cur_cost
            no_improve = 0
        else:
            no_improve += 1

        history.append(cur_cost)

        # cool temperature
        T = alpha * T

        # small restart when stuck
        if no_improve > 250 and k < int(iters * 0.9):
            current = best[:]
            cur_cost = best_cost
            current = _mut_detour(current, neighbors_fn, rng)
            cur_cost = _safe_cost(current)
            no_improve = 0

    return best, history
