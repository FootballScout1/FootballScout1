-- prepares a MySQL server for the football scouting project

CREATE DATABASE IF NOT EXISTS football_scout_test_db;
CREATE USER IF NOT EXISTS 'football_scout_test'@'localhost' IDENTIFIED BY 'football_scout_test_pwd';
GRANT ALL PRIVILEGES ON `football_scout_test_db`.* TO 'football_scout_test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'football_scout_test'@'localhost';
FLUSH PRIVILEGES;

