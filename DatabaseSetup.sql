CREATE TABLE t_teams (
  team_abbreviation VARCHAR(10) NOT NULL,
  bye_week INT NOT NULL,
  PRIMARY KEY (team_abbreviation)
) ENGINE=InnoDB;

INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('GB', 4);
INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('PHI', 4);

INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('JAC', 5);
INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('KC', 5);
INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('NO', 5);
INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('SEA', 5);

INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('MIN', 6);
INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('TB', 6);

INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('CAR', 7);
INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('DAL', 7);

INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('BAL', 8);
INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('LA', 8);
INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('MIA', 8);
INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('NYG', 8);
INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('PIT', 8);
INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('SF', 8);

INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('ARI', 9);
INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('CHI', 9);
INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('CIN', 9);
INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('HOU', 9);
INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('NE', 9);
INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('WAS', 9);

INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('BUF', 10);
INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('DET', 10);
INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('IND', 10);
INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('OAK', 10);

INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('ATL', 11);
INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('DEN', 11);
INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('NYJ', 11);
INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('SD', 11);

INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('CLE', 13);
INSERT INTO t_teams (team_abbreviation, bye_week) VALUES ('TEN', 13);

CREATE TABLE t_experts (
  expert_name VARCHAR(30) NOT NULL,
  PRIMARY KEY (expert_name)
) ENGINE=InnoDB;

INSERT INTO t_experts (expert_name) VALUES ('Berry');

CREATE TABLE t_positions (
  position_id INT NOT NULL AUTO_INCREMENT,
  berry_position_abbreviation VARCHAR(10) UNIQUE,
  PRIMARY KEY (position_id)
) ENGINE=InnoDB;

INSERT INTO t_positions (berry_position_abbreviation) VALUES ('QB');
INSERT INTO t_positions (berry_position_abbreviation) VALUES ('RB');
INSERT INTO t_positions (berry_position_abbreviation) VALUES ('WR');
INSERT INTO t_positions (berry_position_abbreviation) VALUES ('TE');
INSERT INTO t_positions (berry_position_abbreviation) VALUES ('K');
INSERT INTO t_positions (berry_position_abbreviation) VALUES ('D/ST');

CREATE TABLE t_players (
  player_id INT NOT NULL AUTO_INCREMENT,
  berry_player_name VARCHAR(40) UNIQUE,
  team_abbreviation VARCHAR(10) NOT NULL,
  position_id INT NOT NULL,
  PRIMARY KEY (player_id),
  FOREIGN KEY (team_abbreviation) REFERENCES t_teams(team_abbreviation)
) ENGINE=InnoDB;

CREATE TABLE t_rankings (
  player_id INT NOT NULL,
  expert_name VARCHAR(30) NOT NULL,
  rank INT NOT NULL,
  PRIMARY KEY (expert_name, rank),
  UNIQUE (player_id, expert_name),
  FOREIGN KEY (player_id) REFERENCES t_players(player_id),
  FOREIGN KEY (expert_name) REFERENCES t_experts(expert_name)
) ENGINE=InnoDB;

INSERT INTO t_experts (expert_name) VALUES ('ESPN');
ALTER TABLE t_positions ADD COLUMN espn_position_abbreviation VARCHAR(10);
UPDATE t_positions SET espn_position_abbreviation = 'QB' WHERE berry_position_abbreviation = 'QB';
UPDATE t_positions SET espn_position_abbreviation = 'RB' WHERE berry_position_abbreviation = 'RB';
UPDATE t_positions SET espn_position_abbreviation = 'WR' WHERE berry_position_abbreviation = 'WR';
UPDATE t_positions SET espn_position_abbreviation = 'TE' WHERE berry_position_abbreviation = 'TE' ;
UPDATE t_positions SET espn_position_abbreviation = 'K' WHERE berry_position_abbreviation = 'K';
UPDATE t_positions SET espn_position_abbreviation = 'DST' WHERE berry_position_abbreviation = 'D/ST';
ALTER TABLE t_positions MODIFY COLUMN espn_position_abbreviation VARCHAR(10) NOT NULL;

ALTER TABLE t_teams ADD COLUMN team_name VARCHAR(20);
UPDATE t_teams SET team_name = 'Cardinals' WHERE team_abbreviation = 'ARI';
UPDATE t_teams SET team_name = 'Falcons' WHERE team_abbreviation = 'ATL';
UPDATE t_teams SET team_name = 'Ravens' WHERE team_abbreviation = 'BAL';
UPDATE t_teams SET team_name = 'Bills' WHERE team_abbreviation = 'BUF';
UPDATE t_teams SET team_name = 'Panthers' WHERE team_abbreviation = 'CAR';
UPDATE t_teams SET team_name = 'Bears' WHERE team_abbreviation = 'CHI';
UPDATE t_teams SET team_name = 'Bengals' WHERE team_abbreviation = 'CIN';
UPDATE t_teams SET team_name = 'Browns' WHERE team_abbreviation = 'CLE';
UPDATE t_teams SET team_name = 'Cowboys' WHERE team_abbreviation = 'DAL';
UPDATE t_teams SET team_name = 'Broncos' WHERE team_abbreviation = 'DEN';
UPDATE t_teams SET team_name = 'Lions' WHERE team_abbreviation = 'DET';
UPDATE t_teams SET team_name = 'Ravens' WHERE team_abbreviation = 'BAL';
UPDATE t_teams SET team_name = 'Packers' WHERE team_abbreviation = 'GB';
UPDATE t_teams SET team_name = 'Texans' WHERE team_abbreviation = 'HOU';
UPDATE t_teams SET team_name = 'Colts' WHERE team_abbreviation = 'IND';
UPDATE t_teams SET team_name = 'Jaguars' WHERE team_abbreviation = 'JAC';
UPDATE t_teams SET team_name = 'Chiefs' WHERE team_abbreviation = 'KC';
UPDATE t_teams SET team_name = 'Rams' WHERE team_abbreviation = 'LA';
UPDATE t_teams SET team_name = 'Dolphins' WHERE team_abbreviation = 'MIA';
UPDATE t_teams SET team_name = 'Vikings' WHERE team_abbreviation = 'MIN';
UPDATE t_teams SET team_name = 'Patriots' WHERE team_abbreviation = 'NE';
UPDATE t_teams SET team_name = 'Saints' WHERE team_abbreviation = 'NO';
UPDATE t_teams SET team_name = 'Giants' WHERE team_abbreviation = 'NYG';
UPDATE t_teams SET team_name = 'Jets' WHERE team_abbreviation = 'NYJ';
UPDATE t_teams SET team_name = 'Raiders' WHERE team_abbreviation = 'OAK';
UPDATE t_teams SET team_name = 'Eagles' WHERE team_abbreviation = 'PHI';
UPDATE t_teams SET team_name = 'Steelers' WHERE team_abbreviation = 'PIT';
UPDATE t_teams SET team_name = 'Chargers' WHERE team_abbreviation = 'SD';
UPDATE t_teams SET team_name = 'Seahawks' WHERE team_abbreviation = 'SEA';
UPDATE t_teams SET team_name = '49ers' WHERE team_abbreviation = 'SF';
UPDATE t_teams SET team_name = 'Buccaneers' WHERE team_abbreviation = 'TB';
UPDATE t_teams SET team_name = 'Titans' WHERE team_abbreviation = 'TEN';
UPDATE t_teams SET team_name = 'Redskins' WHERE team_abbreviation = 'WAS';
ALTER TABLE t_teams MODIFY COLUMN team_name VARCHAR(20) NOT NULL;

INSERT INTO t_experts (expert_name) VALUES ('Clay');
INSERT INTO t_experts (expert_name) VALUES ('Yates');
INSERT INTO t_experts (expert_name) VALUES ('Karabell');
INSERT INTO t_experts (expert_name) VALUES ('Cockcroft');