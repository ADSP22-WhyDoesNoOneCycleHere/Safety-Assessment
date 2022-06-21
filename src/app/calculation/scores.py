def calculate_scores_ways(leg, cur, conn):
    leg['a_score'] = min(leg['a_count'] / leg['count'], 1)
    leg['c_score'] = min(leg['c_count'] / leg['count'], 1)
    leg['p_score'] = ((1 - leg['a_score']) + leg['c_score']) / 2

    # Scary incidents times 4.4 as this is the weight that was calculated for Berlin (see bachelors thesis)
    # min(x,1) as score can not be higher than 1
    leg['s_score'] = max(min(1 - (1 / leg['count'] * leg['length']) * (4.4 * leg['scary_incident_count'] + leg['normal_incident_count']), 1), 0)
    leg['m_p_score'] = ((1 - leg['a_score']) + leg['c_score'] + leg['s_score'] * 2) / 4

    # There should be a smarter way to do this
    cur.execute(f"select * from leg_scores where id = {leg['id']}")

    if len(cur.fetchall()) == 0:
        query = f"insert into leg_scores (id, infra_type, a_score, c_score, p_score, s_score, m_p_score)" \
                f"values(" \
                f"{leg['id']}, " \
                f"'{leg['infra_type']}', " \
                f"{leg['a_score']}, " \
                f"{leg['c_score']}, " \
                f"{leg['p_score']}, " \
                f"{leg['s_score']}, " \
                f"{leg['m_p_score']});"

        cur.execute(query)
        conn.commit()


def initialize_score_table(cur, conn):
    query = "create table if not exists leg_scores(" \
            "id serial primary key," \
            "infra_type text, " \
            "a_score numeric, " \
            "c_score numeric, " \
            "p_score numeric, " \
            "s_score numeric, " \
            "m_p_score numeric);"

    cur.execute(query)
    conn.commit()

    cur.execute("truncate leg_scores;")
    conn.commit()
