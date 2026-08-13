from src.data_loader import DataLoader
from src.match_engine import MatchEngine
from src.probability import ProbabilityEngine
from src.visualiser import Visualiser


loader = DataLoader("data/deliveries.csv")
loader.load()


match_ids = loader.get_match_ids()
match = loader.get_match_data(match_ids[0])
innings = loader.get_innings(match, 2)


engine = MatchEngine(innings)
states = engine.compute_state(target=141)


probability_engine = ProbabilityEngine()

probabilities = []

for state in states:
    result = probability_engine.compute(state)
    probabilities.append(result["win_probability"])


print(len(states))
print(len(probabilities))

print(probabilities[0])
print(probabilities[-1])


visualiser = Visualiser()

visualiser.plot_win_probability(
    probabilities,
    "Chasing Team"
)