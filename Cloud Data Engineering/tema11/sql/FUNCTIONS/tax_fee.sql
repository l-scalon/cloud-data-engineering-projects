CREATE DEFINER=`root`@`%` FUNCTION `tax_fee`(rate float, amount float) RETURNS float
    DETERMINISTIC
BEGIN
	DECLARE fee FLOAT;
    
    SET fee = rate * amount;
RETURN fee;
END