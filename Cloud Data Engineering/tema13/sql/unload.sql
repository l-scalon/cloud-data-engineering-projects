UNLOAD ('SELECT *, extract(year from time) as year FROM contabyx.transactions WHERE DATE_PART(year, time) != DATE_PART(year, CURRENT_DATE)')
TO 's3://<BUCKET>/<KEY>/contabyx-parquet/transactions/'
iam_role DEFAULT
FORMAT AS PARQUET
PARTITION BY (year)
ALLOWOVERWRITE;

UNLOAD ('SELECT transfers.transferid, transfers.expense_transactionid, transfers.income_transactionid, extract(year from transactions.time) as year FROM contabyx.transfers
JOIN contabyx.transactions ON
transfers.expense_transactionid = transactions.transactionid
WHERE expense_transactionid
IN (SELECT transactionID FROM contabyx.transactions WHERE DATE_PART(year, time) != DATE_PART(year, CURRENT_DATE))')
TO 's3://<BUCKET>/<KEY>/contabyx-parquet/transfers/'
iam_role DEFAULT
FORMAT AS PARQUET
PARTITION BY (year)
ALLOWOVERWRITE;

UNLOAD ('SELECT tax.transactionid, tax.taxtypeid, tax.fee, extract(year from transactions.time) as year FROM contabyx.tax
JOIN contabyx.transactions ON
tax.transactionid = transactions.transactionid
WHERE tax.transactionID IN
(SELECT transactionID FROM contabyx.transactions WHERE DATE_PART(year, time) != DATE_PART(year, CURRENT_DATE))')
TO 's3://<BUCKET>/<KEY>/contabyx-parquet/tax/'
iam_role DEFAULT
FORMAT AS PARQUET
PARTITION BY (year)
ALLOWOVERWRITE;

DELETE FROM contabyx.tax 
WHERE transactionID IN
(SELECT transactionID FROM contabyx.transactions WHERE DATE_PART(year, time) != DATE_PART(year, CURRENT_DATE));

DELETE FROM contabyx.transfers
WHERE expense_transactionid
IN (SELECT transactionID FROM contabyx.transactions WHERE DATE_PART(year, time) != DATE_PART(year, CURRENT_DATE));

DELETE FROM contabyx.transactions 
WHERE DATE_PART(year, time) != DATE_PART(year, CURRENT_DATE);