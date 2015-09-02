import csv

"""
A class which stores player data, availability info, and rankings.
Target use case is for a draft where the tracking of best available players is required.

Author: Louis Croce
Since: 9/1/2015
"""
class DraftBoard:
    """
    Read player information from a csv file into a dictionary and store relevant keys.
    """
    def __init__(self, s_rankings_filename, s_player_name_header, s_position_key, l_player_data_keys, l_experts):
        self.__l_player_data_keys = l_player_data_keys
        self.__s_position_key = s_position_key
        self.__l_experts = l_experts
        self.__s_availability_key = 'Available'
        self.__d_players = {}
        print 'Reading player rankings from data file.'
        # use csv reader to read player ranking file line by line into the self.__d_players dictionary
        try:
            with open(s_rankings_filename, 'rU') as csvfile:
                reader = csv.DictReader(csvfile)
                for s_line in reader:
                    s_player_name = s_line[s_player_name_header]
                    self.__d_players[s_player_name] = {}
                    for s_player_data_key in self.__l_player_data_keys:
                        self.__d_players[s_player_name][s_player_data_key] = s_line[s_player_data_key]
                    for s_expert in self.__l_experts:
                        self.__d_players[s_player_name][s_expert] = s_line[s_expert]
                    self.__d_players[s_player_name][self.__s_availability_key] = True
        except IOError:
            print 'Error: ' + s_rankings_filename + ' does not exist.'
        print 'Finished reading player rankings from data file.'

    """
    Return a list of the n_count best available players according to the specified expert
    at the specified position (if position is specified)
    """
    def get_n_best_available(self, s_expert, s_position, n_count):
        # list of player names
        l_best_available = []
        for s_player_name in self.__d_players:
            if self.__d_players[s_player_name][self.__s_availability_key]:
                if s_position == '' or s_position == self.__d_players[s_player_name][self.__s_position_key]:
                    l_best_available.append(s_player_name)
        # sort list of best available by specified expert ranking
        l_best_available.sort(key=lambda x: int(self.__d_players[x][s_expert]))
        return l_best_available[:n_count]


    """
    For each player in the list l_player_names, print the specified expert's ranking of that player,
    the player's name, and all the non-ranking data we have stored for that player.
    """
    def print_players_with_ranking(self, l_player_names, s_expert):
        for s_player_name in l_player_names:
            # add ranking to player info string
            s_player_info = str(self.__d_players[s_player_name][s_expert]) + '.\t' + s_player_name
            for s_player_data_key in self.__l_player_data_keys:
                # add additional information to player info string
                s_player_info += '\t' + self.__d_players[s_player_name][s_player_data_key]
            print s_player_info

    """
    Returns True if we have ranking data for the player specified.
    Returns False otherwise.
    """
    def contains_player(self, s_player_name):
        return s_player_name in self.__d_players

    """
    Marks player as unavailable if he exists.
    Returns True if the player exists and was previously available.
    Returns False otherwise.
    """
    def remove_player(self, s_player_name):
        if s_player_name in self.__d_players:
            if self.__d_players[s_player_name][self.__s_availability_key]:
                self.__d_players[s_player_name][self.__s_availability_key] = False
                return True
        return False

    """
    Marks player as available if he exists.
    Returns True if the player exists and was previously unavailable.
    Returns False otherwise.
    """
    def add_player(self, s_player_name):
        if s_player_name in self.__d_players:
            if not self.__d_players[s_player_name][self.__s_availability_key]:
                self.__d_players[s_player_name][self.__s_availability_key] = True
                return True
        return False

    """
    Return the list of experts names.
    """
    def get_experts_list(self):
        return self.__l_experts