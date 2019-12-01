# How to use Liquibase Cli
## Requires Liquibase and Postgres installed! 
Install Liquibase Cli: https://www.liquibase.org/documentation/installation-windows.html

Install Postgresql: https://www.postgresql.org/download/windows/

Yderlig SKAL du opdatere db.properties, som den stemmer overens med din egen lokale database! Dvs. URL, USERNAME og PASSWORD!

MAN MÅ IKKE ÆNDRE EN CHANGELOG, HVIS DEN ER RULLET UD! Liquibase holder en checksum, for hvilken version der er ude og hvad der blev tilføjet under første udrulning!

### Status Command
Denne command giver dig mulighed for at se, hvilken tilstand din nuværende database er i. Altså hvilke changelogs der er blevet rullet på.
```
liquibase --defaultsFile=db.properties --changeLogFile=changelog-master.xml status
```
### Update Command
Update commandoen, opdatere din database til den nyeste version som er tilføjet i changelog-master.xml!
```
liquibase --defaultsFile=db.properties --changeLogFile=changelog-master.xml update
```
### Rollback Command
Rollback commamndoen, giver dig mulighed for at rollback til en ældre version! < tag > er navnet på den gamle changelog gerne vil rollback til!
```
liquibase --defaultsFile=db.properties --changeLogFile=changelog-master.xml rollback <tag>
```
