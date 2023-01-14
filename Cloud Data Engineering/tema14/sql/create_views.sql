CREATE VIEW contabyx.clients_info AS
SELECT 
	contabyx.spectrum_transactions.clientID,
	ROUND(SUM(CASE WHEN contabyx.transactiontypes.nature = 'income' THEN contabyx.spectrum_transactions.amount
		ELSE contabyx.spectrum_transactions.amount * -1 END ), 2)::decimal(10,2) as balance,
	SUM(CASE WHEN contabyx.transactiontypes.nature = 'income' THEN 1 ELSE 0 END) as total_income,
	SUM(CASE WHEN contabyx.transactiontypes.nature = 'expense' THEN 1 ELSE 0 END) as total_expense
FROM contabyx.spectrum_transactions JOIN contabyx.transactiontypes
ON contabyx.spectrum_transactions.typeid = Transactiontypes.typeid
GROUP BY contabyx.spectrum_transactions.clientid
WITH NO SCHEMA BINDING;

CREATE VIEW contabyx.clients_info_by_month AS
SELECT 
	contabyx.spectrum_transactions.clientID,
	extract(year from contabyx.spectrum_transactions.time) as year,
    extract(month from contabyx.spectrum_transactions.time) as month,
	SUM(CASE WHEN contabyx.transactiontypes.nature = 'income' THEN 1 ELSE 0 END) as income,
	SUM(CASE WHEN contabyx.transactiontypes.nature = 'expense' THEN 1 ELSE 0 END) as expense
FROM contabyx.spectrum_transactions JOIN contabyx.transactiontypes
ON contabyx.spectrum_transactions.typeid = Transactiontypes.typeid
GROUP BY contabyx.spectrum_transactions.clientid, year, month
WITH NO SCHEMA BINDING;