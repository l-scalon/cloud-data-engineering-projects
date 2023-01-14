CREATE DEFINER=`root`@`%` PROCEDURE `new_transaction_income`(IN clientID int, IN amount float)
BEGIN
	DECLARE rate FLOAT;
	DECLARE fee  FLOAT;
    
	INSERT INTO Transactions (clientID, nature, amount)
		VALUES (clientID, 'income', amount);
        
	SET rate = tax_rate ('income', amount);
    SET fee  = tax_fee  (amount, rate);
        
	INSERT INTO Tax (transactionID, rate, fee)
		VALUES (LAST_INSERT_ID(), rate, fee);
END