CREATE TABLE users (id SERIAL PRIMARY KEY, item_type TEXT, username TEXT UNIQUE, password TEXT, created_at TIMESTAMP, is_admin BOOLEAN, visible BOOLEAN);
CREATE TABLE subforums (id SERIAL PRIMARY KEY, item_type TEXT, title TEXT, content TEXT, category TEXT, followers INTEGER, created_at TIMESTAMP, user_id INTEGER REFERENCES users, visible BOOLEAN);
CREATE TABLE discussions (id SERIAL PRIMARY KEY, item_type TEXT, title TEXT, content TEXT, created_at TIMESTAMP, subforum_id INTEGER REFERENCES subforums, user_id INTEGER REFERENCES users, visible BOOLEAN);
CREATE TABLE comments (id SERIAL PRIMARY KEY, item_type TEXT, content TEXT, created_at TIMESTAMP, discussion_id INTEGER REFERENCES discussions, comment_id INTEGER REFERENCES comments, user_id INTEGER REFERENCES users, visible BOOLEAN);
CREATE TABLE tags (id SERIAL PRIMARY KEY, tag TEXT, subforum INTEGER REFERENCES subforums);
CREATE TABLE follows_user (id SERIAL PRIMARY KEY, user_id1 INTEGER REFERENCES users, user_id2 INTEGER REFERENCES users, visible BOOLEAN);
CREATE TABLE follows_subforum (id SERIAL PRIMARY KEY, subforum_id INTEGER REFERENCES subforums, user_id INTEGER REFERENCES users, visible BOOLEAN);
CREATE TABLE interests (id SERIAL PRIMARY KEY, interest TEXT, user_id INTEGER REFERENCES users);