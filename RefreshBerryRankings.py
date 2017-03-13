from bs4 import BeautifulSoup
import urllib
from sqlalchemy import *
from DraftBoard import DB_CONNECTION_STRING

BERRY_RANKINGS_URL = 'http://www.espn.com/fantasy/football/story/_/id/14765088/matthew-berry-2016-fantasy-football-rankings-nfl'
ESPN_RANKINGS_URL = 'http://www.espn.com/fantasy/football/story/_/id/16287927/2016-fantasy-football-rankings-top-300'
CLAY_PPR_RANKINGS_URL = 'http://www.espn.com/fantasy/football/story/_/id/17054264/fantasy-football-ppr-rankings-2016-espn-nfl-rankings-ppr-top-300-overall'
YATES_RANKINGS_URL = 'http://www.espn.com/fantasy/football/story/_/id/17171463/field-yates-qb-rb-wr-te-d-st-kicker-rankings-2016-fantasy-football-nfl'
KARABELL_RANKINGS_URL = 'http://www.espn.com/fantasy/football/story/_/id/15592938/eric-karabell-top-100-rankings-2016-fantasy-football-nfl'
COCKCROFT_RANKINGS_URL = 'http://www.espn.com/fantasy/football/story/_/id/15564986/tristan-h-cockcroft-2016-fantasy-football-rankings-nfl'

BERRY_TABLE_HEADER = "Matthew Berry's Top 200 for 2016"
ESPN_TABLE_HEADER = '2016 rankings: Top 300 overall'
CLAY_PPR_TABLE_HEADER = '2016 rankings: PPR top 300 overall'
YATES_TABLE_HEADER = "2016 Rankings: Field Yates' top 160"
KARABELL_TABLE_HEADER = "Eric Karabell's Top 100 for 2016"
COCKCROFT_TABLE_HEADER = '2016 Rankings: Top 10'

UPSERT_PLAYER_QUERY = """INSERT INTO t_players (berry_player_name, team_abbreviation, position_id)
    VALUES (:berry_player_name, :team_abbreviation, :position_id)
    ON DUPLICATE KEY UPDATE position_id = position_id;
    """

GET_PLAYER_ID_QUERY = """SELECT player_id FROM t_players WHERE berry_player_name= :berry_player_name;"""

INSERT_RANKING_QUERY = """INSERT INTO t_rankings (player_id, expert_name, rank) VALUES (:player_id, :expert_name, :rank)"""

CLEAR_EXPERT_RANKINGS_QUERY = """DELETE FROM t_rankings WHERE expert_name = :expert_name;"""

def build_position_to_id_map_from_db(db_engine):
    get_positions_and_ids_query = """SELECT position_id, berry_position_abbreviation, espn_position_abbreviation
        FROM t_positions;"""
    result = db_engine.execute(text(get_positions_and_ids_query))
    rows = result.fetchall()
    position_to_id_map = {}
    for row in rows:
        position_to_id_map[row['berry_position_abbreviation']] = row['position_id']
        position_to_id_map[row['espn_position_abbreviation']] = row['position_id']
    return position_to_id_map

def build_team_to_abbreviation_map_from_db(db_engine):
    get_positions_and_ids_query = """SELECT team_name, team_abbreviation
        FROM t_teams;"""
    result = db_engine.execute(text(get_positions_and_ids_query))
    rows = result.fetchall()
    team_to_abbreviation_map = {}
    for row in rows:
        team_to_abbreviation_map[row['team_name']] = row['team_abbreviation']
    return team_to_abbreviation_map

def find_rankings_table(rankings_page_soup, table_text):
    caption_text = rankings_page_soup.find(text=table_text)
    caption = caption_text.parent
    table = caption.parent
    return table

def add_rankings_from_table(table, db_engine, position_to_id_map, expert_name, team_to_abbreviation_map):
    rows = table.find('tbody').find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        ranking = cells[0].contents[0].replace('.', '').strip()
        anchor = cells[0].find('a')
        if not anchor:
            continue
        player_name = anchor.get_text().strip()
        position = cells[1].get_text()
        if len(cells) > 2:
            team_abbreviation = cells[2].get_text()
        elif 6 == position_to_id_map[position]:
                #hacky but doing this because berry's table is now missing columns in certain rows
                team_name = player_name.split()[-1]
                team_abbreviation = team_to_abbreviation_map[team_name]
        else:
            print 'oh shit, we got issues with ' + player_name
            continue

        db_engine.execute(text(UPSERT_PLAYER_QUERY), {'berry_player_name': player_name, 'team_abbreviation': team_abbreviation, 'position_id': position_to_id_map[position]})
        result = db_engine.execute(text(GET_PLAYER_ID_QUERY), {'berry_player_name': player_name})
        row = result.fetchone()
        player_id = row['player_id']
        db_engine.execute(text(INSERT_RANKING_QUERY), {'player_id': player_id, 'expert_name': expert_name, 'rank': ranking})

        print ranking + ' ' + player_name + ' ' + str(position_to_id_map[position]) + ' ' + team_abbreviation



def main():
    db_engine = create_engine(DB_CONNECTION_STRING, echo=False)
    position_to_id_map = build_position_to_id_map_from_db(db_engine)
    team_to_abbreviation_map = build_team_to_abbreviation_map_from_db(db_engine)
    # Berry Top 200
    rankings_page = urllib.urlopen(BERRY_RANKINGS_URL).read()
    rankings_page_soup = BeautifulSoup(rankings_page, 'html.parser')
    table = find_rankings_table(rankings_page_soup, BERRY_TABLE_HEADER)
    db_engine.execute(text(CLEAR_EXPERT_RANKINGS_QUERY), {'expert_name': 'Berry'})
    add_rankings_from_table(table, db_engine, position_to_id_map, 'Berry', team_to_abbreviation_map)

    # ESPN Top 300
    rankings_page = urllib.urlopen(ESPN_RANKINGS_URL).read()
    rankings_page_soup = BeautifulSoup(rankings_page, 'html.parser')
    table = find_rankings_table(rankings_page_soup, ESPN_TABLE_HEADER)
    db_engine.execute(text(CLEAR_EXPERT_RANKINGS_QUERY), {'expert_name': 'ESPN'})
    add_rankings_from_table(table, db_engine, position_to_id_map, 'ESPN', team_to_abbreviation_map)

    # Clay PPR Top 300
    rankings_page = urllib.urlopen(CLAY_PPR_RANKINGS_URL).read()
    rankings_page_soup = BeautifulSoup(rankings_page, 'html.parser')
    table = find_rankings_table(rankings_page_soup, CLAY_PPR_TABLE_HEADER)
    db_engine.execute(text(CLEAR_EXPERT_RANKINGS_QUERY), {'expert_name': 'Clay'})
    add_rankings_from_table(table, db_engine, position_to_id_map, 'Clay', team_to_abbreviation_map)

    # Yates Top 160
    rankings_page = urllib.urlopen(YATES_RANKINGS_URL).read()
    rankings_page_soup = BeautifulSoup(rankings_page, 'html.parser')
    table = find_rankings_table(rankings_page_soup, YATES_TABLE_HEADER)
    db_engine.execute(text(CLEAR_EXPERT_RANKINGS_QUERY), {'expert_name': 'Yates'})
    add_rankings_from_table(table, db_engine, position_to_id_map, 'Yates', team_to_abbreviation_map)

    # # Karabell Top 100
    # rankings_page = urllib.urlopen(KARABELL_RANKINGS_URL).read()
    # rankings_page_soup = BeautifulSoup(rankings_page, 'html.parser')
    # table = find_rankings_table(rankings_page_soup, KARABELL_TABLE_HEADER)
    # db_engine.execute(text(CLEAR_EXPERT_RANKINGS_QUERY), {'expert_name': 'Karabell'})
    # add_rankings_from_table(table, db_engine, position_to_id_map, 'Karabell', team_to_abbreviation_map)
    #
    # # Cockcroft Top 100
    # rankings_page = urllib.urlopen(COCKCROFT_RANKINGS_URL).read()
    # rankings_page_soup = BeautifulSoup(rankings_page, 'html.parser')
    # table = find_rankings_table(rankings_page_soup, COCKCROFT_TABLE_HEADER)
    # db_engine.execute(text(CLEAR_EXPERT_RANKINGS_QUERY), {'expert_name': 'Cockcroft'})
    # add_rankings_from_table(table, db_engine, position_to_id_map, 'Cockcroft', team_to_abbreviation_map)



######################
# SCRIPT BEGINS HERE #
######################
main()