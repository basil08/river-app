DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS user_detail;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS comment;

CREATE TABLE user_detail (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  posts TEXT,
  followers TEXT,
  verified BOOLEAN DEFAULT FALSE,
  is_premium BOOLEAN DEFAULT FALSE,
  email_id TEXT NOT NULL,
  bio TEXT,
  pfp BLOB,
  relationship_status TEXT,
  location TEXT,
  joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE post (
  post_id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  title TEXT,
  body TEXT NOT NULL,
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  likes INTEGER,
  is_reported BOOLEAN,
  is_blocked BOOLEAN,
  FOREIGN KEY (author_id) REFERENCES user_detail (user_id)
);

CREATE TABLE comment (
  comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  post_id INTEGER NOT NULL,
  title TEXT,
  body TEXT NOT NULL,
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  likes INTEGER,
  FOREIGN KEY (author_id) REFERENCES user_detail (user_id),
  FOREIGN KEY (post_id) REFERENCES post (post_id)
);