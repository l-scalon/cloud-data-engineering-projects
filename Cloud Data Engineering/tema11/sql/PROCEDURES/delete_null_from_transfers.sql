CREATE PROCEDURE `delete_null_from_transfers` ()
BEGIN
	DELETE FROM Transfers 
	WHERE expense_transactionID IS NULL AND income_transactionID IS NULL;
END
