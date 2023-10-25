import numpy as np
import pandas as pd
from io import StringIO
import glob
import re


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
    return df

path = "Data_Testing/"
print(create_dataframe(path))