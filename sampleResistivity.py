import numpy as np
import pandas as pd
from io import StringIO
import glob
import re


def get_fx_approximation(x):
    return (np.cosh(np.log(x) / 2.403)) ** (-1)


def get_sampleResistivity(R43, R23, d, f):
    return ((np.pi * d) / np.log(2)) * ((R43 + R23) / 2) * f


def append_resistivity_x(df, x, p):
    df["R43 / R23"] = x
    df["p"] = p
    df.to_csv('Data.csv', encoding='utf-8', index=False)



df = pd.read_csv("Data.csv")

d = 350 * 1e-6  # +- 25*e-6
R43 = df["V(43) (mV)"] / df["I (mA)"]
R23 = df["V(23) (mV)"] / df["I (mA)"]

print(R43)
print(R23)

x = R43 / R23
f = get_fx_approximation(x)

p = get_sampleResistivity(R43, R23, d, f)

append_resistivity_x(df, x, p)