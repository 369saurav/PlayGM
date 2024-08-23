CREATE TABLE IF NOT EXISTS `chess_games_data` (
                  `game_id` INT PRIMARY KEY AUTO_INCREMENT,
                  `player_name` VARCHAR(100) NOT NULL,
                  `player_rating` INT,
                  `opponent_name` VARCHAR(100) NOT NULL,
                  `opponent_rating` INT,
                  `date` DATE NOT NULL,
                  `player_piece_color` ENUM ('W', 'B') NOT NULL,
                  `chess_annotation_pgn` TEXT NOT NULL,
                  `ECO` char(5),
                  `result` VARCHAR(10) NOT NULL,
                  `event` VARCHAR(50),
                  `location` VARCHAR(25)
                );

CREATE TABLE IF NOT EXISTS `chess_eco` (
                  `id` INT PRIMARY KEY AUTO_INCREMENT,
                  `eco` char(5),
                  `eco_name` varchar(50)
                );


CREATE TABLE IF NOT EXISTS `chess_positions` (
  `id` INT AUTO_INCREMENT,
  `game_id` INT NOT NULL,
  `player_color` char(1),
  `player_fen` VARCHAR(100),
  `opponent_fen` VARCHAR(100),
  `move_number` INT NOT NULL,
  `embedding` vector(384) COMMENT "hnsw(distance=cosine)",
  `player_id` INT NOT NULL
)PARTITION BY LIST (`player_id`) (
    PARTITION p1 VALUES IN (1),
    PARTITION p2 VALUES IN (2),
    PARTITION p3 VALUES IN (3),
    PARTITION p4 VALUES IN (4),
    PARTITION p5 VALUES IN (5),
    PARTITION p6 VALUES IN (6),
    PARTITION p7 VALUES IN (7),
    PARTITION p8 VALUES IN (8),
    PARTITION p9 VALUES IN (9),
    PARTITION p10 VALUES IN (10)
);


CREATE TABLE IF NOT EXISTS `chess_players` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `player_name` VARCHAR(50) NOT NULL,
  `player_display_name` VARCHAR(50)
    );