from DraftBoard import DraftBoard

"""
A script which utilizes the DraftBoard class to assist a user in a Fantasy Football Draft.

Author: Louis Croce
Since: 9/1/2015
"""

S_RANKINGS_FILENAME             = 'FantasyFootballRankings.csv'              # csv file of player data and rankings
S_PLAYER_NAME_HEADER            = 'Player Name'                              # player name header of rankings csv file
S_POSITION_HEADER               = 'Position'                                 # position header of rankings csv file
L_PLAYER_DATA_HEADERS           = [S_POSITION_HEADER, 'Team', 'Bye Week']    # non-ranking player data headers
S_BEST_AVAILABLE_COMMAND        = 'rank'                                     # command used when best available players desired
S_ADD_COMMAND                   = 'add'                                      # command used when making a player available
S_REMOVE_COMMAND                = 'rm'                                       # command used when making a player unavailable
S_QUIT_COMMAND                  = 'quit'                                     # command used to exit program
S_HELP_COMMAND                  = 'help'                                     # command used to render command options and descriptions
S_PROMPT                        = '$ '                                       # prompt displayed to user
N_DEFAULT_BEST_AVAILABLE_COUNT  = 10                                         # default amount of players a request for best available will display

"""
Print the command options.
"""
def print_command_options():
    print 'Command Options:'
    print S_BEST_AVAILABLE_COMMAND + ' <expert> (<position>) : Get best available players at position according to expert.'
    print S_ADD_COMMAND + ' <player name> : Mark player as available (default).'
    print S_REMOVE_COMMAND + ' <player name> : Mark player as drafted.'
    print S_QUIT_COMMAND + ' : Terminate program.'
    print S_HELP_COMMAND + ' : Display command options.'

"""
Build the list of experts from the rankings file.
Returns a list of experts names as they are in the rankings file headers.
Returns None if the rankings file doesn't exist.
"""
def get_experts_list():
    try:
        with open(S_RANKINGS_FILENAME, 'r') as f:
            s_first_row = f.readline().replace('\n', '')
            l_column_names = s_first_row.split(',')
            n_non_ranking_columns_in_csv = 1 + len(L_PLAYER_DATA_HEADERS)
            return l_column_names[n_non_ranking_columns_in_csv:]
    except IOError:
        print 'Error: ' + S_RANKINGS_FILENAME + ' does not exist.'
    return None

"""
Query draft_board for best available players (position and count optional) for a specified expert.
Prints the players names along with that expert's ranking for the player and the non-ranking data for the player.
"""
def handle_rank_command(draft_board, args):
    # rank the next 10 available players based on the expert provided
    if len(args) > 0:
        s_expert = args[0]
        if s_expert in draft_board.get_experts_list():
            s_position = ''
            n_count = N_DEFAULT_BEST_AVAILABLE_COUNT
            if len(args) > 1:
                s_position = args[1]
            # get best available
            l_best_available_players = draft_board.get_n_best_available(s_expert, s_position, n_count)
            if l_best_available_players:
                # print best available
                print 'Best Available Players according to ' + s_expert + ':'
                draft_board.print_players_with_ranking(l_best_available_players, s_expert)
            else:
                print 'Error: There were no available players that met your requirements. Try a different position?'
        else:
            print 'Usage Error: Expert not found. Format should be \"rank <expert> <position> <count>\".'
    else:
        print 'Usage Error: No expert provided. Format should be \"rank <expert> <position> <count>\".'

"""
Depending on the value of command, attempts to draft a player from or re-add a player to the draft board.
"""
def handle_add_remove_command(draft_board, command, args):
    if len(args) > 0:
        s_player_name = ' '.join(args)
        if draft_board.contains_player(s_player_name):
            if command == S_REMOVE_COMMAND:
                # attempting to remove (draft) player
                if draft_board.remove_player(s_player_name):
                    print 'Success: Player ' + s_player_name + ' drafted.'
                else:
                    print 'Error: Player ' + s_player_name + ' has already been drafted.'
            else:
                # attempting to add player (fix mistake)
                if draft_board.add_player(s_player_name):
                    print 'Success: Player ' + s_player_name + ' re-added.'
                else:
                    print 'Error: Player ' + s_player_name + ' is still available.'
        else:
            print 'Usage Error: Player not found. Format should be \"' + command + ' <Player Name>\".'
    else:
        print 'Usage Error: No Player Name provided. Format should be \"' + command + ' <Player Name>\".'

"""
Handles user input to manipulate the draft board.
"""
def handle_user_interaction(draft_board):
    s_command = raw_input(S_PROMPT)
    while s_command != S_QUIT_COMMAND:
        l_command_args = s_command.split(' ')
        s_action = l_command_args[0]
        if s_action == S_BEST_AVAILABLE_COMMAND:
            handle_rank_command(draft_board, l_command_args[1:])
        elif s_action == S_REMOVE_COMMAND or s_action == S_ADD_COMMAND:
            handle_add_remove_command(draft_board, s_action, l_command_args[1:])
        elif s_action == S_HELP_COMMAND:
            print_command_options()
        else:
            print 'Error: Command ' + s_command + ' is invalid. Enter ' + S_HELP_COMMAND + ' for command options.'
        s_command = raw_input(S_PROMPT)
    print 'Program terminated. Good bye!'


"""
Initializes the draft board and allows a user to manipulate it.
"""
def main():
    draft_board = DraftBoard(S_RANKINGS_FILENAME, S_PLAYER_NAME_HEADER, S_POSITION_HEADER, L_PLAYER_DATA_HEADERS, get_experts_list())
    handle_user_interaction(draft_board)

######################
# SCRIPT BEGINS HERE #
######################
main()