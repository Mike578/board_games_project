-- MySQL Workbench Synchronization
-- Generated: 2024-04-22 12:27
-- Model: New Model
-- Version: 1.0
-- Project: Name of the project
-- Author: micel

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

ALTER TABLE `bgg`.`categories` 
CHANGE COLUMN `bgg_id` `bgg_id` BIGINT(20) NOT NULL ,
ADD INDEX `fgfgh_idx` (`bgg_id` ASC) VISIBLE;
;

ALTER TABLE `bgg`.`designers` 
CHANGE COLUMN `bgg_id` `bgg_id` BIGINT(20) NOT NULL ,
ADD INDEX `fgdhg_idx` (`bgg_id` ASC) VISIBLE;
;

ALTER TABLE `bgg`.`games` 
ADD COLUMN `games_bgg_id` BIGINT(20) NOT NULL AFTER `kickstarted_binary2`,
ADD COLUMN `games_bgg_id1` BIGINT(20) NOT NULL AFTER `games_bgg_id`,
ADD COLUMN `games_games_bgg_id` BIGINT(20) NOT NULL AFTER `games_bgg_id1`,
ADD COLUMN `games_bgg_id2` BIGINT(20) NOT NULL AFTER `games_games_bgg_id`,
ADD COLUMN `games_games_bgg_id1` BIGINT(20) NOT NULL AFTER `games_bgg_id2`,
CHANGE COLUMN `bgg_id` `bgg_id` BIGINT(20) NOT NULL ,
ADD PRIMARY KEY (`bgg_id`, `games_bgg_id`);
;

ALTER TABLE `bgg`.`mechanics` 
CHANGE COLUMN `bgg_id` `bgg_id` BIGINT(20) NOT NULL ,
ADD INDEX `fgrgeh_idx` (`bgg_id` ASC) VISIBLE;
;

ALTER TABLE `bgg`.`publishers` 
CHANGE COLUMN `bgg_id` `bgg_id` BIGINT(20) NOT NULL ,
ADD INDEX `games_publishers_idx` (`bgg_id` ASC) VISIBLE;
;

ALTER TABLE `bgg`.`rankings` 
CHANGE COLUMN `bgg_id` `bgg_id` BIGINT(20) NOT NULL ;

ALTER TABLE `bgg`.`ratings_distribution` 
CHANGE COLUMN `bgg_id` `bgg_id` BIGINT(20) NOT NULL ,
ADD PRIMARY KEY (`bgg_id`);
;

ALTER TABLE `bgg`.`subcategories` 
CHANGE COLUMN `bgg_id` `bgg_id` BIGINT(20) NOT NULL ,
ADD INDEX `games_subcategories_idx` (`bgg_id` ASC) VISIBLE;
;

ALTER TABLE `bgg`.`themes` 
CHANGE COLUMN `bgg_id` `bgg_id` BIGINT(20) NOT NULL ,
ADD INDEX `games_themes_idx` (`bgg_id` ASC) VISIBLE;
;

ALTER TABLE `bgg`.`user_ratings` 
CHANGE COLUMN `bgg_id` `bgg_id` BIGINT(20) NOT NULL ,
ADD PRIMARY KEY (`bgg_id`);
;

ALTER TABLE `bgg`.`artists` 
ADD CONSTRAINT `games_artists`
  FOREIGN KEY (`bgg_id`)
  REFERENCES `bgg`.`games` (`bgg_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `bgg`.`categories` 
ADD CONSTRAINT `games_categories`
  FOREIGN KEY (`bgg_id`)
  REFERENCES `bgg`.`games` (`bgg_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `bgg`.`designers` 
ADD CONSTRAINT `games_designers`
  FOREIGN KEY (`bgg_id`)
  REFERENCES `bgg`.`games` (`bgg_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `bgg`.`mechanics` 
ADD CONSTRAINT `games_mechanics`
  FOREIGN KEY (`bgg_id`)
  REFERENCES `bgg`.`games` (`bgg_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `bgg`.`publishers` 
ADD CONSTRAINT `games_publishers`
  FOREIGN KEY (`bgg_id`)
  REFERENCES `bgg`.`games` (`bgg_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `bgg`.`rankings` 
ADD CONSTRAINT `games_rankings`
  FOREIGN KEY (`bgg_id`)
  REFERENCES `bgg`.`games` (`bgg_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `bgg`.`ratings_distribution` 
ADD CONSTRAINT `games_ratings_distribution`
  FOREIGN KEY (`bgg_id`)
  REFERENCES `bgg`.`games` (`bgg_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `bgg`.`subcategories` 
ADD CONSTRAINT `games_subcategories`
  FOREIGN KEY (`bgg_id`)
  REFERENCES `bgg`.`games` (`bgg_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `bgg`.`themes` 
ADD CONSTRAINT `games_themes`
  FOREIGN KEY (`bgg_id`)
  REFERENCES `bgg`.`games` (`bgg_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `bgg`.`user_ratings` 
ADD CONSTRAINT `user_ratings_games`
  FOREIGN KEY (`bgg_id`)
  REFERENCES `bgg`.`games` (`bgg_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
