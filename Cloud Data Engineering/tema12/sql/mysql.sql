CREATE DATABASE IF NOT EXISTS `contabyx`

CREATE TABLE `Clients` (
  `clientID` int NOT NULL AUTO_INCREMENT,
  `type` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`clientID`),
  UNIQUE KEY `clientID` (`clientID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

create table DocumentTypes (
	documentTypeID int NOT NULL AUTO_INCREMENT UNIQUE,
	initials varchar(10) not null,
	fullName varchar(255) NOT null,
	`type` varchar(7) NOT null
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Documents` (
  `clientID` int NOT NULL,
  `documentTypeID` int NOT NULL,
  `number` bigint NOT NULL,
  PRIMARY KEY (`clientID`,`documentTypeID`),
  unique (`documentTypeID`, `number`),
  CONSTRAINT `Documents$documents_clientID` FOREIGN KEY (`clientID`) REFERENCES `Clients` (`clientID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Documents$documents_documentTypeID` FOREIGN KEY (`documentTypeID`) REFERENCES `DocumentTypes` (`documentTypeID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `TransactionTypes` (
  typeID int NOT NULL AUTO_INCREMENT UNIQUE,
  nature varchar(7) not null,
  transactionType varchar(45) NOT NULL,
  PRIMARY KEY (`typeID`),
  UNIQUE (`nature`, `transactionType`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Transactions` (
  `transactionID` int NOT NULL AUTO_INCREMENT UNIQUE,
  `clientID` int NOT NULL,
  `typeID` int NOT NULL,
  `time` datetime(6) NOT NULL,
  `amount` float NOT NULL,
  PRIMARY KEY (`transactionID`),
  KEY `transaction_clientID` (`clientID`),
  CONSTRAINT `Transactions$transaction_clientID` FOREIGN KEY (`clientID`) REFERENCES `Clients` (`clientID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Transactions$transaction_typeID` FOREIGN KEY (`typeID`) REFERENCES `TransactionTypes` (`typeID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Transfers` (
  `transferID` int NOT NULL AUTO_INCREMENT,
  `expense_transactionID` int DEFAULT NULL,
  `income_transactionID` int DEFAULT NULL,
  PRIMARY KEY (`transferID`),
  UNIQUE KEY `transferID` (`transferID`),
  KEY `expense_transactionID` (`expense_transactionID`),
  KEY `income_transactionID` (`income_transactionID`),
  CONSTRAINT `Transfers$expense_transactionID` FOREIGN KEY (`expense_transactionID`) REFERENCES `Transactions` (`transactionID`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `Transfers$income_transactionID` FOREIGN KEY (`income_transactionID`) REFERENCES `Transactions` (`transactionID`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

create table TaxType (
	taxTypeID int NOT NULL AUTO_INCREMENT UNIQUE,
	typeID int not null,
	rate float not null,
	PRIMARY KEY (`taxTypeID`),
	CONSTRAINT `TaxType$typeID` FOREIGN KEY (`typeID`) REFERENCES `TransactionTypes` (`typeID`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Tax (
  transactionID int NOT null,
  taxTypeID int NOT NULL,
  fee float NOT NULL,
  PRIMARY KEY (`transactionID`),
  CONSTRAINT `Tax$transactionID` FOREIGN KEY (`transactionID`) REFERENCES `Transactions` (`transactionID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Tax$taxTypeID` FOREIGN KEY (`taxTypeID`) REFERENCES `TaxType` (`taxTypeID`) ON DELETE CASCADE ON UPDATE CASCADE
);