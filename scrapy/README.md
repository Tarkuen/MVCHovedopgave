# Opsætning af Virtuelt miljø

## Conda

For at oprette det virtuelle miljø med de rigtige packages, har jeg lavet en enviroment fil.
Ved endt udvikling og test, opretter man miljøet ved at skrive

```cmd
cd /Hovedopgave/MVCHovedopgave/MVCHovedopgave/scrapy
```

```conda
conda env create --file ./enviroment.yml
conda activate scrapy_env
conda list -n scrapy_env
```

<b>Husk at tjekke om scrapy er installeret m. korrekt version</b>

```cmd
scrapy -v
```

# Chrome Dependency 
<b>Denne POC kræver min. Chrome version 78, samt en binær chromedriver</b>

I forbindelse med mine tests, har jeg fundet mange kontaktsider, der bruger JS til at skjule deres mails fra scrapers.
For at komme rundt om dette, har jeg importeret Selenium, der simulerer en browser ('user agent').

Derfor kræver det Chrome version 78 for at køre scraperen og den installeres på følgende måde:

Efter installationen, kræver det en driver til chrome.

# Mac

In it's current form, you cannot use our software on a MacOS or any non-windows distribution.
This is still to be scheduled for a fix in an upcoming release


# Windows 
## Driver installation

Kræver <b>Powershell</b> som default følger med windows 10

### Windows Driver

```powershell
New-Item -ItemType Directory -Path "C:/chromedriver/"
cd "C:/chromedriver/"
Invoke-WebRequest -Uri "https://chromedriver.storage.googleapis.com/78.0.3904.105/chromedriver_win32.zip" -OutFile "chromedriver_win32.zip"
Expand-Archive -Path "chromedriver_win32.zip" -DestinationPath "."
```
Jeg har valgt et dir på C drevet, men det kan I naturligvis ændre så det passer til jeres system - Det berør kun New-Item og cd kommandoen.

# Kør Scraperen

```cmd
cd MVCHovedopgave/Scrapy/scrapy_project
scrapy crawl spider1
```