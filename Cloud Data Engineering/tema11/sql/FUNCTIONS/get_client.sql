CREATE DEFINER=`root`@`%` FUNCTION `get_client`() RETURNS int
    NO SQL
    DETERMINISTIC
BEGIN

RETURN @clientID;
END