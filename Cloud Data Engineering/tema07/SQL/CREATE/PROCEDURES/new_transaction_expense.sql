CREATE DEFINER=`root`@`%` PROCEDURE `new_transaction_expense`(IN clientID int, IN amount float)
BEGIN
	DECLARE rate FLOAT;
	DECLARE fee  FLOAT;
    
	INSERT INTO Transactions (clientID, nature, amount)
		VALUES (clientID, 'expense', amount);
        
	SET rate = tax_rate ('expense', amount);
    SET fee  = tax_fee  (amount, rate);
        
	INSERT INTO Tax (transactionID, rate, fee)
		VALUES (LAST_INSERT_ID(), rate, fee);
END