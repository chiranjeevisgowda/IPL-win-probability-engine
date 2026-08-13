import matplotlib.pyplot as plt


class Visualiser:

    def plot_win_probability(self, probabilities, team_name):
        """
        Plots win probability after every delivery.
        """

        balls = range(1, len(probabilities) + 1)

        # Convert probability to percentage
        probability_percentage = [
            prob * 100 for prob in probabilities
        ]

        plt.figure(figsize=(10, 5))

        plt.plot(
            balls,
            probability_percentage
        )

        plt.xlabel("Ball Number")
        plt.ylabel("Win Probability (%)")

        plt.title(
            f"{team_name} Win Probability"
        )

        plt.ylim(0, 100)

        plt.grid(True)

        plt.show()


    def plot_run_rate_heatmap(self, rpo):
        """
        Placeholder for future run rate visualization.
        """

        plt.figure(figsize=(8, 4))

        plt.bar(
            rpo.keys(),
            rpo.values()
        )

        plt.xlabel("Over")
        plt.ylabel("Runs")

        plt.title("Runs Per Over")

        plt.show()


    def plot_phase_comparison(self, phases):
        """
        Placeholder for comparing match phases.
        """

        labels = list(phases.keys())
        values = list(phases.values())

        plt.figure(figsize=(8, 4))

        plt.bar(
            labels,
            values
        )

        plt.xlabel("Phase")
        plt.ylabel("Run Rate")

        plt.title("Phase Comparison")

        plt.show()