import pandas as pd

data_set = "nyc_leading_cause_of_death.csv"


def create_adj_csv():
    
    new_df = pd.DataFrame()
    old_df = pd.read_csv(data_set, sep=",")

    for idx, row in old_df.iterrows():
        print(f"At index {idx} of {len(old_df)}, length of new_df is {len(new_df)}")
        if row['Deaths'] != ".":
            n_dups = int(row['Deaths'])
            print(f"Duplicating {n_dups} times...")
            for i in range(0, n_dups):
                new_df = new_df.append(row, ignore_index=True)

    new_df.to_csv("nyc_leading_cause_of_death_adj.csv")


create_adj_csv()
