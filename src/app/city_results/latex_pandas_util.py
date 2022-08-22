import pandas as pd


def round_dataframe(df, decimals):
    df = df.round(decimals)
    return df


def choose_columns(df, column_indices):
    df = df[column_indices]
    return df


def choose_indices(df, index_indices):
    contained_indices = []

    for index_name in index_indices:
        if index_name in df.index:
            print(f"HALT {index_name}")
            contained_indices.append(index_name)

    df = df.loc[contained_indices, :]
    return df


def latex_tabular(df, decimals):
    str = df.to_latex(float_format=f"{{:0.{decimals}f}}".format)
    return str


def change_latex_str(str):
    str = str.replace("\\toprule\n", "")
    str = str.replace("\\midrule\n", "")
    str = str.replace("\\bottomrule\n", "")
    str = str.replace(r"\\", r"\\ \hline")
    str = str.replace("lrrrr", "|l|l|l|l|l|")
    return str


def tabular_to_table(str, city):
    temp = "\\begin{table}[!ht]\n\\captionof{listing}{Results " + city + "}\n\\label{tab:results" + city + "}\n\\centering\n" \
           "\\begin{adjustbox}{tabular=lllll, center}\n"
    temp = temp + str
    temp = temp + "\\end{adjustbox}\n\\end{table}"
    return temp

def main():
    city = "Stuttgart"

    df = pd.read_csv(f"{city}.csv", index_col=0)
    df = df.set_index("infra_type")

    df = round_dataframe(df, 3)

    print(df.index)

    df = choose_columns(df, ["count", "avg_p_score", "avg_s_score", "avg_m_p_score"])
    df = choose_indices(df, ['[bicycle = designated][segregated = yes]', "[bicycle_road = yes][!segregated]",
                             '[bicycle = designated][parking][!segregated]',
                             "[cycleway = track]", "[cycleway = lane]", "[bicycle_road = yes][parking][!segregated]",
                             '[highway = secondary][parking][!cycleway]',
                             '[highway = tertiary][parking][!cycleway]', '[highway = secondary][!cycleway][!parking]',
                             '[highway = tertiary][!cycleway][!parking]', '[highway = residential][parking][!cycleway]',
                             '[highway = residential][!cycleway][!parking]'])

    str = latex_tabular(df, 3)

    str2 = change_latex_str(str)

    str3 = tabular_to_table(str2, city)

    print(str3)


if __name__ == "__main__":
    main()
