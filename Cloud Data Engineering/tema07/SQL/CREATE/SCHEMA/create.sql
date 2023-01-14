DROP DATABASE IF EXISTS contabyx;
CREATE DATABASE IF NOT EXISTS contabyx
DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE contabyx;

CREATE TABLE Clients (
	clientID int NOT NULL AUTO_INCREMENT,
    `type` ENUM('natural', 'legal') NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    PRIMARY KEY (clientID)
);

CREATE TABLE Documents (
	clientID int NOT NULL,
	`type` VARCHAR(45) NOT NULL,
    `number` bigint UNSIGNED NOT NULL,
    CONSTRAINT documents_clientID 
		FOREIGN KEY (clientID) 
        REFERENCES Clients (clientID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    PRIMARY KEY (clientID, `type`)
);

CREATE TABLE Transactions (
	transactionID int NOT NULL AUTO_INCREMENT,
    clientID int NOT NULL,
    nature ENUM('income', 'expense') NOT NULL,
    `time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    amount float NOT NULL,
    CONSTRAINT amount CHECK (amount > 0),
    CONSTRAINT transaction_clientID 
		FOREIGN KEY (clientID) 
        REFERENCES Clients (clientID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
	PRIMARY KEY (transactionID)
);

CREATE TABLE Transfers (
	transferID int NOT NULL AUTO_INCREMENT,
    expense_transactionID int,
    income_transactionID int,
    CONSTRAINT expense_transactionID
		FOREIGN KEY (expense_transactionID)
        REFERENCES Transactions (transactionID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
	CONSTRAINT income_transactionID
		FOREIGN KEY (income_transactionID)
        REFERENCES Transactions (transactionID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
	PRIMARY KEY (transferID)
);

CREATE TABLE Tax (
	transactionID int NOT NULL,
    rate float NOT NULL,
    fee float NOT NULL,
    CONSTRAINT percentage CHECK (rate BETWEEN 0 AND 1),
    CONSTRAINT transactionID
		FOREIGN KEY (transactionID)
        REFERENCES Transactions (transactionID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
	PRIMARY KEY (transactionID)
);