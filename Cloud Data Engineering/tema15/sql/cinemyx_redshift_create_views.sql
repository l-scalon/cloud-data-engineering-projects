CREATE VIEW cinemyx.tickets_by_channel AS 
SELECT bo.month, box_office, online
FROM 
	(SELECT EXTRACT(month FROM date) as month, COUNT(channel) AS box_office
    FROM cinemyx.purchase
    WHERE channel = 'box_office'
    GROUP BY 1) AS bo JOIN
    (SELECT EXTRACT(month FROM date) as month, COUNT(channel) AS online
    FROM cinemyx.purchase
    WHERE channel = 'online'
    GROUP BY 1) AS ol
ON bo.month = ol.month
GROUP BY 1, 2, 3;

CREATE VIEW cinemyx.movie_tickets_grossing AS 
SELECT
  screening.movieid, EXTRACT(month FROM screening.date) as month, COUNT(ticket.ticketid) AS tickets, SUM(ticket.price) AS grossing
FROM
  (cinemyx.screening
INNER JOIN cinemyx.ticket ON (screening.screeningid = ticket.screeningid))
GROUP BY 1, 2;

CREATE cinemyx.theater_by_tickets_grossing AS
SELECT
  screening.theaterid, EXTRACT(month FROM screening.date) as month, COUNT(ticket.ticketid) as tickets, SUM(ticket.price) AS grossing
FROM
  (cinemyx.screening screening
INNER JOIN cinemyx.ticket ticket ON (screening.screeningid = ticket.screeningid))
GROUP BY 1, 2;

CREATE VIEW cinemyx.ticket_by_category AS
SELECT
  categoryid, EXTRACT(month FROM screening.date) as month, COUNT(ticket.categoryid) AS tickets, AVG(ticket.price) AS average_price
FROM
  cinemyx.ticket JOIN cinemyx.screening ON ticket.screeningid = screening.screeningid
GROUP BY 1, 2;

CREATE VIEW cinemyx.ext_movie_tickets_grossing AS
(SELECT screening.movieid, screening.month, COUNT(ticket.ticketid) AS tickets, SUM(ticket.price) AS grossing
FROM (ext_cinemyx.screening INNER JOIN ext_cinemyx.ticket ON (screening.screeningid = ticket.screeningid))
WHERE CAST(screening.year AS int) = (DATE_PART(year, CURRENT_DATE) - 1)
AND CAST(screening.month AS int) BETWEEN 1 AND ((
  SELECT MAX(DATE_PART(month, screening.date)) FROM cinemyx.screening) - 1)
GROUP BY 1, 2
UNION
SELECT screening.movieid, screening.month, COUNT(ticket.ticketid) AS tickets, SUM(ticket.price) AS grossing
FROM (ext_cinemyx.screening INNER JOIN ext_cinemyx.ticket ON (screening.screeningid = ticket.screeningid))
WHERE CAST(screening.year AS int) = (DATE_PART(year, CURRENT_DATE) - 1)
AND CAST(screening.month AS int) = (SELECT MAX(DATE_PART(month, screening.date)) FROM cinemyx.screening)
AND CAST(screening.day AS int) BETWEEN 1 AND (
  SELECT MAX(DATE_PART(day, screening.date)) FROM cinemyx.screening
  WHERE DATE_PART(month, screening.date) = (SELECT MAX(DATE_PART(month, screening.date)) FROM cinemyx.screening))
GROUP BY 1, 2)
WITH NO SCHEMA BINDING

CREATE VIEW cinemyx.movie_tickets_grossing_overall AS
SELECT movie.movieid, movie.name, genre.genre, overall.year, overall.tickets, overall.grossing FROM
(SELECT movie.movieid, movie.name, movie.genreid FROM cinemyx.movie
 UNION
 SELECT movie.movieid, movie.name, movie.genreid FROM ext_cinemyx.movie) AS movie
JOIN
(SELECT 
	screening.movieid,
    EXTRACT(year from screening.date) as year,
    COUNT(ticket.ticketid) AS tickets,
    SUM(ticket.price) AS grossing
FROM
	cinemyx.screening
    JOIN cinemyx.ticket
    ON screening.screeningid = ticket.screeningid
GROUP BY 1, 2
UNION
SELECT 
	screening.movieid,
    CAST(screening.year AS int),
    COUNT(ticket.ticketid) AS tickets,
    SUM(ticket.price) AS grossing
FROM
	ext_cinemyx.screening
    JOIN ext_cinemyx.ticket
    ON screening.screeningid = ticket.screeningid
GROUP BY 1, 2) AS overall
ON movie.movieid = overall.movieid
JOIN cinemyx.genre ON
movie.genreid = genre.genreid
WITH NO SCHEMA BINDING