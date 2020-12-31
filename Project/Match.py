import threading
from ANSI import *

'''
Here we implemented the game rules and the data/result sent from server to client 
at each match. We got two threads, one for group1 and another for group2 counting 
how many chars received from each group in every match.
'''


class Match:

    def __init__(self):
        self.group1 = {}
        self.group2 = {}
        self.group1_result = 0
        self.group2_result = 0
        self.counter1_lock = threading.Lock()
        self.counter2_lock = threading.Lock()

    def inc_g1_counter(self):   # counting how many chars group1 inserted
        with self.counter1_lock:
            self.group1_result += 1

    def inc_g2_counter(self):   # counting how many chars group2 inserted
        with self.counter2_lock:
            self.group2_result += 1

    def start_game_msg(self):  # The start message which will be sent right before starting the match.
        game_message = ANSI.CYAN + "\nWelcome to Keyboard Spamming Battle Royale." + ANSI.END
        game_message += (ANSI.YELLOW + "\nGroup 1:\n==\n" + ANSI.END)
        msg = game_message + concatenate_list_data(self.group1, 1)
        msg += ANSI.YELLOW + "Group 2:\n==\n" + ANSI.END
        msg += concatenate_list_data(self.group2, 1)
        msg += ANSI.CYAN + "Start pressing keys on your keyboard as fast as you can!!\n" + ANSI.END
        return msg
    # After changing the instructions so the server now sends the result to all clients instead of printing them out.
    # We got 3 cases, 1. group 1 won, 2. group 2 won, 3. draw and none of them one.
    def print_result(self):
        if not self.is_valid():
            print(ANSI.RED + "No players registered for the match, sending out offer requests..." + ANSI.END)
            return
        str0 = ANSI.BROWN + "\n====+====+====+====+====+====+====+====+====+===="
        str0 += "\n====+====+====+====+====+====+====+====+====+====" + ANSI.END
        str1 = ANSI.CYAN + "Group 1 typed in " + str(self.group1_result) + " characters. "
        str2 = "Group 2 typed in " + str(self.group2_result) + " characters." + ANSI.END
        end_game_message = ("\n" + ANSI.RED + "Game Over!" + ANSI.END + "\n" + str1 + str2)
        if self.group1_result > self.group2_result:
            winners = concatenate_list_data(self.group1, 1) + str0
            winners += "\n"
            str3 = ANSI.GREEN_ITALIC + "Group 1 wins!" + ANSI.END + "\n\n"
            str3 += ANSI.CYAN + "Congratulations to the winners:\n==" + ANSI.END + "\n" + winners
            return end_game_message+'\n'+str3
        elif self.group2_result > self.group1_result:
            winners = concatenate_list_data(self.group2, 1) + str0
            winners += "\n"
            str4 = ANSI.GREEN_ITALIC + "Group 2 wins!" + ANSI.END + "\n\n"
            str4 += ANSI.CYAN + "Congratulations to the winners:\n==" + ANSI.END + "\n" + winners
            return end_game_message+'\n'+str4
        else:
            str5 = ANSI.LIGHT_RED + "Draw!" + ANSI.END + "\n" + ANSI.GREEN_ITALIC + "None of the groups won the game!"
            str5 += ANSI.END + "\n" + str0 + "\n"
            return end_game_message+'\n'+str5

    def add_team_to_group1(self, team_name, client_thread):
        self.group1[team_name] = client_thread

    def add_team_to_group2(self, team_name, client_thread):
        self.group2[team_name] = client_thread

    def run_client_threads(self):          # running each thread to start the match
        for t in self.group1.values():
            t.start()
        for t in self.group2.values():
            t.start()

    def join_client_threads(self):
        for t in self.group1.values():
            t.join()
        for t in self.group2.values():
            t.join()

    def is_valid(self): # checking if any of the groups not empty
        return self.group1 or self.group2   # return if there were players registered to this match


def concatenate_list_data(lst, color):  # given a list of strings, this function concatenate them.
    result = ""
    for element in lst:
        if color == 1:
            result += ANSI.GREEN_ITALIC
        result += element
        if color == 1:
            result += ANSI.END
        result += "\n"
    return result
