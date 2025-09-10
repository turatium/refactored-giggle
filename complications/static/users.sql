CREATE TABLE IF NOT EXISTS `users` (
	`id` integer primary key NOT NULL UNIQUE,
	`fingerprint` TEXT NOT NULL UNIQUE,
	`created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS `liked` (
	`id` integer primary key NOT NULL UNIQUE,
	`presentation_id` INTEGER NOT NULL,
	`fingerprint_id` INTEGER NOT NULL,
FOREIGN KEY(`fingerprint_id`) REFERENCES `users`(`id`)
);
