# Safety-Assessment
This project is based on ride-data gathered by the [SimRa](https://simra-project.github.io/) mobile application. The aim is to map different street segments to [infrastructure types](/doc/infra-types.md), that could be extracted from [openstreetmap](https://www.openstreetmap.org). After mapping, scores regarding the popularity, safety and mixed-popularity (a score gained from popularity and safety) are calculated for each infrastructure-type and saved in a [postgres](https://www.postgresql.org/) database. After computation the results can be visualized with the provided [notebook](/notebooks/Visualization.ipynb). An overview and explanation of the resulting database can be found [here](/doc/db-structure.md).

## Local development setup:
1. Follow the [instructions](/doc/postgres.md) for setting up the postgres database
2. Import the postgres dump (consists of SimRa rides mapped to openstreetmap street segments) provided [here](https://tubcloud.tu-berlin.de/s/H2AJ4iCa8J6gJMd)* by running the code below:
```
gunzip -c simra.sql.gz | psql simra
```
3. Install the code dependencies:
```
pip install -r src/requirements.txt 
```
4. Run the code:
```
python src/app/main.py
```

To specify the areas scores should be calculated for, change [areas.json](src/app/areas.json).
Note: Score calculation will only work for areas included in the SimRa dataset. To make sure that the areas you want are included check the [dashboard](https://simra-project.github.io/dashboard/).

*For security reasons the download is protected by a password. To gain access message [@tobiasengelbrecht](https://github.com/tobiasengelbrecht) or [@vDawgg](https://github.com/vDawgg).

## Startup using [docker-compose](https://docs.docker.com/compose/):
```
docker-compose up
```

## Project structure:
```
> doc                   // Further documentation, already linked to here
> notebooks             // notebook for visualizing and analyzing the results
> src                   // source-code, Dockerfile and requirements
    > app               // areas.json and main.py
        > calculation   // score calculation
        > city-results  // results from included cities in csv-format
        > data          // database and overpass functions
```
