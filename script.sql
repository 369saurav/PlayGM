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

CREATE TABLE IF NOT EXISTS `chess_positions` (
                  `id` INT PRIMARY KEY AUTO_INCREMENT,
                  `game_id` INT NOT NULL,
                  `fen` VARCHAR(100) NOT NULL,
                  `next_move` VARCHAR(10) NOT NULL,
                  `move_number` INT NOT NULL,
                  `embedding` vector(384) COMMENT "hnsw(distance=cosine)"
                );
CREATE TABLE IF NOT EXISTS `chess_eco` (
                  `id` INT PRIMARY KEY AUTO_INCREMENT,
                  `eco` char(5),
                  `eco_name` varchar(50)
                );


CREATE TABLE IF NOT EXISTS `chess_positions` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `game_id` INT NOT NULL,
  `player_color` char(1),
  `player_fen` VARCHAR(100),
  `opponent_fen` VARCHAR(100),
  `move_number` INT NOT NULL,
  `embedding` vector(384)
);