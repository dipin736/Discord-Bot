"""
CREATE DATABASE discord_bot;
USE discord_bot;

CREATE TABLE auth_tokens (
    server_id BIGINT PRIMARY KEY,
    bot_token VARCHAR(255) NOT NULL
);


INSERT INTO auth_tokens (server_id, bot_token) VALUES ("your_server_id", 'your_token');

"""