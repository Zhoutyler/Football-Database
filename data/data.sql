INSERT INTO Coach (coachName,nationality,age) VALUES
('Julen Lopetegui', 'Spanish', '52'),
('Massimiliano Allegri', 'Italian', '51'),
('Ernesto Valverde', 'Spanish', '54'),
('Thomas Tuchel', 'German', '45'),
('Niko Kovač', 'German', '47'),
('José Mourinho', 'Portuguese', '55'),
('Maurizio Sarri', 'Italian', '59'),
('Jürgen Klopp', 'German', '51'),
('Diego Simeone', 'Argentine', '48'),
('Pep Guardiola', 'Spanish', '47');




INSERT INTO Club (clubName, league, ground, coachID, coachSince) VALUES
('Real Madrid CF', 'Laliga', 'Santiago Bernabéu Stadium', '1', '2018'),
('Juventus', 'Serie A', 'Allianz Stadium', '2', '2014'),
('FC Barcelona', 'Laliga', 'Camp Nou' ,'3' ,'2017'),
('Paris Saint-Germain', 'France Ligue1', 'Parc des Princes', '4', '2018'),
('FC Bayern Munich', 'Bundesliga', 'Allianz Arena', '5', '2018'),
('Manchester United','Premier League','Old Trafford', '6', '2016'),
('Chelsea', 'Premier League','Stamford Bridge', '7', '2018'),
('Liverpool F.C.', 'Premier League', 'Anfield', '8', '2015'),
('Atlético Madrid', 'Laliga', 'Wanda Metropolitano', '9', '2011'),
('Manchester City F.C.', 'Premier League', 'Etihad Stadium', '10', '2016');


INSERT INTO Competition (compName, founded, recent_champion) VALUES
('UEFA Champions League', '1955-09-04', 'Real Madrid CF'),
('UEFA Europa League', '1971-01-01', 'Atlético Madrid'),
('Laliga','1929-02-10','Barcelona'),
('Serie A', '1898-01-01', 'Juventus'),
('France Ligue1', '1932-09-11', 'Paris Saint-Germain'),
('Premier League', '1992-02-20', 'Manchester City F.C.'),
('Bundesliga', '1963-08-24','FC Bayern Munich'),
('EFL Cup', '1960-09-26', 'Manchester City F.C.'),
('FA Cup', '1871-03-16', 'Chelsea F.C.'),
('Copa del Rey', '1903-04-06', 'FC Barcelona');


INSERT INTO Match (score_a, score_b, club_a, club_b, ground, match_date, compName) VALUES
('0','3','Juventus','Real Madrid CF','Allianz Stadium','2018-4-3','UEFA Champions League'),
('1','3','Real Madrid CF','Juventus','Santiago Bernabéu Stadium','2018-4-11','UEFA Champions League'),
('1','2','FC Bayern Munich','Real Madrid CF','Allianz Arena','2018-4-25','UEFA Champions League'),
('2','2','Real Madrid CF','FC Bayern Munich','Santiago Bernabéu Stadium','2018-5-1','UEFA Champions League'),
('4','0','Paris Saint-Germain','FC Barcelona','Parc des Princes','2017-2-14','UEFA Champions League'),
('6','1','FC Barcelona','Paris Saint-Germain','Camp Nou','2017-3-8','UEFA Champions League'),
('4','0','Chelsea','Manchester United','Stamford Bridge','2016-10-23','Premier League'),
('2','0','Manchester United','Chelsea','Old Trafford','2017-4-16','Premier League'),
('5','0','Manchester City F.C.','Liverpool F.C.','Etihad Stadium','2017-9-9','Premier League'),
('4','3','Liverpool F.C.','Manchester City F.C.','Anfield','2018-1-14','Premier League');

\copy Player(full_name, club, acceleration, aggression, agility, balance, ball_control) FROM '/home/nc2734/project/players.csv' DELIMITER ',' CSV;

INSERT INTO Transfers (playerID, clubName, transfer_date) VALUES
('1','Juventus','2018-7-10'),
('3','Paris Saint-Germain','2017-8-3'),
('4','FC Barcelona','2014-7-11'),
('5','FC Bayern Munich','2011-7-1'),
('6','FC Bayern Munich','2014-7-1'),
('7','Chelsea','2012-7-1'),
('8','Real Madrid CF','2014-7-17'),
('10','Real Madrid CF','2005-8-31'),
('11','Manchester City F.C.','2015-8-30'),
('13','Real Madrid CF','2012-8-27');





INSERT INTO Account (username, pswd) VALUES
( 'aaaa' , '6402jnw' ),
( 'bbbb' , '2863hzo' ),
( 'cccc' , '8172pjy' ),
( 'dddd' , '4231xzo' ),
( 'eeee' , '4153ncv' ),
( 'ffff' , '3620ugt' ),
( 'gggg' , '3208zry' ),
( 'hhhh' , '8452mjk' ),
( 'iiii' , '2567aop' ),
( 'jjjj' , '6408hip' );

INSERT INTO Favorites ( userID, playerID) VALUES
( '1' , '10' ),
( '2' , '4' ),
( '3' , '2' ),
( '4' , '1' ),
( '5' , '2' ),
( '6' , '3' ),
( '7' , '9' ),
( '8' , '7' ),
( '9' , '1' ),
( '10' , '1' );

INSERT INTO Title ( titleName, year, clubName) VALUES



