# Explanation and overview of resulting database

The following rows can be found in the tables "SimRaAPI_osmwayslegsused"

## Explanation for relevant columns in resulting database:
| Column              | Explanation                                                    |
|---------------------|----------------------------------------------------------------|
| osmId               | openstreetmap id for connection with osm data                  |
| geom                | geometry data for use with postgis (e.g. length-calculation)   |
| streetName          | Name of the street                                             |
| count               | number of times a street-segment was included in a ride        |
| normalIncidentCount | Number of times a normal incident was recorded on this segment |
| scaryIncidentCount  | Number of times a scary incident was recorded on this segment  |
| avoidedCount        | Number of times this segment was deliberately avoided          |
| chosenCount         | Number of times this segment was deliberately chosen           |
| a_score             | The avoided-score of this street-segment                       |
| c_score             | The chosen-score of this street-segment                        |
| p_score             | The popularity-score of this street-segment                    |
| s_score             | The safety-score of this street-segment                        |
| m_p_score           | The mixed-popularity-score of this street-segment              |
| danger_score        | The dangerousness-score of this street-segment                 |
| infra_type          | The infrastructure-types that this segment could be mapped to  |

Note: not all the scores are included in the resulting analysis but might still be interesting for future research.

The table "infra_type_scores" contains the resulting scores for every infrastructure-type along with an aggregated count.