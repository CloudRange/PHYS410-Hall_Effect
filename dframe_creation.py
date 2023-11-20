import numpy as np
import pandas as pd
from io import StringIO
import glob
import re
import os.path
import os

def create_df(path):
    """
    creates a general voltage dataframe
    """
    EXT = ".dat"
    files = [os.path.join(path, file) for file in os.listdir(path) 
             if EXT in file]
    headers = []

    with open(files[0], "r") as f:
        headers = np.array(f.readlines()[1].strip().split("\t"))

    headers = np.append(headers, ["MF (KGs)", "STD (KGs)"])

    # header renaming
    for idx, header in enumerate(headers):
        if header.startswith("V"):
            edge: str = re.findall(r"([1-4][1-4])", header)[0]
            headers[idx] = f"V{edge}{'_RF' if 'RF' in header else ''}_mV"
        elif not header.startswith("STD"):
            units = re.findall(r"\(([A-Za-z]{0,2}[A-Za-z])\)", header)[0]
            title = re.findall(r"([A-Z][A-Za-z]*) ", header)[0]
            headers[idx] = f"{title}_{units}"
        else:
            headers[idx] = f"e{headers[idx - 1]}"

    out = pd.DataFrame(columns = headers)

    for file in files:
        mfs = []
        text = []
        lines = []
        with open(file, "r") as f:
            lines = f.readlines()
            
        mfs = re.findall(r"(\d+\.\d{2,})", lines[0])
        text = [line.strip().split("\t") for line in lines[2:]]

        for t in text:
            w = np.array([float(el) for el in t])
            mfs  = np.array([float(mf) for mf in mfs])
            w = np.append(w, mfs)
            if len(w) != out.shape[1]:
                continue
            out.loc[len(out)] = w
    return out


def create_dataframe(path):
    files = glob.glob(path + "/*.dat")
    initialization = False
    main_data = []
    for i in files:
        with open(i, "rb") as file:
            binary_data = file.read()

        curr_data = str(binary_data).split("\\n")
        header = []
        if not initialization:
            # Get header
            header = curr_data[1].split("\\t")
            header[-1] = header[-1].replace("\\r", "")
            header = np.append(header, "MF (KGs)")
            header = np.append(header, "STD (KGs)")
            for j in curr_data[2:-1]:

                temp_line = j.split("\\t")
                temp_line[-1] = temp_line[-1].replace("\\r", "")
                regex_result = re.findall(r"(\d\.\d.)", curr_data[0])
                temp_line = np.append(temp_line, regex_result)
                main_data = np.vstack((header, temp_line))
            initialization = True
        else:
            for j in curr_data[2:-1]:
                temp_line = j.split("\\t")
                temp_line[-1] = temp_line[-1].replace("\\r", "")
                regex_result = re.findall(r"(\d\.\d.)", curr_data[0])
                temp_line = np.append(temp_line, regex_result)
                main_data = np.vstack((main_data, temp_line))

    df = pd.DataFrame(data=main_data[1:, :], columns=main_data[0])
    df.to_csv('Data.csv', encoding='utf-8', index = False)
    return df

if __name__ == "__main__":
    path = "Data_Testing/"
    print(create_dataframe(path))