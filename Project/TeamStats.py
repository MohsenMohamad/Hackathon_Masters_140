class TeamStats:

    def __init__(self, team_name):
        self.team_name = team_name
        self.wins = 0
        self.losses = 0
        self.high_score = 0
        self.total_points = 0
        self.keys = {}

    def add_win(self):
        self.wins += 1

    def add_loss(self):
        self.losses += 1

    def add_score(self,points):
        self.total_points += points
        if self.high_score < points:
            self.high_score = points

    def pressed_key(self, key):
        try:
            self.keys[key] += 1
        except KeyError:
            self.keys[key] = 1
