DROP TABLE IF EXISTS users;
CREATE TABLE users (
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  PRIMARY KEY (username, password)
);

