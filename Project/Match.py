import threading


class Match:

    def __init__(self):
        self.group1 = {}
        self.group2 = {}
        self.group1_result = 0
        self.group2_result = 0
        self.counter1_lock = threading.Lock()
        self.counter2_lock = threading.Lock()

    def inc_g1_counter(self):
        with self.counter1_lock:
            self.group1_result += 1

    def inc_g2_counter(self):
        with self.counter2_lock:
            self.group2_result += 1

    def start_game_msg(self):
        game_message = "\nWelcome to Keyboard Spamming Battle Royale.\nGroup 1:\n==\n"
        msg = game_message + concatenate_list_data(self.group1)
        msg += "Group 2:\n==\n"
        msg += concatenate_list_data(self.group2)
        msg += "Start pressing keys on your keyboard as fast as you can!!\n"
        return msg

    def print_result(self):
        str1 = "Group 1 typed in " + str(self.group1_result) + " characters. "
        str2 = "Group 2 typed in " + str(self.group2_result) + " characters."
        print("\nGame Over!\n" + str1 + str2)
        if self.group1_result > self.group2_result:
            winners = concatenate_list_data(self.group1) + "Game over, sending out offer requests..."
            print(
                "\033[1;3;32mGroup 1 wins!\033[0m\n\n\u001b[36mCongratulations to the winners:\033[0m\n==\n" + winners)
        elif self.group2_result > self.group1_result:
            winners = concatenate_list_data(self.group2) + "Game over, sending out offer requests..."
            print(
                "\033[1;3;32mGroup 2 wins!\033[0m\n\n\u001b[36mCongratulations to the winners:\033[0m\n==\n" + winners)
        else:
            print(
                "\033[0;31mDraw!\033[0m\nNone of the groups won the game!\n" + "Game over, sending out offer requests...")
    #    group1_result = 0
    #    group2_result = 0

    def add_team_to_group1(self, team_name, client_thread):
        self.group1[team_name] = client_thread

    def add_team_to_group2(self, team_name, client_thread):
        self.group2[team_name] = client_thread


def concatenate_list_data(lst):
    result = ""
    for element in lst:
        result += element
        result += "\n"
    return result
