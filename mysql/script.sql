
CREATE TABLE group_users(
	`group_id` VARCHAR(20),
	`user_id` VARCHAR(20),
	`count` INT NUT NULL,
	PRIMARY KEY(`group_id`,`message_id`)
);


CREATE TABLE ghaar_messages(
	`group_id` VARCHAR(20),
	`message_id` VARCHAR(20),
	PRIMARY KEY(`group_id`,`message_id`)
);