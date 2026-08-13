import numpy as np
from src.match_engine import MatchEngine

class ProbabilityEngine:
    def __init__(self, avg_score=165):
        self.avg_score = avg_score

    def _sigmoid(self, x):
        exponential = np.exp(-x)
        return 1 / (1+exponential)
    
    def compute(self, state):
        wickets = state["wickets_in_hand"]
        crr = state["current_run_rate"]
        rrr = state["required_run_rate"]
        balls_remaining = state["balls_remaining"]
        runs_required = state["runs_required"]

        run_rate_advantage = (crr - rrr) * 0.2
        wicket_advantage = wickets * 0.05
        advantage_score = run_rate_advantage + wicket_advantage

        if balls_remaining > 0:
            pressure_penalty = (runs_required / balls_remaining) * 0.3
        else:
            pressure_penalty = 0
        advantage_score = advantage_score - pressure_penalty

        probability = self._sigmoid(advantage_score)

        return {
                "advantage_score": advantage_score,
                "win_probability": probability
            }