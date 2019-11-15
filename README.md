[fork]: https://help.github.com/assets/images/help/repository/fork_button.jpg "Github Fork"

# MVC Hovedopgave
Hovedopgave til Datamatiker

# Workflow

Når man skal starte på en ny feature, er det vigtigt at vi følger denne process:


### Ved ny feature
  + Opret personlig synkroniseret Fork    
  + Opret feature-branch på personlig fork  
  + Udvikling af ny feature foregår på feature-branch

### Efter endt udvikling

  + Opret pull request fra feature branch, tilbage til dette master repo  
  + Sæt gruppen på som reviewers


### Opsætning af workspace

Husk opsætningen af dit workspace, for at sikre synkroniseringen af workspacet er bedst:

```git
git fetch | git pull 
```

Dette <i>stager</i> de seneste ændringer fra din fork og henter dem ned til dit lokale repo.

### Fork

For at lave en personlig fork på Github gør man følgende:

![alt text][fork]

### Feature Branch

Nu kan du lave en branch af din personlige fork, så du ikke korrupterer din egen fork.

```git
git checkout -b navn_på_feature_branch_uden_spaces
```
Nu er du klar til at udvikle !

<br></br>
<br></br>

# Efter en feature er lavet færdig og testet

For at sikre, at det er nemmere at ændre dele af koden tilbage, hvis den viser sig ikke at kunne integreres  
så er det vigtigt at committe ændringer til koden løbende, når man er færdig med en feature.

Når man er færdig med sin session, skal man derfor blot huske at pushe dem til sin fork og lave et pull request.

### Stage dine ændringer

Tjek dine ændringer, for at se hvad du skal committe:
```git
git status
```


Tilføj de relevante filer til dit commit
```git
git add navn_på_fil1 navn_på_fil2
```


Eller for at tilføje alle ændringer: 
```git
git add .
```

### Commit dine ændringer

Efter at du har tilføjet de relevante filer fra det tidligere trin, er du nu klar til at tilføje dem til dit commit.
```git
git commit -m 'Din Commit beskrivelse af den feature som ændringerne er knyttet til. '
```

Denne process med at tilføje og committe fortsætter indtil at din session er færdig.

## Efter endt udvikling

### Push til repo
For at gemme ændringerne i din personlige fork, skal du pushe dine commits:
```git
git push
```

# Pull Request

For at merge dine ændringer mod master repo'et. 

  * Fra master repo'et kan du enten trykke på <b>Make Pull Request</b> øverst til venstre, eller tryk på linket https://github.com/Tarkuen/MVCHovedopgave/pull/new/master 
  * Tryk herefter på <b>Compare across forks</b>
  * Herefter kan du vælge base repositoriet som 'MVC Hovedopgave' -> 'master'
  * Head repositoriet er din personlige fork, og branchen er din personlige feature branch
  * Indtast herefter en beskrivelse for ændringer, gerne feature og story ID.
  * Tryk herefter <b>Create Pull Request</b> øverst til højre.

