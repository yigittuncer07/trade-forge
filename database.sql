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
    Id INT,
    Name VARCHAR(255),
    Code VARCHAR(255)
);
INSERT INTO cryptos (Id, Name, Code) VALUES (1, 'Bitcoin', 'BTC');
INSERT INTO cryptos (Id, Name, Code) VALUES (1027, 'Ethereum', 'ETH');
INSERT INTO cryptos (Id, Name, Code) VALUES (328, 'Monero', 'XMR');
