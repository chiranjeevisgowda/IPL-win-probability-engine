from src.data_loader import DataLoader
from src.match_engine import MatchEngine
from src.probability import ProbabilityEngine
from src.visualiser import Visualiser

from tabulate import tabulate


# -----------------------------
# Load Data
# -----------------------------

loader = DataLoader(
    "data/deliveries.csv",
    "data/matches.csv"
)

loader.load()
loader.load_matches()


# -----------------------------
# Select Match
# -----------------------------

match_ids = loader.get_match_ids()

for i, match_id in enumerate(match_ids[:20]):
    print(i, match_id)

choice = int(input("Select match number: "))

match_id = match_ids[choice]

match_data = loader.get_match_data(match_id)

innings = loader.get_innings(
    match_data,
    2
)

chasing_team = innings[0]["batting_team"]

# -----------------------------
# Match Information
# -----------------------------

match_info = loader.get_match_info(match_id)

target = match_info["target_runs"]


print("\nMATCH INFO")
print("-" * 50)

print(f"Teams         : {match_info['team1']} vs {match_info['team2']}")
print(f"Chasing Team  : {chasing_team}")
print(f"Target        : {target}")
print(f"Winner        : {match_info['winner']}")


# -----------------------------
# Generate Match States
# -----------------------------

engine = MatchEngine(innings)

states = engine.compute_state(
    target=target
)


# -----------------------------
# Generate Probabilities
# -----------------------------

probability_engine = ProbabilityEngine()

probabilities = []

for state in states:

    result = probability_engine.compute(state)

    probabilities.append(
        result["win_probability"]
    )


# -----------------------------
# Generate Over Summary
# -----------------------------

over_summary = engine.over_summary(states)


# -----------------------------
# Add Probability To Each Over
# -----------------------------

for over in over_summary:

    probability_index = min(
        ((over["over"] + 1) * 6) - 1,
        len(probabilities) - 1
    )

    over["win_probability"] = round(
        probabilities[probability_index] * 100,
        1
    )


# -----------------------------
# Display Match Summary Table
# -----------------------------

table = []

for over in over_summary:

    table.append([
        over["over"] + 1,
        over["runs"],
        over["total_runs"],
        over["wickets"],
        over["current_run_rate"],
        over["required_run_rate"],
        f"{over['win_probability']}%"
    ])


print("\nMATCH SUMMARY")
print("-" * 80)

print(
    tabulate(
        table,
        headers=[
            "Over",
            "Runs",
            "Total Runs",
            "Wickets",
            "CRR",
            "RRR",
            "Win Probability"
        ],
        tablefmt="grid"
    )
)


# -----------------------------
# Visualisation
# -----------------------------

visualiser = Visualiser()

visualiser.plot_win_probability(
    probabilities,
    f"{match_info['team1']} vs {match_info['team2']}"
)