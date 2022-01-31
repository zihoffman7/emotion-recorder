---- UNCOMMENT TO OVERRIDE ALL DATA ----
-- DROP TABLE IF EXISTS users;
-- DROP TABLE IF EXISTS logs;
---- END ----

-- All user data
CREATE TABLE IF NOT EXISTS users (
  username TEXT NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS logs (
  username TEXT NOT NULL,
  category VARCHAR(24) NOT NULL,
  value VARCHAR(100) NOT NULL,
  _time INT NOT NULL
);
