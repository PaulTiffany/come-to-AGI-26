"""Executable evidence for a genuine belief-sensitive action boundary."""

from compitum.regret_lab.belief_bellman_v2 import BeliefSensitiveBellmanOracle

u_normal = 1.0
u_high = 8.0
initial_budget = 6.0
p_opportunity_normal = 0.15
p_opportunity_high = 0.25
transition_normal_to_high = 0.2
transition_high_to_high = 0.6

oracle = BeliefSensitiveBellmanOracle(
    u_normal_opportunity=u_normal,
    u_high_opportunity=u_high,
    p_opportunity_normal=p_opportunity_normal,
    p_opportunity_high=p_opportunity_high,
    transition_normal_to_high=transition_normal_to_high,
    transition_high_to_high=transition_high_to_high,
)

remaining_steps = 1
reachable_budget = 4.5
observed_opportunity = True
low_belief = 0.05
high_belief = 0.2
low_action, low_value = oracle.best_action_given_observation(
    remaining_steps,
    reachable_budget,
    low_belief,
    observed_opportunity,
)
high_action, high_value = oracle.best_action_given_observation(
    remaining_steps,
    reachable_budget,
    high_belief,
    observed_opportunity,
)

assert initial_budget == 6.0
assert low_action != high_action
assert low_action == "spend"
assert high_action == "opportunity"

print(f"reachable_budget={reachable_budget:.1f}")
print(f"low_belief={low_belief:.2f} action={low_action} value={low_value:.6f}")
print(f"high_belief={high_belief:.2f} action={high_action} value={high_value:.6f}")
print("PASS")
