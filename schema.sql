CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, created_at TIMESTAMP);
CREATE TABLE subforums (id SERIAL PRIMARY KEY, title TEXT, content TEXT, category TEXT, followers INTEGER, created_at TIMESTAMP, user_id INTEGER REFERENCES users);
CREATE TABLE discussions (id SERIAL PRIMARY KEY, title TEXT, content TEXT, created_at TIMESTAMP, subforum_id INTEGER REFERENCES subforums, user_id INTEGER REFERENCES users);
CREATE TABLE comments (id SERIAL PRIMARY KEY, content TEXT, created_at TIMESTAMP, discussion_id INTEGER REFERENCES discussions, comment_id INTEGER REFERENCES comments, user_id INTEGER REFERENCES users);
CREATE TABLE tags (id SERIAL PRIMARY KEY, tag TEXT, subforum INTEGER REFERENCES subforums)
CREATE TABLE friends (id SERIAL PRIMARY KEY, user1 INTEGER REFERENCES users, user2 INTEGER REFERENCES users)
CREATE TABLE interests (id SERIAL PRIMARY KEY, interest TEXT, user INTEGER REFERENCES users)