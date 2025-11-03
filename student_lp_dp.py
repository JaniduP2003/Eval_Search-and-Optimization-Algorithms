# student_lp_dp.py
from __future__ import annotations
from typing import List, Tuple, Optional
from functools import lru_cache
import math

"""
LP and DP implementations.
"""

Constraint = Tuple[float, float, float]  # a1, a2, b  meaning  a1*x + a2*y <= b
EPS = 1e-9

def _intersect(c1: Constraint, c2: Constraint) -> Optional[Tuple[float, float]]:
    a1, a2, b = c1
    c1_, c2_, d = c2
    det = a1 * c2_ - a2 * c1_
    if abs(det) < 1e-12:
        return None
    x = (b * c2_ - a2 * d) / det
    y = (a1 * d - b * c1_) / det
    return (float(x), float(y))

def _is_feasible(pt: Tuple[float, float], constraints: List[Constraint]) -> bool:
    x, y = pt
    for (a1, a2, b) in constraints:
        lhs = a1 * x + a2 * y
        if lhs > b + EPS:
            return False
    return True

def feasible_vertices(constraints: List[Constraint]) -> List[Tuple[float, float]]:
    # Copy constraints and add non-negativity as <= constraints: -x <= 0, -y <= 0
    cons = list(constraints)
    cons.append((-1.0, 0.0, 0.0))  # -x <= 0  <=> x >= 0
    cons.append((0.0, -1.0, 0.0))  # -y <= 0  <=> y >= 0

    candidates: List[Tuple[float, float]] = []
    n = len(cons)
    # pairwise intersections
    for i in range(n):
        for j in range(i + 1, n):
            pt = _intersect(cons[i], cons[j])
            if pt is not None:
                candidates.append(pt)
    # include origin explicitly
    candidates.append((0.0, 0.0))
    # filter feasible and deduplicate
    feasible = []
    seen = set()
    for (x, y) in candidates:
        if not (math.isfinite(x) and math.isfinite(y)):
            continue
        if not _is_feasible((x, y), cons):
            continue
        key = (round(x, 10), round(y, 10))
        if key in seen:
            continue
        seen.add(key)
        feasible.append((round(x, 10), round(y, 10)))
    return feasible

def maximize_objective(vertices: List[Tuple[float, float]], c1: float, c2: float) -> Tuple[Tuple[float, float], float]:
    if not vertices:
        return (0.0, 0.0), 0.0
    best_pt = vertices[0]
    best_val = c1 * best_pt[0] + c2 * best_pt[1]
    for (x, y) in vertices[1:]:
        val = c1 * x + c2 * y
        if val > best_val + EPS:
            best_val = val
            best_pt = (x, y)
        elif abs(val - best_val) <= EPS:
            # deterministic tie-break: prefer larger x, then larger y
            if x > best_pt[0] + EPS or (abs(x - best_pt[0]) <= EPS and y > best_pt[1] + EPS):
                best_pt = (x, y)
                best_val = val
    return (float(best_pt[0]), float(best_pt[1])), float(best_val)

def knapsack_bottom_up(values: List[int], weights: List[int], capacity: int) -> int:
    if capacity < 0 or len(values) != len(weights):
        return 0
    n = len(values)
    # dp[i][cap] = best value using items i..n-1 with capacity 'cap'
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for cap in range(0, capacity + 1):
            best = dp[i + 1][cap]
            if weights[i] <= cap:
                best = max(best, values[i] + dp[i + 1][cap - weights[i]])
            dp[i][cap] = best
    return int(dp[0][capacity])

def knapsack_top_down(values: List[int], weights: List[int], capacity: int) -> int:
    n = len(values)
    if n != len(weights) or capacity < 0:
        return 0

    @lru_cache(maxsize=None)
    def f(i: int, cap: int) -> int:
        if i >= n or cap <= 0:
            return 0
        # skip
        res = f(i + 1, cap)
        # take if fits
        if weights[i] <= cap:
            res = max(res, values[i] + f(i + 1, cap - weights[i]))
        return res

    return int(f(0, capacity))

# Minimal local smoke tests are left intact in runner; don't run anything here on import.
