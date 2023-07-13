import glob
import pandas as pd

# Reads and Gets data
def get_data():
    all_filenames = glob.glob('Data/*')
    all_data = {}
    for filename in all_filenames:
        table = pd.read_csv(filename, skiprows=3, delimiter='\t')
        table = table.drop("Unnamed: 18", axis =1)
        table["B-Field (Gauss)"] = pd.to_numeric(table["B-Field (Gauss)"],
                                                 errors="coerce")
        pos_B = table[table["B-Field (Gauss)"] > 2000]
        neg_B = table[table["B-Field (Gauss)"] < 0]
        zero_B = pd.concat([table, pos_B, neg_B]).drop_duplicates(keep=False)
        #all_data[filename[5:][:-4]] = table
        all_data[filename[5:][:-4]] = {"-B":neg_B,
                                       "0B":zero_B,
                                       "+B":pos_B}
    return all_data

all_data = get_data()
