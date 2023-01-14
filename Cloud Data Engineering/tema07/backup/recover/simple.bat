@ECHO OFF
GOTO :newest

:newest
    FOR /F "delims=" %%a IN ('dir /b /a-d /t:w /o:d "..\backups\*.sql"') DO (
        SET file=%%a
        )

type ..\backups\%file% | docker exec -i mysql /usr/bin/mysql -u root --password=%1 --default-character-set=utf8 contabyx