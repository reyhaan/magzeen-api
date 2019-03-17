DROP TABLE IF EXISTS users, teams, user_team_junction, posts, comments, reactions, sections, user_access_level CASCADE;

CREATE TABLE users (
	user_id SERIAL PRIMARY KEY,
    first_name VARCHAR,
	last_name VARCHAR,
    password VARCHAR NOT NULL,
	email VARCHAR NOT NULL,
    created_at DATE,
	updated_at DATE,
    type VARCHAR,
    domain_name VARCHAR
);

CREATE TABLE teams (
	team_id SERIAL PRIMARY KEY,
	team_name VARCHAR,
	team_slug VARCHAR,
	team_domain VARCHAR
);

CREATE TABLE user_team_junction (
	user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
	team_id INTEGER REFERENCES teams(team_id) ON DELETE CASCADE,
	CONSTRAINT junction_id PRIMARY KEY (user_id, team_id)
);

CREATE TABLE user_access_level (
	user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
	team_id INTEGER REFERENCES teams(team_id) ON DELETE CASCADE,
	access_level VARCHAR
);

CREATE TABLE comments (
	comment_id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users(user_id),
	content VARCHAR,
	created_at DATE,
	updated_at DATE
);

CREATE TABLE posts (
	post_id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users(user_id),
	title VARCHAR,
	body VARCHAR,
	mentions VARCHAR,
	tags VARCHAR,
	created_at DATE,
	updated_at DATE
);

CREATE TABLE reactions (
	reaction_id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users(user_id),
	reaction VARCHAR,
	created_at DATE,
	updated_at DATE
);

CREATE TABLE sections (
	section_id SERIAL PRIMARY KEY,
	team_id INTEGER REFERENCES teams(team_id),
	name VARCHAR,
	created_at DATE,
	updated_at DATE
);