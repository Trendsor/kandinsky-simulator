-- Create a superuser
CREATE ROLE admin WITH LOGIN SUPERUSER PASSWORD 'password';

-- Create additional roles or databases if needed
CREATE DATABASE trading_bot;
GRANT ALL PRIVILEGES ON DATABASE trading_bot TO admin;
