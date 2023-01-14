@ECHO OFF
CALL path\to\venv\Scripts\activate.bat
python path\to\Scripts\main.py
aws s3 sync path\to\Scripts\tweets s3://path/to/tweets/
