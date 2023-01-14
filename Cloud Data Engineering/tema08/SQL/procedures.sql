CREATE PROCEDURE contabyx.analyze_all
AS 
   BEGIN

      SET  XACT_ABORT  ON

      SET  NOCOUNT  ON
      
      UPDATE STATISTICS contabyx.Clients
      UPDATE STATISTICS contabyx.Documents
      UPDATE STATISTICS contabyx.Tax
      UPDATE STATISTICS contabyx.Transactions
      UPDATE STATISTICS contabyx.Transfers
    END;
GO;
CREATE PROCEDURE contabyx.delete_null_from_transfers
AS 
   BEGIN

      SET  XACT_ABORT  ON

      SET  NOCOUNT  ON

      DELETE 
      FROM contabyx.Transfers
      WHERE Transfers.expense_transactionID IS NULL AND Transfers.income_transactionID IS NULL
      
      DELETE
      FROM contabyx.Transfers
      WHERE Transfers.expense_transactionID IS NULL
      AND income_transactionID NOT IN (
      	SELECT transactionID
      	FROM contabyx.Transactions
      	JOIN contabyx.Transfer_income_where_expense_is_null
      	ON transactionID = contabyx.Transfer_income_where_expense_is_null.income_transactionID)
   END;

CREATE FUNCTION contabyx.enum2str$Clients$type 
( 
   @setval tinyint
)
RETURNS nvarchar(max)
AS 
   BEGIN
      RETURN 
         CASE @setval
            WHEN 1 THEN 'natural'
            WHEN 2 THEN 'legal'
            ELSE ''
         END
   END;

CREATE FUNCTION contabyx.enum2str$tax_rate$nature 
( 
   @setval tinyint
)
RETURNS nvarchar(max)
AS 
   BEGIN
      RETURN 
         CASE @setval
            WHEN 1 THEN 'income'
            WHEN 2 THEN 'expense'
            ELSE ''
         END
   END;

CREATE FUNCTION contabyx.enum2str$Transactions$nature 
( 
   @setval tinyint
)
RETURNS nvarchar(max)
AS 
   BEGIN
      RETURN 
         CASE @setval
            WHEN 1 THEN 'income'
            WHEN 2 THEN 'expense'
            ELSE ''
         END
   END;

CREATE FUNCTION contabyx.get_client 
(
)
RETURNS int
AS 
   BEGIN
      RETURN NULL

   END;

CREATE PROCEDURE contabyx.get_history  
   @clientID int
AS 
   BEGIN

      SET  XACT_ABORT  ON

      SET  NOCOUNT  ON
      
      SELECT [Transaction], [Time], Movement FROM contabyx.Transaction_History
      WHERE clientID = @clientID
      ORDER BY 2
   END;

CREATE PROCEDURE contabyx.new_client_legal  
   @name nvarchar(255),
   @document nvarchar(45),
   @number bigint
AS 
   BEGIN

      SET  XACT_ABORT  ON

      SET  NOCOUNT  ON

      INSERT contabyx.Clients(type, name)
         VALUES (contabyx.norm_enum$Clients$type(N'legal'), @name)
         
      DECLARE @temp int
      SET @temp = scope_identity()
      EXECUTE contabyx.new_document @temp, @document, @number
	END;
      
CREATE PROCEDURE contabyx.new_client_natural  
   @name nvarchar(255),
   @document nvarchar(45),
   @number bigint
AS 
   BEGIN

      SET  XACT_ABORT  ON

      SET  NOCOUNT  ON

      INSERT contabyx.Clients(type, name)
         VALUES (contabyx.norm_enum$Clients$type(N'natural'), @name)
         
      DECLARE @temp int
      SET @temp = scope_identity()
      EXECUTE contabyx.new_document @temp, @document, @number
   END;

CREATE PROCEDURE contabyx.new_document  
   @clientID int,
   @document nvarchar(45),
   @number bigint
AS 
   BEGIN

      SET  XACT_ABORT  ON

      SET  NOCOUNT  ON

      INSERT contabyx.Documents(clientID, type, number)
         VALUES (@clientID, @document, @number)

   END;

CREATE PROCEDURE contabyx.new_transaction_expense  
   @clientID int,
   @amount float(24)
AS 
   BEGIN

      SET  XACT_ABORT  ON

      SET  NOCOUNT  ON

      DECLARE
         @rate float(24)

      DECLARE
         @fee float(24)

      INSERT contabyx.Transactions(clientID, nature, amount)
         VALUES (@clientID, contabyx.norm_enum$Transactions$nature(N'expense'), @amount)

      SET @rate = contabyx.tax_rate(0, @amount)

      SET @fee = contabyx.tax_fee(@amount, @rate)

      INSERT contabyx.Tax(transactionID, rate, fee)
         VALUES (scope_identity(), @rate, @fee)

   END;

CREATE PROCEDURE contabyx.new_transaction_income  
   @clientID int,
   @amount float(24)
AS 
   BEGIN

      SET  XACT_ABORT  ON

      SET  NOCOUNT  ON

      DECLARE
         @rate float(24)

      DECLARE
         @fee float(24)

      INSERT contabyx.Transactions(clientID, nature, amount)
         VALUES (@clientID, contabyx.norm_enum$Transactions$nature(N'income'), @amount)

      SET @rate = contabyx.tax_rate(0, @amount)

      SET @fee = contabyx.tax_fee(@amount, @rate)

      INSERT contabyx.Tax(transactionID, rate, fee)
         VALUES (scope_identity(), @rate, @fee)

   END;

CREATE PROCEDURE contabyx.new_transfer
	@source int,
	@destination int,
	@amount float(24)
AS
	BEGIN
		
	  SET  XACT_ABORT  ON

      SET  NOCOUNT  ON
      
      DECLARE
      	@transferID int,
      	@expenseID int
      
      EXECUTE contabyx.new_transaction_expense @source, @amount
      SET @expenseID = IDENT_CURRENT('contabyx.Transactions')
      
      INSERT INTO contabyx.Transfers (expense_transactionID)
      VALUES (@expenseID)
      
      SET @transferID = IDENT_CURRENT('contabyx.Transfers')
      
      EXECUTE contabyx.new_transaction_income @destination, @amount
      
      UPDATE contabyx.Transfers
      SET income_transactionID = IDENT_CURRENT('contabyx.Transactions')
      WHERE transferID = @transferID
		
	END;

CREATE FUNCTION contabyx.norm_enum$Clients$type 
( 
   @setval nvarchar(max)
)
RETURNS nvarchar(max)
AS 
   BEGIN
      RETURN contabyx.enum2str$Clients$type(contabyx.str2enum$Clients$type(@setval))
   END;

CREATE FUNCTION contabyx.norm_enum$tax_rate$nature 
( 
   @setval nvarchar(max)
)
RETURNS nvarchar(max)
AS 
   BEGIN
      RETURN contabyx.enum2str$tax_rate$nature(contabyx.str2enum$tax_rate$nature(@setval))
   END;

CREATE FUNCTION contabyx.norm_enum$Transactions$nature 
( 
   @setval nvarchar(max)
)
RETURNS nvarchar(max)
AS 
   BEGIN
      RETURN contabyx.enum2str$Transactions$nature(contabyx.str2enum$Transactions$nature(@setval))
   END;

CREATE FUNCTION contabyx.str2enum$Clients$type 
( 
   @setval nvarchar(max)
)
RETURNS tinyint
AS 
   BEGIN
      RETURN 
         CASE @setval
            WHEN 'natural' THEN 1
            WHEN 'legal' THEN 2
            ELSE 0
         END
   END;

CREATE FUNCTION contabyx.str2enum$tax_rate$nature 
( 
   @setval nvarchar(max)
)
RETURNS tinyint
AS 
   BEGIN
      RETURN 
         CASE @setval
            WHEN 'income' THEN 1
            WHEN 'expense' THEN 2
            ELSE 0
         END
   END;

CREATE FUNCTION contabyx.str2enum$Transactions$nature 
( 
   @setval nvarchar(max)
)
RETURNS tinyint
AS 
   BEGIN
      RETURN 
         CASE @setval
            WHEN 'income' THEN 1
            WHEN 'expense' THEN 2
            ELSE 0
         END
   END;

CREATE FUNCTION contabyx.tax_fee 
( 
   @rate float(24),
   @amount float(24)
)
RETURNS float(24)
AS 
   BEGIN

      DECLARE
         @fee float(24)

      SET @fee = @rate * @amount

      RETURN @fee

   END;

CREATE FUNCTION contabyx.tax_rate 
( 
   @nature nvarchar(7),
   @amount float(24)
)
RETURNS float(24)
AS 
   BEGIN

      DECLARE
         @rate float(24)

      SET @rate = 0

      IF @nature = 0
         IF (@amount >= 1000 AND @amount < 5000)
            SET @rate = 0.005
         ELSE 
            IF (@amount >= 5000 AND @amount < 9000)
               SET @rate = 0.007
            ELSE 
               IF (@amount >= 9000 AND @amount < 11000)
                  SET @rate = 0.009
               ELSE 
                  BEGIN
                     IF @amount >= 11000
                        SET @rate = 0.011
                  END
      ELSE 
         IF (@amount >= 5000 AND @amount < 9000)
            SET @rate = 0.005
         ELSE 
            IF (@amount >= 9000 AND @amount < 11000)
               SET @rate = 0.007
            ELSE 
               BEGIN
                  IF @amount >= 11000
                     SET @rate = 0.009
               END

      RETURN @rate

   END;
