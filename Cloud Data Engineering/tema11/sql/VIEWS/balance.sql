CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`%` 
    SQL SECURITY DEFINER
VIEW `Balance` AS
    SELECT 
        `Clients`.`clientID` AS `Client`,
        ROUND(SUM((CASE
            WHEN (`Transactions`.`nature` = 'income') THEN `Transactions`.`amount`
            ELSE (`Transactions`.`amount` * -(1))
        END)), 2) AS `Balance`
    FROM
        (`Clients`
        JOIN `Transactions` ON ((`Clients`.`clientID` = `Transactions`.`clientID`)))
    GROUP BY `Clients`.`clientID`