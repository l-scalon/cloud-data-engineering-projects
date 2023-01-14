CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`%` 
    SQL SECURITY DEFINER
VIEW `Transfer_Aux_Expense` AS
    SELECT 
        `Transfers`.`transferID` AS `transferID`,
        `Transactions`.`clientID` AS `From`,
        `Transactions`.`amount` AS `Movement`
    FROM
        (`Transactions`
        JOIN `Transfers` ON ((`Transactions`.`transactionID` = `Transfers`.`expense_transactionID`)))