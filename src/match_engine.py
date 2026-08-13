class MatchEngine:
    def __init__(self, innings_data):
        self.innings_data = innings_data

    def runs_per_over(self):
        runs_per_over = {}
        for row in self.innings_data:
            over = row["over"]
            runs = row["total_runs"]
            if over in runs_per_over:
                runs_per_over[over] += runs
            else:
                runs_per_over[over] = runs

        return runs_per_over

    def wickets_per_over(self):
        wickets_per_over = {}
        for row in self.innings_data:
            over = row["over"]
            is_wicket = row["is_wicket"]
            if over in wickets_per_over:
                wickets_per_over[over] += is_wicket
            else:
                wickets_per_over[over] = is_wicket

        return wickets_per_over
    def compute_state(self, target=None):
        states = []
        runs = 0
        wickets = 0
        legal_balls = 0

        for row in self.innings_data:
            runs += row["total_runs"]
            wickets += row["is_wicket"]

            if row["extras_type"] not in ("wides", "no_balls"):
                legal_balls = legal_balls+1

            if target is not None:
                runs_required = target - runs
            else:
                runs_required = None

            balls_remaining = 120 - legal_balls
            wickets_in_hand = 10 - wickets

            if legal_balls > 0:
                current_run_rate = runs / (legal_balls/6)
            else:
                current_run_rate = 0

            if target is not None and balls_remaining > 0:
                required_run_rate = (runs_required/balls_remaining) * 6
            else:
                required_run_rate = None
            state = {
                "runs" : runs,
                "wickets" : wickets,
                "legal_balls" : legal_balls,
                "runs_required" : runs_required,
                "balls_remaining" : balls_remaining,
                "wickets_in_hand" : wickets_in_hand,
                "current_run_rate" : current_run_rate,
                "required_run_rate" : required_run_rate
            }

            states.append(state)
        
        return states