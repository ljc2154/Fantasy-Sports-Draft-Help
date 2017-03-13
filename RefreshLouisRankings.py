

with open('LouisRankings.txt') as f:
    player_names = f.readlines()
    rank = 1
    for player_name in player_names: