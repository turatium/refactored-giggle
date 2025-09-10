CREATE TABLE IF NOT EXISTS `sessions` (
	`id` integer primary key NOT NULL UNIQUE,
	`name` TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS `presentations` (
	`id` integer primary key NOT NULL UNIQUE,
	`name` TEXT NOT NULL,
	`authors` TEXT NOT NULL,
	`session_id` INTEGER NOT NULL,
	`likes` INTEGER NOT NULL,
FOREIGN KEY(`session_id`) REFERENCES `sessions`(`id`)
);
