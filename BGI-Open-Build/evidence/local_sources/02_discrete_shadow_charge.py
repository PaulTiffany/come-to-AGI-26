"""Executable evidence for the exact discrete shadow-charge identity."""

from compitum.regret_lab.belief_action_pricing import (
    action_shadow_charge,
    unit_marginal_prices,
)
from compitum.regret_lab.belief_bellman import BellmanOracle
from compitum.regret_lab.belief_regime import GRID_UNIT

remaining_steps = 5
budget = 10.0
belief = 0.5
num_units = 8
oracle = BellmanOracle()

unit_prices = unit_marginal_prices(
    oracle,
    remaining_steps,
    budget,
    belief,
    num_units,
)
charge = action_shadow_charge(
    oracle,
    remaining_steps,
    budget,
    belief,
    num_units * GRID_UNIT,
)
telescoping_sum = sum(unit_prices)

assert len(unit_prices) == num_units
assert abs(telescoping_sum - charge) <= 1e-9

print(f"unit_prices={[round(value, 6) for value in unit_prices]}")
print(f"telescoping_sum={telescoping_sum:.6f}")
print(f"action_shadow_charge={charge:.6f}")
print("PASS")
