CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`%` 
    SQL SECURITY DEFINER
VIEW `Transaction_History` AS
    SELECT 
        `Transactions`.`transactionID` AS `Transaction`,
        `Transactions`.`time` AS `Time`,
        ROUND((CASE
                    WHEN (`Transactions`.`nature` = 'income') THEN `Transactions`.`amount`
                    ELSE (`Transactions`.`amount` * -(1))
                END),
                2) AS `Movement`
    FROM
        `Transactions`
    WHERE
        (`Transactions`.`clientID` = GET_CLIENT())
    ORDER BY `Transactions`.`time`