import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def main():
    df = pd.read_csv("highway_cities.csv")

    fig, ax = plt.subplots()

    x = np.arange(len(df["city"]))
    width = 0.25

    rects1 = ax.barh(x - width, df["s_secondary"], width, label='secondary')
    rects2 = ax.barh(x, df["s_tertiary"], width, label='tertiary')
    rects3 = ax.barh(x + width, df["s_residential"], width, label='residential')

    ax.set_yticks(x, df["city"])
    ax.invert_yaxis()

    ax.set_xticks(np.arange(0, 1.01, step=0.2))
    ax.set_xlabel("safety score")

    ax.set_title('Safety of highway types by city')
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    ax.bar_label(rects3, padding=3)

    fig.tight_layout()

    #plt.show()
    fig.savefig(f'highways_safety.png')


if __name__ == "__main__":
    main()
