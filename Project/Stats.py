from ANSI import *


teams_stats = {}

# Bonus 2 Impl
class Data:

    def __init__(self):
        self.groups = {}  # group_name, [all teams]
        self.statistics1 = {}  # group_name, scores
        self.statistics2 = {}  # group_name, number_of_games_won

    def top_three_winners(self):  # prints top 3 groups who won highest number of matches.
        dct = self.statistics2
        group1 = max(dct, key=dct.get)
        dct.pop(group1)
        group2 = max(dct, key=dct.get)
        dct.pop(group2)
        group3 = max(dct, key=dct.get)
        dct.pop(group3)
        print(ANSI.CYAN + "Here are top 3 groups winners, who got most winning games!" + ANSI.END)
        print("Group1:\n==")
        self.print_teams(group1)
        print("Group2:\n==")
        self.print_teams(group1)
        print("Group3:\n==")
        self.print_teams(group1)
        print(ANSI.GREEN_ITALIC + "Congratulations, you are the best!" + ANSI.END + "\n")

    def highest_score(self):  # prints the group who has highest score in a single match.
        dct = self.statistics1
        winner = max(dct, key=dct.get)
        print(ANSI.CYAN + "Here is the players who scored the most in one match!" + ANSI.END)
        self.print_teams(winner)

    def print_teams(self, group_name):
        lst = self.groups[group_name]
        for item in lst:
            print(ANSI.GREEN_ITALIC + item + ANSI.END + "\n")
