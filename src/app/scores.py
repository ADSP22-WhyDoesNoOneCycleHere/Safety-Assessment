import numpy as np
import pandas as pd
import math


if __name__ == '__main__':
    counts_by_infra = pd.read_csv("../../counts.csv", index_col=0)

    # add columns for scores we want to calculate
    #counts_by_infra[' avoided_score'] = pd.Series(np.zeros(len(counts_by_infra.index)), index=counts_by_infra.index)
    #counts_by_infra[' chosen_score'] = pd.Series(np.zeros(len(counts_by_infra.index)), index=counts_by_infra.index)
    #counts_by_infra[' popularity_score'] = pd.Series(np.zeros(len(counts_by_infra.index)), index=counts_by_infra.index)
    #counts_by_infra[' mixed_popularity_score'] = pd.Series(np.zeros(len(counts_by_infra.index)), index=counts_by_infra.index)

    counts_by_infra[' avoided_score'] = counts_by_infra.loc[:, ' avoided_count'] / counts_by_infra.loc[:, ' leg_count']
    counts_by_infra[' chosen_score'] = counts_by_infra.loc[:, ' chosen_count'] / counts_by_infra.loc[:, ' leg_count']
    counts_by_infra[' popularity_score'] = ((1 - counts_by_infra[' avoided_score']) + counts_by_infra[' chosen_score']) / 2

    counts_by_infra[' temporary_safety_score'] = 1 - (1 / counts_by_infra[' leg_count']) * (2 * counts_by_infra[' scary_incident_count'] + counts_by_infra[' normal_incident_count'])
    counts_by_infra[' mixed_popularity_score'] = ((1 - counts_by_infra[' avoided_score']) + counts_by_infra[' chosen_score'] + counts_by_infra[' temporary_safety_score'] * 2) / 4

    #for i in range(len(counts_by_infra.index)):
    #    index_label = counts_by_infra.index[i]
    #    if not math.isnan(counts_by_infra.loc[index_label, ' avoided_score']):
    #        print()

    counts_by_infra.to_csv("../../scores.csv")
    print(counts_by_infra[[' temporary_safety_score', ' mixed_popularity_score']])