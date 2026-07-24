"""Executable evidence for shadow-charge and online-optimal equivalence."""

import numpy as np
from compitum.regret_lab.belief_action_pricing import run_shadow_charge_policy
from compitum.regret_lab.belief_bellman import BellmanOracle
from compitum.regret_lab.belief_online_optimum import run_online_optimal_policy
from compitum.regret_lab.belief_pricing import ExactBeliefEstimator
from compitum.regret_lab.belief_regime import INITIAL_BELIEF, generate_belief_sequence

seed = 42
rng = np.random.default_rng(seed)
sequence, _, _, _ = generate_belief_sequence(rng, "adapter-equivalence")
oracle = BellmanOracle()

shadow_result, _, _ = run_shadow_charge_policy(
    sequence,
    oracle,
    ExactBeliefEstimator(belief=INITIAL_BELIEF),
)
online_result, _ = run_online_optimal_policy(sequence, oracle, INITIAL_BELIEF)
mismatch_vector = np.array(
    [
        shadow != online
        for shadow, online in zip(shadow_result.choices, online_result.choices, strict=True)
    ],
    dtype=bool,
)
mismatches = int(np.count_nonzero(mismatch_vector))

assert shadow_result.choices == online_result.choices
assert abs(shadow_result.cumulative_utility - online_result.cumulative_utility) <= 1e-12
assert not np.any(mismatch_vector)
assert mismatches == 0

print(f"seed={seed}")
print(f"choices={shadow_result.choices}")
print(f"cumulative_utility={shadow_result.cumulative_utility:.6f}")
print(f"mismatches={mismatches}")
print("PASS")
