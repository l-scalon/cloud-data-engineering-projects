-- contabyx.Balance source

-- contabyx.Balance2 source

-- contabyx.Balance source

CREATE VIEW contabyx.Balance ([Client], [Balance])
AS

SELECT TOP (9223372036854775807)
	clientID AS Client,
	ROUND(SUM(CASE WHEN nature = 'expense' THEN -1 ELSE 1 END * amount), 2) AS Amount
FROM contabyx.Transactions
GROUP BY clientID
ORDER BY clientID ASC;


-- contabyx.Transaction_History source

-- contabyx.Transaction_History source

CREATE VIEW contabyx.Transaction_History2
AS 

SELECT TOP (9223372036854775807)
	clientID,
	transactionID AS [Transaction],
	time AS Time,
	ROUND(CASE WHEN nature = 'expense' THEN -1 ELSE 1 END * amount, 2) AS Movement
FROM contabyx.Transactions
ORDER BY clientID;


-- contabyx.Transfer_Aux_Expense source

CREATE VIEW contabyx.Transfer_Aux_Expense ([transferID], [From], [Movement])
AS 
   SELECT Transfers.transferID AS transferID, Transactions.clientID AS [From], Transactions.amount AS Movement
   FROM (contabyx.Transactions 
      INNER JOIN contabyx.Transfers 
      ON ((Transactions.transactionID = Transfers.expense_transactionID)));


-- contabyx.Transfer_Aux_Income source

CREATE VIEW contabyx.Transfer_Aux_Income ([transferID], [To], [Movement])
AS 
   SELECT Transfers.transferID AS transferID, Transactions.clientID AS [To], Transactions.amount AS Movement
   FROM (contabyx.Transactions 
      INNER JOIN contabyx.Transfers 
      ON ((Transactions.transactionID = Transfers.income_transactionID)));


-- contabyx.Transfer_History source

CREATE VIEW contabyx.Transfer_History (
   [Transfer], 
   [From], 
   [To], 
   [Movement])
AS 
   SELECT Transfer_Aux_Expense.transferID AS Transfer, Transfer_Aux_Expense.[From] AS [From], Transfer_Aux_Income.[To] AS [To], Transfer_Aux_Expense.Movement AS Movement
   FROM (contabyx.Transfer_Aux_Expense 
      INNER JOIN contabyx.Transfer_Aux_Income 
      ON ((Transfer_Aux_Expense.transferID = Transfer_Aux_Income.transferID)));


-- contabyx.Transfer_income_where_expense_is_null source

CREATE VIEW contabyx.transfer_income_where_expense_is_null AS

      SELECT income_transactionID
      FROM contabyx.Transfers
      WHERE expense_transactionID IS NULL;