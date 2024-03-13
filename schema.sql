DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS posts;


CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    start_time DATETIME,
    end_time DATETIME,
    arranger INTEGER,
    picture TEXT,
    category TEXT,
    nationcard INTEGER CHECK (nationcard IN (0, 1)),
    FOREIGN KEY (arranger) REFERENCES users(id)
);


CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active INTEGER CHECK (is_active IN (0, 1)) DEFAULT 1,
    role TEXT
);
