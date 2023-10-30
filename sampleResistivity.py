import numpy as np
import pandas as pd
from io import StringIO
import glob
import re


def get_fx_approximation(x):
    return (np.cosh(np.log(x) / 2.403)) ** (-1)


def get_sampleResistivity(R43, R23, d, f):
    return ((np.pi * d) / np.log(2)) * ((R43 + R23) / 2) * f


def df_resistivity(T1, T2, x, p):
    df = pd.DataFrame()
    df["T_12_43"] = T1
    df["T_14_23"] = T2
    df["R43/R23"] = x
    df["rho"] = p
    df.to_csv('Resistivity_Data.csv', encoding='utf-8', index=False)


df_12_43 = pd.read_csv("Data_12_43.csv")
df_12_43 = df_12_43.sort_values(by=['Temperature (C)'])

df_14_23 = pd.read_csv("Data_14_23.csv")
df_14_23 = df_14_23.sort_values(by=['Temperature (C)'])

d = 350 * 1e-6  # +- 25*e-6
R43 = df_12_43["V(43) (mV)"] / df_12_43["I(12) (mA)"]
R23 = df_14_23["V(23) (mV)"] / df_14_23["I(14) (mA)"]

x = R43 / R23
f = get_fx_approximation(x)

p = get_sampleResistivity(R43, R23, d, f)


df_resistivity(df_12_43['Temperature (C)'], df_14_23['Temperature (C)'], x, p)
