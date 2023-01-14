DROP DATABASE IF EXISTS `cinemyx`;
CREATE DATABASE `cinemyx`;
USE `cinemyx`;

CREATE TABLE `category` (
  `categoryid` int NOT NULL AUTO_INCREMENT,
  `name` varchar(31) NOT NULL,
  `rate` decimal(3,2) NOT NULL,
  PRIMARY KEY (`categoryid`),
  UNIQUE KEY `categoryid` (`categoryid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `city` (
  `cityid` int NOT NULL AUTO_INCREMENT,
  `name` varchar(31) NOT NULL,
  PRIMARY KEY (`cityid`),
  UNIQUE KEY `cityid` (`cityid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `genre` (
  `genreid` int NOT NULL AUTO_INCREMENT,
  `genre` varchar(31) NOT NULL,
  PRIMARY KEY (`genreid`),
  UNIQUE KEY `genreid` (`genreid`),
  UNIQUE KEY `genre` (`genre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `movie` (
  `movieid` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `runningtime` int NOT NULL,
  `genreid` int NOT NULL,
  `firstscreening` datetime NOT NULL,
  `lastscreening` datetime NOT NULL,
  PRIMARY KEY (`movieid`),
  UNIQUE KEY `movieid` (`movieid`),
  KEY `movie$genreid` (`genreid`),
  CONSTRAINT `movie$genreid` FOREIGN KEY (`genreid`) REFERENCES `genre` (`genreid`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `purchase` (
  `purchaseid` int NOT NULL AUTO_INCREMENT,
  `tickets` int NOT NULL,
  `total` decimal(5,2) NOT NULL,
  `channel` varchar(10) NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`purchaseid`),
  UNIQUE KEY `purchaseid` (`purchaseid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `venue` (
  `venueid` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `cityid` int NOT NULL,
  `theaters` int NOT NULL,
  PRIMARY KEY (`venueid`),
  UNIQUE KEY `venueid` (`venueid`),
  KEY `venue$cityid` (`cityid`),
  CONSTRAINT `venue$cityid` FOREIGN KEY (`cityid`) REFERENCES `city` (`cityid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `theater` (
  `theaterid` int NOT NULL AUTO_INCREMENT,
  `venueid` int NOT NULL,
  `seats` int NOT NULL,
  `rate` decimal(3,2) NOT NULL,
  PRIMARY KEY (`theaterid`),
  UNIQUE KEY `theaterid` (`theaterid`),
  KEY `theater$venueid` (`venueid`),
  CONSTRAINT `theater$venueid` FOREIGN KEY (`venueid`) REFERENCES `venue` (`venueid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `screening` (
  `screeningid` int NOT NULL AUTO_INCREMENT,
  `movieid` int NOT NULL,
  `theaterid` int NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`screeningid`),
  UNIQUE KEY `screeningid` (`screeningid`),
  KEY `screening$movieid` (`movieid`),
  KEY `screening$theaterid` (`theaterid`),
  CONSTRAINT `screening$movieid` FOREIGN KEY (`movieid`) REFERENCES `movie` (`movieid`),
  CONSTRAINT `screening$theaterid` FOREIGN KEY (`theaterid`) REFERENCES `theater` (`theaterid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `ticket` (
  `ticketid` int NOT NULL AUTO_INCREMENT,
  `screeningid` int NOT NULL,
  `categoryid` int NOT NULL,
  `purchaseid` int NOT NULL,
  `price` decimal(4,2) NOT NULL,
  `seat` int NOT NULL,
  PRIMARY KEY (`ticketid`),
  UNIQUE KEY `ticketid` (`ticketid`),
  KEY `ticket$screeningid` (`screeningid`),
  KEY `ticket$categoryid` (`categoryid`),
  KEY `ticket$purchaseid` (`purchaseid`),
  CONSTRAINT `ticket$categoryid` FOREIGN KEY (`categoryid`) REFERENCES `category` (`categoryid`),
  CONSTRAINT `ticket$purchaseid` FOREIGN KEY (`purchaseid`) REFERENCES `purchase` (`purchaseid`),
  CONSTRAINT `ticket$screeningid` FOREIGN KEY (`screeningid`) REFERENCES `screening` (`screeningid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;