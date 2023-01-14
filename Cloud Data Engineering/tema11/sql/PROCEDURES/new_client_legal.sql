CREATE DEFINER=`root`@`%` PROCEDURE `new_client_legal`(IN name VARCHAR(255), IN document VARCHAR(45), IN number bigint UNSIGNED)
BEGIN
	INSERT INTO Clients (`type`, `name`)
		VALUES ('legal', name);
        
	CALL new_document (LAST_INSERT_ID(), document, number);
END