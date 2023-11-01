import numpy as np
import pandas as pd
from io import StringIO
import glob
import re




def create_dataframe_rho(path, fnameout):
    files = glob.glob(path + "/*.dat")
    initialization12_43 = False
    initialization14_23 = False
    main_data12_43 = []
    main_data14_23 = []

    for i in files:
        with open(i, "rb") as file:
            binary_data = file.read()

        curr_data = str(binary_data).split("\\n")
        df_type = re.findall(r"(I\d\d_V\d\d)", i)[0]
        header = []
        print(i)
        if df_type == "I12_V43":
            if not initialization12_43:
                # Get header
                header = curr_data[1].split("\\t")
                header[-1] = header[-1].replace("\\r", "")
                header = np.append(header, "MF (KGs)")
                header = np.append(header, "STD (KGs)")
                for j in curr_data[2:-1]:

                    temp_line = j.split("\\t")
                    temp_line[-1] = temp_line[-1].replace("\\r", "")
                    regex_result = re.findall(r"(\d\.\d.)", curr_data[0])
                    temp_line = np.append(temp_line[:-2], regex_result)
                    main_data12_43 = np.vstack((header, temp_line))
                initialization12_43 = True
            else:
                for j in curr_data[2:-1]:
                    temp_line = j.split("\\t")
                    temp_line[-1] = temp_line[-1].replace("\\r", "")
                    regex_result = re.findall(r"(\d\.\d.)", curr_data[0])
                    temp_line = np.append(temp_line[:-2], regex_result)
                    main_data12_43 = np.vstack((main_data12_43, temp_line))
        elif df_type == "I14_V23":
            if not initialization14_23:
                # Get header
                header = curr_data[1].split("\\t")
                header[-1] = header[-1].replace("\\r", "")
                header = np.append(header, "MF (KGs)")
                header = np.append(header, "STD (KGs)")
                for j in curr_data[2:-1]:
                    temp_line = j.split("\\t")
                    temp_line[-1] = temp_line[-1].replace("\\r", "")
                    regex_result = re.findall(r"(\d\.\d.)", curr_data[0])
                    temp_line = np.append(temp_line[:-2], regex_result)
                    main_data14_23 = np.vstack((header, temp_line))
                initialization14_23 = True
            else:
                for j in curr_data[2:-1]:
                    temp_line = j.split("\\t")
                    temp_line[-1] = temp_line[-1].replace("\\r", "")
                    regex_result = re.findall(r"(\d\.\d.)", curr_data[0])
                    temp_line = np.append(temp_line[:-2], regex_result)
                    main_data14_23 = np.vstack((main_data14_23, temp_line))

    df_12_43 = pd.DataFrame(data=main_data12_43[1:, :], columns=main_data12_43[0])
    df_14_23 = pd.DataFrame(data=main_data14_23[1:, :], columns=main_data14_23[0])

    if len(fnameout) != 2:
        fnameout = ['Data_12_43.csv', 'Data_14_23.csv']
    
    df_12_43.to_csv(fnameout[0], encoding='utf-8', index=False)
    df_14_23.to_csv(fnameout[1], encoding='utf-8', index=False)

    return

if __name__ == "__main__":
    path = "IV_Data/"
    
    create_dataframe_rho(path)
