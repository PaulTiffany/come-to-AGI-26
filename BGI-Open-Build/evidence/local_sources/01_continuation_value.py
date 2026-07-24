"""Executable evidence for the canonical Bellman continuation value."""

from compitum.regret_lab.belief_bellman import BellmanOracle
from compitum.regret_lab.belief_regime import GRID_UNIT

remaining_steps = 5
budget = 8.0
belief = 0.5
oracle = BellmanOracle()

continuation_value = oracle.value(remaining_steps, budget, belief)
lower_value = oracle.value(remaining_steps, budget - GRID_UNIT, belief)
marginal_price = oracle.marginal_price(remaining_steps, budget, belief)
expected_price = (continuation_value - lower_value) / GRID_UNIT

assert continuation_value >= lower_value
assert abs(marginal_price - expected_price) <= 1e-12

print(f"continuation_value={continuation_value:.6f}")
print(f"lower_value={lower_value:.6f}")
print(f"marginal_price={marginal_price:.6f}")
print("PASS")
