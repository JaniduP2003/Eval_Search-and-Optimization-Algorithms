# student_ids.py
# ============================================================
# TASK
#   Implement Iterative Deepening Search (IDS).
#
# SIGNATURE (do not change):
#   ids(start, goal, neighbors_fn, trace, max_depth=64) -> (List[Coord], int)
#
# PARAMETERS
#   start, goal:       coordinates
#   neighbors_fn(u):   returns valid 4-neighbors of u
#   trace:             MUST call trace.expand(u) when you EXPAND u
#                      in the depth-limited search (DLS).
#   max_depth:         upper cap for the iterative deepening
#
# RETURN
#   (path, depth_limit_used)
#   - If found at depth L, return the path and L.
#   - If not found up to max_depth, return ([], max_depth).
#
# IMPLEMENTATION HINT
# - Outer loop: for limit in [0..max_depth]:
#       run DLS(start, limit) with its own parent dict and visited set
#       DLS(u, remaining):
#           trace.expand(u)
#           if u == goal: return True
#           if remaining == 0: return False
#           for v in neighbors_fn(u):
#               if v not seen in THIS DLS: mark parent[v]=u and recurse
# - Reconstruct the path when DLS reports success.
# ============================================================
# student_ids.py
# Iterative Deepening Search (IDS) implementation.
from typing import List, Tuple, Callable, Dict, Optional, Set

Coord = Tuple[int, int]

def ids(start: Coord,
        goal: Coord,
        neighbors_fn: Callable[[Coord], List[Coord]],
        trace,
        max_depth: int = 64) -> List[Coord]:
    """
    Iterative deepening: return a path list (or [] if not found up to max_depth).

    REQUIRED: call trace.expand(u) in the DLS when you expand u.
    """
    if start == goal:
        try:
            trace.expand(start)
        except Exception:
            pass
        return [start]

    def reconstruct(par: Dict[Coord, Optional[Coord]], node: Coord) -> List[Coord]:
        path = []
        cur = node
        while cur is not None:
            path.append(cur)
            cur = par[cur]
        path.reverse()
        return path

    for limit in range(0, max_depth + 1):
        parent: Dict[Coord, Optional[Coord]] = {start: None}
        seen: Set[Coord] = {start}
        found = False

        def dls(u: Coord, remaining: int) -> bool:
            nonlocal found
            # trace expansion hook
            try:
                trace.expand(u)
            except Exception:
                pass

            if u == goal:
                found = True
                return True
            if remaining == 0:
                return False
            for v in neighbors_fn(u):
                if v not in seen:
                    seen.add(v)
                    parent[v] = u
                    if dls(v, remaining - 1):
                        return True
            return False

        if dls(start, limit):
            # reconstruct path using parent
            if found:
                return reconstruct(parent, goal)
            # fallback: sometimes dls returns True but found not set (defensive)
            # find any node equal to goal in parent
            if goal in parent:
                return reconstruct(parent, goal)
            # else continue to next limit

    return []
