DROP DATABASE IF EXISTS Ghaar;
CREATE DATABASE Ghaar;
use Ghaar;

DROP TABLE IF EXISTS group_users;
CREATE TABLE group_users(
	`group_id` VARCHAR(20),
	`user_id` VARCHAR(20),
	`count` INT NOT NULL,
	PRIMARY KEY(`group_id`,`user_id`)
);

DROP TABLE IF EXISTS ghaar_messages;
CREATE TABLE ghaar_messages(
	`group_id` VARCHAR(20),
	`message_id` VARCHAR(20),
	PRIMARY KEY(`group_id`,`message_id`)
);

DROP TABLE IF EXISTS messages;
CREATE TABLE messages(
	`group_id` VARCHAR(20),
	`message_id` VARCHAR(20),
	`caption` TEXT, 
	`image_hash` VARCHAR(30),
	`video_hash` TEXT,
	PRIMARY KEY(`group_id`,`message_id`)
);