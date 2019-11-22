# Opsætning af Virtuelt miljø

## Conda

For at oprette det virtuelle miljø med de rigtige packages, har jeg lavet en enviroment fil.
Ved endt udvikling og test, opretter man miljøet ved at skrive

```cmd
cd \Hovedopgave\MVCHovedopgave\MVCHovedopgave\scrapy
```

```conda
conda env create --file .\enviroment.yml
conda activate scrapy_env
conda list -n scrapy_env
```