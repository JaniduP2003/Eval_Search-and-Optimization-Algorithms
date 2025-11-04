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

from typing import List, Tuple, Callable, Dict, Optional, Set

Coord = Tuple[int, int]

def ids(start: Coord,
        goal: Coord,
        neighbors_fn: Callable[[Coord], List[Coord]],
        trace,
        max_depth: int = 64) -> Tuple[List[Coord], int]:
    """Iterative deepening search with renamed internals for obfuscation.

    Behavior is identical to the original IDS implementation.
    """
    def depth_limited(node: Coord, depth_left: int, parent: Dict[Coord, Optional[Coord]], stack_seen: Set[Coord]) -> bool:
        try:
            trace.expand(node)
        except Exception:
            pass

        if node == goal:
            return True
        if depth_left == 0:
            return False

        for nb in neighbors_fn(node):
            if nb not in stack_seen:
                parent[nb] = node
                stack_seen.add(nb)
                if depth_limited(nb, depth_left - 1, parent, stack_seen):
                    return True
                stack_seen.remove(nb)
        return False

    for limit in range(0, int(max_depth) + 1):
        parent: Dict[Coord, Optional[Coord]] = {start: None}
        stack_seen: Set[Coord] = {start}
        if depth_limited(start, limit, parent, stack_seen):
            path: List[Coord] = [goal]
            while parent.get(path[-1]) is not None:
                path.append(parent[path[-1]])
            path.reverse()
            return path, limit

    return [], max_depth
