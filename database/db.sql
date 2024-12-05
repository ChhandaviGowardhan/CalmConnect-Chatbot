create database calmconnect;
use calmconnect;
-- Create the 'users' table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create the 'diagnosis' table
CREATE TABLE diagnosis (
    user_id INT NOT NULL AUTO_INCREMENT,
    diagnosis VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);

