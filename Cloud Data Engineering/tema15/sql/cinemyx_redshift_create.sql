DROP SCHEMA IF EXISTS cinemyx CASCADE;
CREATE SCHEMA cinemyx;

CREATE TABLE dev.cinemyx.purchase (
    purchaseid integer PRIMARY KEY DISTKEY,
    tickets integer NOT NULL,
    total decimal(6, 2) NOT NULL,
    channel varchar(10) NOT NULL,
    "date" timestamp NOT NULL SORTKEY
);

CREATE TABLE dev.cinemyx.genre (
    genreid integer PRIMARY KEY,
    genre varchar(31) NOT NULL
);

CREATE TABLE dev.cinemyx.movie (
    movieid integer PRIMARY KEY,
    "name" varchar(255) NOT NULL,
    runningtime integer NOT NULL,
    genreid integer NOT NULL,
    firstscreening timestamp NOT NULL SORTKEY,
    lastscreening timestamp NOT NULL,
    CONSTRAINT movie$genreid FOREIGN KEY (genreid) REFERENCES cinemyx.genre (genreid)
);

CREATE TABLE dev.cinemyx.city (
    cityid integer NOT NULL PRIMARY KEY,
    "name" varchar(31)
);

CREATE TABLE dev.cinemyx.venue (
    venueid integer NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL,
    cityid integer NOT NULL,
    theaters integer NOT NULL,
    CONSTRAINT venue$cityid FOREIGN KEY (cityid) REFERENCES cinemyx.city (cityid)
);

CREATE TABLE dev.cinemyx.theater (
    theaterid integer PRIMARY KEY,
    venueid integer NOT NULL,
    seats integer NOT NULL,
    rate decimal(3, 2) NOT NULL,
    CONSTRAINT theater$venueid FOREIGN KEY (venueid) REFERENCES cinemyx.venue (venueid)
);

CREATE TABLE dev.cinemyx.screening (
    screeningid integer PRIMARY KEY,
    movieid integer NOT NULL,
    theaterid integer NOT NULL,
    "date" timestamp SORTKEY NOT NULL,
    CONSTRAINT screening$movieid FOREIGN KEY (movieid) REFERENCES cinemyx.movie (movieid),
    CONSTRAINT screening$theaterid FOREIGN KEY (theaterid) REFERENCES cinemyx.theater (theaterid)
);

CREATE TABLE dev.cinemyx.category (
    categoryid integer PRIMARY KEY,
    "name" varchar(31) NOT NULL,
    rate decimal(3, 2) NOT NULL
);

CREATE TABLE dev.cinemyx.ticket (
    ticketid integer PRIMARY KEY,
    screeningid integer NOT NULL,
    categoryid integer NOT NULL,
    purchaseid integer NOT NULL,
    price decimal(6, 2) NOT NULL,
    seat integer NOT NULL,
    CONSTRAINT ticket$screeningid FOREIGN KEY (screeningid) REFERENCES cinemyx.screening (screeningid),
    CONSTRAINT ticket$categoryid FOREIGN KEY (categoryid) REFERENCES cinemyx.category (categoryid),
    CONSTRAINT ticket$purchaseid FOREIGN KEY (purchaseid) REFERENCES cinemyx.purchase (purchaseid)
);

DROP SCHEMA IF EXISTS ext_cinemyx;
CREATE EXTERNAL SCHEMA ext_cinemyx FROM data catalog 
DATABASE 'cinemyx' 
iam_role DEFAULT
CREATE EXTERNAL DATABASE IF NOT EXISTS;