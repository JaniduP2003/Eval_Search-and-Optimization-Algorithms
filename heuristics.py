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

from typing import Tuple
from math import hypot

Coord = Tuple[int, int]


def heuristic_manhattan(u: Coord, goal: Coord) -> float:
    ur, uc = u
    gr, gc = goal
    return float(abs(ur - gr) + abs(uc - gc))


def heuristic_straight_line(u: Coord, goal: Coord) -> float:
    ur, uc = u
    gr, gc = goal
    return float(hypot(ur - gr, uc - gc))


def heuristic_custom(u: Coord, goal: Coord) -> float:
    """Conservative mix of Manhattan + Euclidean that stays <= Manhattan.

    We blend metrics with weights that sum to 1 and give more weight to
    Manhattan distance so the result never exceeds the Manhattan value.
    """
    m = heuristic_manhattan(u, goal)
    e = heuristic_straight_line(u, goal)
    # weights chosen so 0.6*m + 0.4*e <= m because e <= m
    return 0.6 * m + 0.4 * e
