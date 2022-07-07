def calculate_scores_legs(leg, cur, conn):

    # annoying cleaning of input strings as sql cant handle some operators (:, $, etc)
    if "parking" in leg['infra_type']:
        leg["infra_type"] = "[highway = residential][parking][!cycleway]"
    leg['infra_type'] = leg['infra_type'].replace(":", "")

    if leg['count'] > 0:
        leg['a_score'] = min(leg['a_count'] / leg['count'], 1)
        leg['c_score'] = min(leg['c_count'] / leg['count'], 1)
        leg['p_score'] = ((1 - leg['a_score']) + leg['c_score']) / 2

        # Scary incidents times 4.4 as this is the weight that was calculated for Berlin (see bachelors thesis)
        leg['s_score'] = max(min(1 - (1 / leg['count'] * leg['length']) * (4.4 * leg['scary_incident_count'] + leg['normal_incident_count']), 1), 0)
        leg['danger_score'] = (1 / leg['count'] * leg['length']) * (4.4 * leg['scary_incident_count'] + leg['normal_incident_count'])
        leg['m_p_score'] = ((1 - leg['a_score']) + leg['c_score'] + leg['s_score'] * 2) / 4

        query = f'update "SimRaAPI_osmwayslegs" ' \
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
        query = f'update "SimRaAPI_osmwayslegs" ' \
                f'set ' \
                f"infra_type = array_append(infra_type, '{leg['infra_type']}') " \
                f"where id = {leg['id']};"

        cur.execute(query)
        conn.commit()


def calculate_scores_infra_types(infra_type, cur, conn):
    if "parking" in infra_type:
        infra_type = "[highway = residential][parking][!cycleway]"
    infra_type = infra_type.replace(":", " ")

    query = f'insert into infra_type_scores' \
            f'(infra_type, avg_a_score, avg_c_score, avg_p_score, ' \
            f'avg_s_score, avg_m_p_score, count, incident_count, ' \
            f'avg_incident_count, scary_incident_count, ' \
            f'avg_scary_incident_count, c_count, avg_c_count, ' \
            f'a_count, avg_a_count) ' \
            f'select ' \
            f"'{infra_type}', " \
            f'round(avg(a_score), 4), ' \
            f'round(avg(c_score), 4), ' \
            f'round(avg(p_score), 4), ' \
            f'round(avg(s_score), 4), ' \
            f'round(avg(danger_score), 4), ' \
            f'round(avg(m_p_score), 4), ' \
            f'sum(count), ' \
            f'sum("normalIncidentCount"), ' \
            f'round(avg("normalIncidentCount"), 4), ' \
            f'sum("scaryIncidentCount"), ' \
            f'round(avg("scaryIncidentCount"), 4), ' \
            f'sum("chosenCount"), ' \
            f'round(avg("chosenCount"), 4), ' \
            f'sum("avoidedCount"), ' \
            f'round(avg("avoidedCount"), 4) ' \
            f'from "SimRaAPI_osmwayslegs" ' \
            f"where '{infra_type}' = any(infra_type)" \
            f"and count > 0;"

    cur.execute(query)
    conn.commit()


def add_columns(cur, conn):
    query = 'alter table "SimRaAPI_osmwayslegs" ' \
            'drop column if exists a_score, ' \
            'drop column if exists c_score, ' \
            'drop column if exists p_score, ' \
            'drop column if exists s_score, ' \
            'drop column if exists m_p_score, ' \
            'drop column if exists danger_score, ' \
            'drop column if exists infra_type;'

    cur.execute(query)
    conn.commit()

    query = 'alter table "SimRaAPI_osmwayslegs"' \
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

    query = f'create table  if not exists infra_type_scores (' \
            f'id serial primary key, ' \
            f'infra_type text, ' \
            f'avg_a_score numeric, ' \
            f'avg_c_score numeric, ' \
            f'avg_p_score numeric, ' \
            f'avg_s_score numeric, ' \
            f'avg_m_p_score numeric, ' \
            f'avg_danger_score numeric, ' \
            f'count numeric, ' \
            f'incident_count numeric, ' \
            f'avg_incident_count numeric, ' \
            f'scary_incident_count numeric, ' \
            f'avg_scary_incident_count numeric, ' \
            f'c_count numeric, ' \
            f'avg_c_count numeric, ' \
            f'a_count numeric, ' \
            f'avg_a_count numeric);'

    cur.execute(query)
    conn.commit()
