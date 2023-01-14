CREATE DEFINER=`root`@`%` PROCEDURE `new_document`(IN clientID int, IN document VARCHAR(45), IN number bigint UNSIGNED)
BEGIN
	INSERT INTO Documents (clientID, `type`, `number`)
		VALUES (clientID, document, number);
END