-- This SQL runs automatically when the MySQL container first starts
CREATE DATABASE IF NOT EXISTS devops;
USE devops;

CREATE TABLE IF NOT EXISTS records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert a test record to verify everything works
INSERT INTO records (name, value) VALUES ('test', 'Hello from MySQL!');