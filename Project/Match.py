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
        msg = game_message + concatenate_list_data(self.group1, 0)
        msg += "Group 2:\n==\n"
        msg += concatenate_list_data(self.group2, 0)
        msg += "Start pressing keys on your keyboard as fast as you can!!\n"
        return msg

    def print_result(self):
        str1 = "\u001b[36mGroup 1 typed in " + str(self.group1_result) + " characters. "
        str2 = "Group 2 typed in " + str(self.group2_result) + " characters.\033[0m"
        print("\n\u001b[31mGame Over!\033[0m\n" + str1 + str2)
        if self.group1_result > self.group2_result:
            winners = concatenate_list_data(self.group1, 1) + "Game over, sending out offer requests..."
            print("\033[1;3;32mGroup 1 wins!\033[0m\n\n\u001b[36mCongratulations to the winners:\n==\033[0m\n" + winners)
        elif self.group2_result > self.group1_result:
            winners = concatenate_list_data(self.group2, 1) + "Game over, sending out offer requests..."
            print("\033[1;3;32mGroup 2 wins!\033[0m\n\n\u001b[36mCongratulations to the winners:\n==\033[0m\n" + winners)
        else:
            print("\033[0;31mDraw!\033[0m\n\033[1;3;32mNone of the groups won the game!\033[0m\n" + "Game over, sending out offer requests...")
    #    group1_result = 0
    #    group2_result = 0

    def add_team_to_group1(self, team_name, client_thread):
        self.group1[team_name] = client_thread

    def add_team_to_group2(self, team_name, client_thread):
        self.group2[team_name] = client_thread

    def run_client_threads(self):
        for t in self.group1.values():
            t.start()
        for t in self.group2.values():
            t.start()

    # may add t.join() so the server thread does not have to sleep for 10 seconds
    # using hte join() will ensure that all the client threads has finished and closed
    # the sockets ( we may have to change that so we can safely call print_result )

    def join_client_threads(self):
        for t in self.group1.values():
            t.join()
        for t in self.group2.values():
            t.join()


def concatenate_list_data(lst, color):
    result = ""
    for element in lst:
        if color == 1:
            result += "\033[1;3;32m"
        result += element
        if color == 1:
            result += "\033[0m"
        result += "\n"
    return result
