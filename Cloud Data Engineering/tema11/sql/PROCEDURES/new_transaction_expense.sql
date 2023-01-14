CREATE DEFINER=`root`@`%` PROCEDURE `new_transaction_expense`(IN clientID int, IN amount float, IN `type` VARCHAR(45), IN `time` VARCHAR(45))
BEGIN
	DECLARE rate FLOAT;
	DECLARE fee  FLOAT;
    DECLARE `datetime` DATETIME;
    
    SET `datetime` = CAST(`time` AS DATETIME);
    
	INSERT INTO Transactions (clientID, nature, amount, `time`)
		VALUES (clientID, 'expense', amount, `datetime`);
        
	SET rate = tax_rate ('expense', amount);
    SET fee  = tax_fee  (amount, rate);
        
	INSERT INTO Tax (transactionID, rate, fee)
		VALUES (LAST_INSERT_ID(), rate, fee);
        
	INSERT INTO TransactionTypes (transactionID, transaction_type)
		VALUES (LAST_INSERT_ID(), `type`);
END