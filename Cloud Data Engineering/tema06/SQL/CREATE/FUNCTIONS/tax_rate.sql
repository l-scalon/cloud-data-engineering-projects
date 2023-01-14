CREATE DEFINER=`root`@`%` FUNCTION `tax_rate`(nature ENUM('income', 'expense'), amount float) RETURNS float
    DETERMINISTIC
BEGIN
	DECLARE rate FLOAT;
    SET rate = 0;
    
	IF nature = 'income' THEN
		IF (amount >= 1000 AND amount < 5000) THEN
			SET rate = 0.005;
		ELSEIF (amount >= 5000 AND amount < 9000) THEN
			SET rate = 0.007;
		ELSEIF (amount >= 9000 AND amount < 11000) THEN
			SET rate = 0.009;
		ELSEIF amount >= 11000 THEN
			SET rate = 0.011;
		END IF;
	ELSE
		IF (amount >= 5000 AND amount < 9000) THEN
			SET rate = 0.005;
		ELSEIF (amount >= 9000 AND amount < 11000) THEN
			SET rate = 0.007;
		ELSEIF amount >= 11000 THEN
			SET rate = 0.009;
		END IF;
	END IF;
RETURN rate;
END