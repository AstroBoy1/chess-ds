INSERT INTO users(uid, gender, state)
VALUES(1, 'M', 'WA');

INSERT INTO user_events(
	event_id,
	user_id,
	date,
	event_name,
	reg_before,
	reg_after,
	quick_before,
	quick_after,
	blitz_before,
	blitz_after,
	section,
	state
)

VALUES(
	1,
	1,
	12-31-94,
	'event name',
	NULL,
	2010,
	2100,
	2200,
	2300,
	2400,
	'section name',
	'HI'
);

INSERT INTO user_events(
	event_id,
	user_id,
	date,
	event_name,
	reg_before,
	reg_after,
	quick_before,
	quick_after,
	blitz_before,
	blitz_after,
	section,
	state
)

VALUES(
	1,
	1,
	12-31-94,
	'event name',
	2000,
	2010,
	2100,
	2200,
	2300,
	2400,
	'section name',
	'HI'
);