CREATE DEFINER=`root`@`%` PROCEDURE `get_history`(IN clientID INT)
BEGIN
	SELECT s.* FROM (SELECT @clientID:=clientID p) Transactions, Transaction_History s;
END