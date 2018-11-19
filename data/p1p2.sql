DROP TABLE IF EXISTS Title;
DROP TABLE IF EXISTS Match;
DROP TABLE IF EXISTS Competition;
DROP TABLE IF EXISTS Transfers;
DROP TABLE IF EXISTS Favorites;
DROP TABLE IF EXISTS Player;
DROP TABLE IF EXISTS Club;
DROP TABLE IF EXISTS Account;
DROP TABLE IF EXISTS Coach;

CREATE TABLE Coach (
coachID serial NOT NULL,
coachName TEXT NOT NULL,
nationality TEXT,
age INT,
PRIMARY KEY (coachID),
CONSTRAINT valid_age CHECK (age > 0 AND age < 100),
CONSTRAINT valid_coach CHECK (coachID >= 0 AND coachID < 65536));

CREATE TABLE Club (
clubName CHAR(50) NOT NULL,
league TEXT NOT NULL,
ground TEXT,
coachID INT,
coachSince INT,
PRIMARY KEY (clubName),
FOREIGN KEY (coachID) REFERENCES Coach(coachID));

CREATE TABLE Competition (
compName CHAR(50) NOT NULL,
founded DATE,
recent_champion TEXT,
PRIMARY KEY (compName));

CREATE TABLE Match (
matchID serial NOT NULL,
score_a INT NOT NULL,
score_b INT NOT NULL,
club_a CHAR(50) NOT NULL,
club_b CHAR(50) NOT NULL,
ground TEXT,
match_date DATE,
compName CHAR(50) NOT NULL,
PRIMARY KEY (matchID),
FOREIGN KEY (club_a) REFERENCES Club(clubName) ON DELETE CASCADE,
FOREIGN KEY (club_b) REFERENCES Club(clubName) ON DELETE CASCADE,
FOREIGN KEY (compName) REFERENCES Competition(compName) ON DELETE CASCADE,
CONSTRAINT valid_match CHECK (matchID >= 0 AND matchID < 65536));

CREATE TABLE Player (
playerID serial NOT NULL,
full_name TEXT NOT NULL,
club CHAR(50) NOT NULL,
acceleration INT,
aggression INT,
agility INT,
balance INT,
ball_control INT,
PRIMARY KEY (playerID),
FOREIGN KEY (club) REFERENCES Club(clubName) ON DELETE CASCADE,
CONSTRAINT valid_player CHECK (playerID >= 0 AND playerID < 65536)
);

CREATE TABLE Transfers (
playerID INT NOT NULL,
clubName CHAR(50) NOT NULL,
transfer_date DATE,
PRIMARY KEY (playerID, clubName),
FOREIGN KEY (playerID) REFERENCES Player(playerID) ON DELETE CASCADE,
FOREIGN KEY (clubName) REFERENCES Club(clubName) ON DELETE CASCADE
);

CREATE TABLE Account (
userID serial,
username TEXT,
pswd TEXT,
PRIMARY KEY (userID),
CONSTRAINT valid_user CHECK (userID >= 0 AND userID < 65536)
);

CREATE TABLE Favorites (
userID INT NOT NULL,
playerID INT NOT NULL,
PRIMARY KEY (userID, playerID),
FOREIGN KEY (userID) REFERENCES Account(userID) ON DELETE CASCADE,
FOREIGN KEY (playerID) REFERENCES Player(playerID) ON DELETE CASCADE,
CONSTRAINT unique_pair UNIQUE(userID, playerID)
);

CREATE TABLE Title (
titleName CHAR(50),
year INT,
clubName CHAR(50) NOT NULL,
PRIMARY KEY (titleName, year)
);