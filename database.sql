CREATE DATABASE IF NOT EXISTS tradeforge;

USE tradeforge;

CREATE TABLE IF NOT EXISTS Users (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    UserName VARCHAR(50),
    PasswordHash VARCHAR(256),
    Email VARCHAR(100),
    SocialId VARCHAR(20)
);

 
CREATE TABLE cryptos (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255)
);

INSERT INTO cryptos (Name) VALUES ('Bitcoin'), ('Ethereum'), ('Monero');
