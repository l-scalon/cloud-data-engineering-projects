CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`%` 
    SQL SECURITY DEFINER
VIEW `Transfer_History` AS
    SELECT 
        `Transfer_Aux_Expense`.`transferID` AS `Transfer`,
        `Transfer_Aux_Expense`.`From` AS `From`,
        `Transfer_Aux_Income`.`To` AS `To`,
        `Transfer_Aux_Expense`.`Movement` AS `Movement`
    FROM
        (`Transfer_Aux_Expense`
        JOIN `Transfer_Aux_Income` ON ((`Transfer_Aux_Expense`.`transferID` = `Transfer_Aux_Income`.`transferID`)))