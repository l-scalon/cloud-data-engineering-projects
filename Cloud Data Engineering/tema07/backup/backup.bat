@ECHO OFF
mkdir .\backups\

FOR /F "usebackq tokens=1,2 delims=,=- " %%i IN (`wmic os get LocalDateTime /value`) DO @if %%i==LocalDateTime (SET token10=%%j)

docker exec mysql /usr/bin/mysqldump -u root --password=%1 --default-character-set=utf8 --skip-set-charset --skip-add-drop-table --no-create-info --insert-ignore contabyx > .\backups\contabyx%token10:~0,14%.sql

GOTO :count

:count
    FOR /F %%a IN ('dir .\backups\ /a-d-s-h /b ^| FIND /v /c ""') DO SET count=%%a
    IF %count% gtr 3 (
        GOTO :delete) ELSE (
            GOTO :breakloop)
:delete
    FOR /F "delims=" %%a IN ('dir /b /a-d /t:w /o:d ".\backups\*.sql"') DO (
        DEL ".\backups\%%a"
        GOTO :count)
:breakloop