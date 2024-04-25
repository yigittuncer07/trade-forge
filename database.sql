CREATE DATABASE IF NOT EXISTS tradeforge;

USE tradeforge;

CREATE TABLE IF NOT EXISTS Users (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    UserName VARCHAR(50),
    PasswordHash VARCHAR(256),
    Email VARCHAR(100),
    SocialId VARCHAR(20)
);

 
USE tradeforge;

-- Inserting user data
INSERT INTO Users (UserName, UserSurname, PasswordHash, Email, SocialId) 
VALUES 
('John', 'Doe', 'd30318c3c2311ac757c0b740a14957fe', 'john@example.com', '12A3B4R5F6'),
('Alice', 'Smith', '082949a8dfacccda185a135db425377b', 'alice@example.com', '65D432DSA1'),
('Bob', 'Johnson', '583317fe343d4ecca20295776885a929', 'bob@example.com', '9W7E65UR4');
