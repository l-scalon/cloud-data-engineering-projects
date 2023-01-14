CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`%` 
    SQL SECURITY DEFINER
VIEW `Transfer_Aux_Income` AS
    SELECT 
        `Transfers`.`transferID` AS `transferID`,
        `Transactions`.`clientID` AS `To`,
        `Transactions`.`amount` AS `Movement`
    FROM
        (`Transactions`
        JOIN `Transfers` ON ((`Transactions`.`transactionID` = `Transfers`.`income_transactionID`)))