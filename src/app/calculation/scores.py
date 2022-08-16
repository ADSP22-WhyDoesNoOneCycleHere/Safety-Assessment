import pandas as pd
from sqlalchemy import create_engine

def calculate_scores_legs(leg, cur, conn):
    # annoying cleaning of input strings as sql cant handle some operators (:, $, etc)
    leg['infra_type'] = leg['infra_type'].replace("~'^parking:.*$'~'.'", "parking")
    leg['infra_type'] = leg['infra_type'].replace(":", "")

    if leg['c_count'] > 0:     # if a leg was never chosen (means never taken asw well), then there is not enough data to calculate scores for this leg
        leg['a_score'] = min(leg['a_count'] / leg['count'], 1)
        leg['c_score'] = min(leg['c_count'] / leg['count'], 1)

        leg['p_score'] = leg['c_count'] / (leg['c_count'] + leg['a_count'])

        # Scary incidents times 4.4 as this is the weight that was calculated for Berlin (see bachelors thesis)
        leg['s_score'] = max(min(1 - (1 / leg['count'] * leg['length']) * (
                    4.4 * leg['scary_incident_count'] + leg['normal_incident_count']), 1), 0)
        leg['danger_score'] = (1 / leg['count'] * leg['length']) * (
                    4.4 * leg['scary_incident_count'] + leg['normal_incident_count'])
        leg['m_p_score'] = (leg['p_score'] + 2 * leg['s_score']) / 3

        query = f'update "SimRaAPI_osmwayslegsused" ' \
                f"set " \
                f"infra_type = array_append(infra_type, '{leg['infra_type']}'), " \
                f"a_score = {leg['a_score']}, " \
                f"c_score = {leg['c_score']}, " \
                f"p_score = {leg['p_score']}, " \
                f"s_score = {leg['s_score']}, " \
                f"m_p_score = {leg['m_p_score']}, " \
                f"danger_score = {leg['danger_score']} " \
                f"where id = {leg['id']};"

        cur.execute(query)
        conn.commit()

    else:
        query = f'update "SimRaAPI_osmwayslegsused" ' \
                f'set ' \
                f"infra_type = array_append(infra_type, '{leg['infra_type']}') " \
                f"where id = {leg['id']};"

        cur.execute(query)
        conn.commit()


def calculate_scores_infra_types(infra_type, cur, conn):
    infra_type = infra_type.replace("~'^parking:.*$'~'.'", "parking")
    infra_type = infra_type.replace(":", "")

    query = f'insert into infra_type_scores' \
            f'(infra_type, avg_p_score, avg_s_score, avg_m_p_score, ' \
            f'avg_danger_score, count,  avg_a_score, avg_c_score, ' \
            f'avg_incident_count, avg_scary_incident_count, avg_c_count, ' \
            f'avg_a_count) ' \
            f'select ' \
            f"'{infra_type}', " \
            f'p_score, ' \
            f's_score, ' \
            f'round((p_score + 2 * s_score) / 3, 4), ' \
            f'avg_danger_score, ' \
            f'count, ' \
            f'avg_a_score, ' \
            f'avg_c_score, ' \
            f'avg_incident_count, ' \
            f'avg_scary_incident_count, ' \
            f'avg_c_count, ' \
            f'avg_a_count ' \
            f'from (' \
            f'select ' \
            f'sum(count) as count, ' \
            f'case when (sum(count)::numeric != 0) then round(sum("avoidedCount")::numeric / sum(count)::numeric, 4) else 1 end as avg_a_score, ' \
            f'case when (sum(count)::numeric != 0) then round(sum("chosenCount")::numeric / sum(count)::numeric, 4) else 0 end as avg_c_score, ' \
            f'round(avg("normalIncidentCount"), 4) as avg_incident_count, ' \
            f'round(avg("scaryIncidentCount"), 4) as avg_scary_incident_count, ' \
            f'round(avg("chosenCount"), 4) as avg_c_count, ' \
            f'round(avg("avoidedCount"), 4) as avg_a_count, ' \
            f'round((1 / sum(count * (ST_Length(geom::geography)::numeric / 1000))::numeric * (4.4 * sum("scaryIncidentCount")::numeric + sum("normalIncidentCount")::numeric)), 4) as avg_danger_score, ' \
            f'case when((sum("avoidedCount")::numeric + sum("chosenCount")::numeric) != 0) ' \
            f'then round(sum("chosenCount")::numeric / (sum("avoidedCount")::numeric + sum("chosenCount")::numeric), 4)::numeric ' \
            f'else -1 ' \
            f'end as p_score, ' \
            f'case when (sum(count * (ST_Length(geom::geography)::numeric / 1000))::numeric != 0) ' \
            f'then round(greatest(least(1 - (1 / sum(count * (ST_Length(geom::geography)::numeric / 1000))::numeric * (4.4 * sum("scaryIncidentCount")::numeric + sum("normalIncidentCount")::numeric)), 1)::numeric, 0)::numeric, 4)::numeric ' \
            f'else -1 ' \
            f'end as s_score ' \
            f'from "SimRaAPI_osmwayslegsused" ' \
            f"where '{infra_type}' = any(infra_type)" \
            f") f;"

    cur.execute(query)
    conn.commit()


def add_columns(cur, conn):
    query = 'alter table "SimRaAPI_osmwayslegsused" ' \
            'drop column if exists a_score, ' \
            'drop column if exists c_score, ' \
            'drop column if exists p_score, ' \
            'drop column if exists s_score, ' \
            'drop column if exists m_p_score, ' \
            'drop column if exists danger_score, ' \
            'drop column if exists infra_type;'

    cur.execute(query)
    conn.commit()

    query = 'alter table "SimRaAPI_osmwayslegsused"' \
            "add column if not exists a_score numeric," \
            "add column if not exists c_score numeric," \
            "add column if not exists p_score numeric," \
            "add column if not exists s_score numeric," \
            "add column if not exists m_p_score numeric," \
            "add column if not exists danger_score numeric," \
            "add column if not exists infra_type text[];"

    cur.execute(query)
    conn.commit()


def initialize_infra_table(cur, conn):
    cur.execute('drop table if exists infra_type_scores;')
    conn.commit()

    query = f'create table if not exists infra_type_scores (' \
            f'id serial primary key, ' \
            f'infra_type text, ' \
            f'avg_p_score numeric, ' \
            f'avg_s_score numeric, ' \
            f'avg_m_p_score numeric, ' \
            f'avg_danger_score numeric, ' \
            f'count numeric, ' \
            f'avg_a_score numeric, ' \
            f'avg_c_score numeric, ' \
            f'avg_incident_count numeric, ' \
            f'avg_scary_incident_count numeric, ' \
            f'avg_c_count numeric, ' \
            f'avg_a_count numeric);'

    cur.execute(query)
    conn.commit()


def save_infra_type_scores(city):
    alchemyEngine = create_engine('postgresql://simra:simra12345simra@localhost:5432/simra')

    dbConnection = alchemyEngine.connect()

    infra_types_scores_city = pd.read_sql('select * from "infra_type_scores"', dbConnection)

    infra_types_scores_city.to_csv(f'city_results/{city}.csv')
