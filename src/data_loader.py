import csv

class DataLoader:
    def __init__(self, filepath, match_filepath):
        self.filepath = filepath
        self.match_filepath = match_filepath
        self.data = []
        self.matches = []

    def load(self):
        """Reads CSV file line-by-line and loads rows into memory as dictionaries."""
        with open(self.filepath, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["match_id"] = int(row["match_id"])
                row["inning"] = int(row["inning"])
                row["over"] = int(row["over"])
                row["ball"] = int(row["ball"])
                row["total_runs"] = int(row["total_runs"])
                row["is_wicket"] = 1 if row["dismissal_kind"] not in ("", "NA") else 0
                
                self.data.append(row)

        print(f"Loading {self.filepath} ... done ({len(self.data)} rows)")

    def load_matches(self):
        with open(self.match_filepath, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:

                row["id"] = int(row["id"])

                if row["target_runs"] not in ("", "NA"):
                    row["target_runs"] = int(row["target_runs"])
                else:
                    row["target_runs"] = None

                self.matches.append(row)

        print(f"Loading {self.match_filepath} ... done ({len(self.matches)} matches)")

    def get_match_info(self, match_id):

        for row in self.matches:
            if row["id"] == match_id:
                return row


    def get_match_ids(self):
        """Returns a list of unique match IDs present in the dataset."""
        return list(dict.fromkeys(row["match_id"] for row in self.data))

    def get_match_data(self, match_id):
        """Filters dataset for a single specific match ID."""
        return [row for row in self.data if row["match_id"] == match_id]

    def get_innings(self, match_data, inning_num):
        """Filters match data for a specific inning number (1 or 2)."""
        return [row for row in match_data if row["inning"] == inning_num]