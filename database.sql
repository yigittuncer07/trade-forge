CREATE DATABASE IF NOT EXISTS tradeforge;

USE tradeforge;

CREATE TABLE IF NOT EXISTS Users (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    UserName VARCHAR(50),
    PasswordHash VARCHAR(256),
    Email VARCHAR(100),
    SocialId VARCHAR(20)
);

use tradeforge;

CREATE TABLE cryptos (
    Id INT PRIMARY KEY,
    Name VARCHAR(255),
    Code VARCHAR(255)
);
INSERT INTO cryptos (Id, Name, Code) VALUES (1, 'Bitcoin', 'BTC');
INSERT INTO cryptos (Id, Name, Code) VALUES (1027, 'Ethereum', 'ETH');
INSERT INTO cryptos (Id, Name, Code) VALUES (328, 'Monero', 'XMR');


CREATE TABLE assets (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    UserId INT,
    CryptoId INT,
    Amount DECIMAL(18, 8),
    FOREIGN KEY (UserId) REFERENCES users(Id),
    FOREIGN KEY (CryptoId) REFERENCES cryptos(Id)
);


INSERT INTO assets (UserId, CryptoId, Amount) VALUES (22, 1, 12.5);
INSERT INTO assets (UserId, CryptoId, Amount) VALUES (22, 1027, 50);
INSERT INTO assets (UserId, CryptoId, Amount) VALUES (22, 328, 10);
