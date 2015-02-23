# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.5.38-0ubuntu0.14.04.1)
# Database: bingo
# Generation Time: 2015-02-23 19:25:06 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table daub_tweets
# ------------------------------------------------------------

CREATE TABLE `daub_tweets` (
  `daub_tweet_id` bigint(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `goal_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `embed_code` text,
  `image_url` text NOT NULL,
  PRIMARY KEY (`daub_tweet_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table goals
# ------------------------------------------------------------

CREATE TABLE `goals` (
  `goal_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `hashtag` varchar(255) DEFAULT NULL,
  `flavor_text` text,
  `headline` text,
  `url` text,
  PRIMARY KEY (`goal_id`),
  UNIQUE KEY `hashtag` (`hashtag`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table user_card_squares
# ------------------------------------------------------------

CREATE TABLE `user_card_squares` (
  `user_card_square_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `goal_id` int(11) NOT NULL,
  `position` int(11) NOT NULL,
  `daub_tweet_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`user_card_square_id`),
  UNIQUE KEY `user_id` (`user_id`,`position`),
  KEY `user_id_2` (`user_id`),
  KEY `goal_id` (`goal_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table users
# ------------------------------------------------------------

CREATE TABLE `users` (
  `user_id` bigint(11) unsigned NOT NULL AUTO_INCREMENT,
  `screen_name` varchar(255) DEFAULT NULL,
  `profile_image_url` text,
  `daubs_left` int(11) NOT NULL DEFAULT '4',
  `total_daubs` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
