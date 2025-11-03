# heuristics.py
# ============================================================
# TASK
#   Implement three admissible (non-overestimating) heuristics.
#
# SIGNATURES (do not change):
#   heuristic_manhattan(u, goal)      -> float   (5%)
#   heuristic_straight_line(u, goal)  -> float   (5%)
#   heuristic_custom(u, goal)         -> float   (10%)
#
# PARAMETERS
#   u, goal: coordinates (r, c)
#
# RETURN
#   A non-negative number estimating the remaining cost from u to goal.
#
# RULES
# - Heuristics must be ADMISSIBLE for 4-neighbor grids with unit step cost,
#   i.e., h(u) <= true shortest path length from u to goal.
# - They must be finite (no NaN/inf) and >= 0.
# - We will probe many random states and compare h(u) against true distances.
#
# HINTS
# - Manhattan distance is admissible in 4-neighborhood: |dr| + |dc|.
# - Straight-line (Euclidean) distance is also admissible.
# - For the custom heuristic, keep it <= Manhattan to be safe,
#   OR design another admissible function and justify in your notes.
# ============================================================
# heuristics.py
# ============================================================
# Implemented admissible heuristics: Manhattan, Euclidean,
# and a custom admissible heuristic (convex mix of Manhattan
# and Euclidean; stays ≤ Manhattan).
# ============================================================

from typing import Tuple
from math import hypot

Coord = Tuple[int, int]

def heuristic_manhattan(u: Coord, goal: Coord) -> float:
    """Return |ur - gr| + |uc - gc| (admissible for 4-neighborhood)."""
    ur, uc = u
    gr, gc = goal
    return float(abs(ur - gr) + abs(uc - gc))

def heuristic_straight_line(u: Coord, goal: Coord) -> float:
    """Return Euclidean (straight-line) distance to goal (admissible)."""
    ur, uc = u
    gr, gc = goal
    return float(hypot(ur - gr, uc - gc))

def heuristic_custom(u: Coord, goal: Coord) -> float:
    """
    Custom admissible heuristic.

    Design:
      - Both Manhattan and Euclidean are admissible on a 4-neighbour grid.
      - Use a convex combination: alpha*Manhattan + (1-alpha)*Euclidean with 0 <= alpha <= 1.
      - Since Euclidean <= Manhattan, any convex combination will be <= Manhattan,
        so the result remains admissible. This can reduce plateaus compared to
        pure Manhattan while staying admissible.

    I pick alpha = 0.6 (60% Manhattan, 40% Euclidean).
    """
    man = heuristic_manhattan(u, goal)
    euc = heuristic_straight_line(u, goal)
    alpha = 0.6
    val = alpha * man + (1.0 - alpha) * euc
    # Safety: ensure non-negative finite number
    if val < 0:
        return 0.0
    return float(val)``
