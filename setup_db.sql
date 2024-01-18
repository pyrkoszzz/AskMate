CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(500)
);

INSERT INTO users (username, password) VALUES
    ('john_doe', 'password123'),
    ('jane_smith', 'letmein'),
    ('bob_jones', 'secret');

CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT current_timestamp
);

INSERT INTO questions (title, content, user_id) VALUES
    ('How to use Python?', 'I am new to Python. Can someone guide me on how to get started?', 1),
    ('Favorite programming language?', 'What is your favorite programming language and why?', 2),
    ('Database design tips?', 'Any tips for designing efficient and scalable databases?', 3);


CREATE TABLE IF NOT EXISTS answers (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users(id),
    question_id INTEGER REFERENCES questions(id),
    created_at TIMESTAMP DEFAULT current_timestamp
);

INSERT INTO answers (content, user_id, question_id) VALUES
    ('Start with the official Python documentation. Its a great resource!', 2, 1),
    ('I love Python because of its readability and versatility.', 1, 2),
    ('Ensure to normalize your database and use indexes for better performance.', 3, 3);