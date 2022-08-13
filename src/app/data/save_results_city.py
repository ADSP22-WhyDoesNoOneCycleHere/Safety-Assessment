import pandas as pd
from sqlalchemy import create_engine

def save_infra_type_scores(country, city):
    alchemyEngine = create_engine('postgresql://simra:simra12345simra@localhost:5432/simra')

    dbConnection = alchemyEngine.connect()

    infra_types_scores_city = pd.read_sql('select * from "infra_type_scores"', dbConnection)

    infra_types_scores_city.to_csv(f'city_results/{city}.csv')

