import threading
from ANSI import *


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

        if not self.is_valid():
            print("no players registered for the match, sending out offer requests...")
            return

        str1 = ANSI.CYAN + "Group 1 typed in " + str(self.group1_result) + " characters. "
        str2 = "Group 2 typed in " + str(self.group2_result) + " characters." + ANSI.END
        print("\n" + ANSI.RED + "Game Over!" + ANSI.END + "\n" + str1 + str2)
        if self.group1_result > self.group2_result:
            winners = concatenate_list_data(self.group1, 1) + "Game over, sending out offer requests..."
            str3 = ANSI.GREEN_ITALIC + "Group 1 wins!" + ANSI.END + "\n\n"
            str3 += ANSI.CYAN + "Congratulations to the winners:\n==" + ANSI.END + "\n" + winners
            print(str3)
        elif self.group2_result > self.group1_result:
            winners = concatenate_list_data(self.group2, 1) + "Game over, sending out offer requests..."
            str4 = ANSI.GREEN_ITALIC + "Group 2 wins!" + ANSI.END + "\n\n"
            str4 += ANSI.CYAN + "Congratulations to the winners:\n==" + ANSI.END + "\n" + winners
        else:
            str5 = ANSI.LIGHT_RED + "Draw!" + ANSI.END + "\n" + ANSI.GREEN_ITALIC + "None of the groups won the game!"
            str5 += ANSI.END + "\n" + "Game over, sending out offer requests..."
            print(str5)

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

    def is_valid(self):
        return self.group1 or self.group2   # return if there were players registered to this match


def concatenate_list_data(lst, color):
    result = ""
    for element in lst:
        if color == 1:
            result += ANSI.GREEN_ITALIC
        result += element
        if color == 1:
            result += ANSI.END
        result += "\n"
    return result
