SCHTASKS /create /tn contabyx_backup /xml %~dp0\mongodb_contabyx.xml
PAUSE