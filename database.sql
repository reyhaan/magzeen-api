CREATE TABLE users (
	user_id serial PRIMARY KEY,
    first_name VARCHAR,
	last_name VARCHAR,
    password VARCHAR NOT NULL,
	email VARCHAR NOT NULL,
    created_at DATE,
	updated_at DATE,
    type VARCHAR,
    domain_name VARCHAR,
	team_id INT,
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);

CREATE TABLE teams (
	team_id serial PRIMARY_KEY,
	team_name VARCHAR,
	team_slug VARCHAR,
	team_domain VARCHAR
);

CREATE TABLE user_access_level (

);

CREATE TABLE comments (

);

CREATE TABLE posts (

);

CREATE TABLE reactions (

);

CREATE TABLE sections (
	
);