DROP TABLE IF EXISTS users;

CREATE TABLE users(
	uid INT PRIMARY KEY NOT NULL,
	gender TEXT,
	state TEXT
);

DROP TABLE IF EXISTS user_events;

CREATE TABLE user_events(
	event_id INT NOT NULL,
	user_id INT NOT NULL,
	date TEXT,
	event_name TEXT,
	reg_before INT,
	reg_after INT,
	quick_before INT,
	quick_after INT,
	blitz_before INT,
	blitz_after INT,
	section TEXT,
	state TEXT,
	FOREIGN KEY (user_id) REFERENCES users(uid)
);