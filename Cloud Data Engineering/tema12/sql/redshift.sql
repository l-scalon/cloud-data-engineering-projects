CREATE TABLE Clients (
  clientID integer primary key DISTKEY,
  "type" varchar(7) not NULL,
  "name" varchar(255) not null
);

create table DocumentTypes (
	documentTypeID integer primary key,
	initials varchar(10) not null,
	fullName varchar(255) NOT null,
	"type" varchar(7) NOT null
);

CREATE TABLE Documents (
  clientID integer NOT NULL,
  documentTypeID integer NOT NULL,
  "number" decimal NOT NULL,
  PRIMARY KEY ("clientID", "documentTypeID"),
  unique ("documentTypeID", "number"),
  CONSTRAINT "Documents$clientID" FOREIGN KEY ("clientID") REFERENCES "Clients" ("clientID"),
  CONSTRAINT "Documents$documentTypeID" FOREIGN KEY ("documentTypeID") REFERENCES "DocumentTypes" ("documentTypeID")
);

create table TransactionTypes (
	typeID integer primary key distkey,
	nature varchar(7) not null,
	transactionType varchar(45)
);

CREATE TABLE Transactions (
  transactionID integer primary key DISTKEY,
  clientID integer NOT NULL,
  typeID integer NOT NULL,
  "time" timestamp NOT null SORTKEY,
  amount real NOT NULL,
  CONSTRAINT "Transactions$clientID" FOREIGN KEY ("clientID") REFERENCES "Clients" ("clientID"),
  CONSTRAINT "Transactions$typeID" FOREIGN KEY ("typeID") REFERENCES "TransactionTypes" ("typeID")
);

CREATE TABLE Transfers (
  transferID integer primary key DISTKEY,
  expense_transactionID integer DEFAULT NULL,
  income_transactionID integer DEFAULT NULL,
  CONSTRAINT Transfers$expense_transactionID FOREIGN KEY (expense_transactionID) REFERENCES Transactions (transactionID),
  CONSTRAINT Transfers$income_transactionID FOREIGN KEY (income_transactionID) REFERENCES Transactions (transactionID)
);

create table TaxType (
	taxTypeID integer primary key,
	typeID integer not null,
	rate real not null,
	CONSTRAINT "TaxType$typeID" FOREIGN KEY ("typeID") REFERENCES "TransactionTypes" ("typeID")
);

CREATE TABLE Tax (
  transactionID integer NOT null primary key,
  taxTypeID integer NOT NULL,
  fee real NOT NULL,
  CONSTRAINT "Tax$transactionID" FOREIGN KEY ("transactionID") REFERENCES "Transactions" ("transactionID"),
  CONSTRAINT "Tax$taxTypeID" FOREIGN KEY ("taxTypeID") REFERENCES "TaxType" ("taxTypeID")
);