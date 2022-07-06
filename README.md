# Safety-Assessment

Es soll die Sicherheit von verschiedenen Straßeninfrastrukturen gemessen werden. Dafür soll für verschiedene Straßentypen, die über osm bestimmt werden können, die verschiedenen Scores der Bachelorarbeit benutzt werden um darüber was herauszufinden.

Anleitung setup:
1. Start postgres server, with simra database correctly set up
2. Start uvicorn server for osm-infrastructure repository
3. Run the python file

A description of the infrastructure-types used can be found [here](/doc/infra-types.md)


## Startup

 `docker-compose up`
