import numpy as np


class ProbabilityEngine:

    def __init__(self, avg_score=165):
        self.avg_score = avg_score

    def _sigmoid(self, x):
        """Numerically stable Sigmoid activation with domain clipping."""
        x_clipped = np.clip(x, -12.0, 12.0)
        return 1.0 / (1.0 + np.exp(-x_clipped))

    def compute(self, state):
        wickets = float(state["wickets_in_hand"])
        crr = float(state["current_run_rate"])
        rrr = float(state["required_run_rate"])
        balls_remaining = int(state["balls_remaining"])
        runs_required = int(state["runs_required"])

        # 1. Deterministic Terminal States
        if runs_required <= 0:
            return {"advantage_score": 10.0, "win_probability": 1.0}

        if wickets <= 0 or balls_remaining <= 0:
            return {"advantage_score": -10.0, "win_probability": 0.0}

        # 2. Run Rate Delta Component
        run_rate_advantage = (crr - rrr) * 0.28

        # 3. Wicket Capital (Anchored at 5 wickets par)
        wicket_advantage = (wickets - 5.0) * 0.32

        # 4. Non-linear Death Over Pressure Strain (RRR > 8.5)
        overs_elapsed = (120.0 - balls_remaining) / 6.0
        time_weight = 1.0 + (overs_elapsed / 10.0)
        rrr_strain = max(0.0, rrr - 8.5) * 0.18 * time_weight

        # 5. Composite Advantage Score & Win Probability
        advantage_score = run_rate_advantage + wicket_advantage - rrr_strain
        probability = float(self._sigmoid(advantage_score))

        return {
            "advantage_score": round(advantage_score, 4),
            "win_probability": round(probability, 4),
        }