CREATE DEFINER=`root`@`%` PROCEDURE `new_transfer`(IN source int, IN destination int, IN amount float, IN `type` VARCHAR(45), IN `time` VARCHAR(45))
BEGIN
	DECLARE transferS_last_id INT;

	INSERT INTO Transfers (transferID)
    VALUES (DEFAULT);
    
    SET transfers_last_id = LAST_INSERT_ID();
    
    CALL new_transaction_expense (source, amount, `type`, `time`);
    UPDATE Transfers
    SET expense_transactionID = LAST_INSERT_ID()
    WHERE transferID = transfers_last_id;
    
    CALL new_transaction_income (destination, amount, `type`, `time`);
	UPDATE Transfers
    SET income_transactionID = LAST_INSERT_ID()
    WHERE transferID = transfers_last_id;
END