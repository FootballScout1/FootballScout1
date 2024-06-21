-- prepares a MySQL server for the football scouting project

CREATE DATABASE IF NOT EXISTS football_scout_dev_db;
CREATE USER IF NOT EXISTS 'football_scout_dev'@'localhost' IDENTIFIED BY 'football_scout_dev_pwd';
GRANT ALL PRIVILEGES ON `football_scout_dev_db`.* TO 'football_scout_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'football_scout_dev'@'localhost';
FLUSH PRIVILEGES;

