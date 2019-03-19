DROP TABLE IF EXISTS users, teams, user_team_junction, posts, comments, reactions, sections, user_access_level CASCADE;

CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TABLE users (
	user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255),
	last_name VARCHAR(255),
    password VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    type VARCHAR(50),
    domain_name VARCHAR
);

CREATE TABLE teams (
	team_id SERIAL PRIMARY KEY,
	team_name VARCHAR(255),
	team_slug VARCHAR(255),
	team_domain VARCHAR(255),
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE user_team_junction (
	user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
	team_id INTEGER REFERENCES teams(team_id) ON DELETE CASCADE,
	CONSTRAINT junction_id PRIMARY KEY (user_id, team_id)
);

CREATE TABLE user_access_level (
	user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
	team_id INTEGER REFERENCES teams(team_id) ON DELETE CASCADE,
	access_level VARCHAR(50),
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE comments (
	comment_id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users(user_id),
	content VARCHAR,
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE posts (
	post_id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users(user_id),
	title VARCHAR,
	body VARCHAR,
	mentions VARCHAR,
	tags VARCHAR,
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE reactions (
	reaction_id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users(user_id),
	reaction VARCHAR,
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE sections (
	section_id SERIAL PRIMARY KEY,
	team_id INTEGER REFERENCES teams(team_id),
	name VARCHAR,
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

DO $$
DECLARE
	table_ RECORD;
BEGIN
   	FOR table_ IN SELECT table_name FROM information_schema.tables WHERE table_schema='public' LOOP
		CREATE TRIGGER set_timestamp
		BEFORE UPDATE ON table_
		FOR EACH ROW
		EXECUTE PROCEDURE trigger_set_timestamp();
	END LOOP;
END;
$$ LANGUAGE plpgsql;