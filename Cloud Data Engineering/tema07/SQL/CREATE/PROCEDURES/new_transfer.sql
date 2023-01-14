CREATE DEFINER=`root`@`%` PROCEDURE `new_transfer`(IN source int, IN destination int, IN amount float)
BEGIN
	DECLARE transferS_last_id INT;

	INSERT INTO Transfers (transferID)
    VALUES (DEFAULT);
    
    SET transfers_last_id = LAST_INSERT_ID();
    
    CALL new_transaction_expense (source, amount);
    UPDATE Transfers
    SET expense_transactionID = LAST_INSERT_ID()
    WHERE transferID = transfers_last_id;
    
    CALL new_transaction_income (destination, amount);
	UPDATE Transfers
    SET income_transactionID = LAST_INSERT_ID()
    WHERE transferID = transfers_last_id;
END