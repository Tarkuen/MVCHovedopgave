# Twisted Webserver

Webserver skrevet vha. Twisted


# Start Serveren

```cmd
cd /TwistedServer
py server.py
```

## Konfiguration

For at udvide funktionaliteten af webserveren, skal man gøre følgende:

Twisted får sine instruktioner gennem Query stringen i de HTTP requests, som den modtager.
Derfor har vi defineret sammenhængen mellem hvad Scrapys <i>Spider</i> har af <i>name</i> attribut
og Query string keywordet i <b>Config.json</b>.

### Config.json

Denne fil følger Key/Value JSON strukturen, hvilket minder om en python dictionary.

<i>Key</i> er navnet på det keyword, som query strengen skal anvende.
<i>Value</i> er det tilhørende Python script, der skal håndtere instruktionen.

### Twisted Instruktioner

For at håndtere et query string keyword, skal man først definere det i Config.json.
Herefter skal man lægge et Python script i kataloget: <i>Commands</i>.

<i>Commands scripts </i> skal returnere en streng, der følger denne struktur

<b>" SPIDERNAME -a url=STARTURL-ADDRESS "</b>
Eksempelvis: " spider1 -a url=https://www.dr.dk "

## Extend the Server




