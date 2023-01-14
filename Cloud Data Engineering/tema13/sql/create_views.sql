CREATE VIEW contabyx.spectrum_transactions AS
SELECT * FROM contabyx.transactions
UNION ALL
SELECT * FROM ext_contabyx.transactions
WITH NO SCHEMA BINDING;

CREATE VIEW contabyx.spectrum_transfers AS
SELECT * FROM contabyx.transfers
UNION ALL
SELECT * FROM ext_contabyx.transfers
WITH NO SCHEMA BINDING;

CREATE VIEW contabyx.spectrum_tax AS
SELECT * FROM contabyx.tax
UNION ALL
SELECT * FROM ext_contabyx.tax
WITH NO SCHEMA BINDING;