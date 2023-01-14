DROP schema IF EXISTS ext_contabyx;
CREATE EXTERNAL SCHEMA ext_contabyx FROM data catalog 
DATABASE 'contabyx' 
iam_role DEFAULT
CREATE EXTERNAL DATABASE IF NOT EXISTS;