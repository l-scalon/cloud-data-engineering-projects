CREATE EXTERNAL TABLE IF NOT EXISTS `contabyx`.`transactions` (
  `transactionid` int,
  `clientid` int,
  `typeid` int,
  `time` timestamp,
  `amount` float
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe' 
WITH SERDEPROPERTIES (
  'serialization.format' = '1'
) LOCATION 's3://<BUCKET>/<KEY>/contabyx-parquet/transactions/'
TBLPROPERTIES ('has_encrypted_data'='false');

CREATE EXTERNAL TABLE IF NOT EXISTS `contabyx`.`transfers` (
  `transferid` int,
  `expense_transactionid` int,
  `income_transactionid` int
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe' 
WITH SERDEPROPERTIES (
  'serialization.format' = '1'
) LOCATION 's3://<BUCKET>/<KEY>/contabyx-parquet/transfers/'
TBLPROPERTIES ('has_encrypted_data'='false');

CREATE EXTERNAL TABLE IF NOT EXISTS `contabyx`.`tax` (
  `transactionid` int,
  `taxtypeid` int,
  `fee` float
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe' 
WITH SERDEPROPERTIES (
  'serialization.format' = '1'
) LOCATION 's3://<BUCKET>/<KEY>/contabyx-parquet/tax/'
TBLPROPERTIES ('has_encrypted_data'='false');