UNLOAD ('SELECT movieid, name, runningtime, genreid, firstscreening, lastscreening,
	EXTRACT (year from lastscreening) as year,
        EXTRACT (month from lastscreening) as month,
	EXTRACT (month from lastscreening) as day
		FROM cinemyx.movie
		WHERE DATE_PART(year, lastscreening) != DATE_PART(year, CURRENT_DATE)')
TO 's3://<BUCKET>/parquet/<KEY>/movie/'
iam_role DEFAULT
FORMAT AS PARQUET
PARTITION BY (year, month, day)
ALLOWOVERWRITE;

UNLOAD ('SELECT screeningid, movieid, theaterid, date,
	EXTRACT (year from date) as year,
        EXTRACT (month from date) as month,
        EXTRACT (day from date) as day
		FROM cinemyx.screening
		WHERE DATE_PART(year, date) != DATE_PART(year, CURRENT_DATE)')
TO 's3://<BUCKET>/parquet/<KEY>/screening/'
iam_role DEFAULT
FORMAT AS PARQUET
PARTITION BY (year, month, day)
ALLOWOVERWRITE;

UNLOAD ('SELECT purchaseid, tickets, total, channel, date,
	EXTRACT (year from date) as year,
        EXTRACT (month from date) as month,
        EXTRACT (day from date) as day
		FROM cinemyx.purchase
		WHERE DATE_PART(year, date) != DATE_PART(year, CURRENT_DATE)')
TO 's3://<BUCKET>/parquet/<KEY>/purchase'
iam_role DEFAULT
FORMAT AS PARQUET
PARTITION BY (year, month, day)
ALLOWOVERWRITE;

UNLOAD ('SELECT ticketid, ticket.screeningid as screeningid, categoryid, purchaseid, price, seat, date as screening_date,
	EXTRACT (year from screening.date) as year,
        EXTRACT (month from screening.date) as month,
        EXTRACT (day from screening.date) as day
		FROM cinemyx.ticket JOIN cinemyx.screening
		ON ticket.screeningid = screening.screeningid
		WHERE DATE_PART(year, screening.date) != DATE_PART(year, CURRENT_DATE);')
TO 's3://<BUCKET>/parquet/<KEY>/ticket'
iam_role DEFAULT
FORMAT AS PARQUET
PARTITION BY (year, month, day)
ALLOWOVERWRITE;

DELETE FROM cinemyx.movie WHERE DATE_PART(year, lastscreening) != DATE_PART(year, CURRENT_DATE)

DELETE FROM cinemyx.screening WHERE DATE_PART(year, date) != DATE_PART(year, CURRENT_DATE)

DELETE FROM cinemyx.purchase WHERE DATE_PART(year, date) != DATE_PART(year, CURRENT_DATE)

DELETE FROM cinemyx.ticket 
WHERE screeningid NOT IN (SELECT screeningid FROM cinemyx.screening)