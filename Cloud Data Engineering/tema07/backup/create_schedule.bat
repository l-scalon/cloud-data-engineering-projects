SCHTASKS /create /tn backup /xml %~dp0\backup_schedule.xml
PAUSE