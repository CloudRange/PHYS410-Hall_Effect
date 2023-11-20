import pandas as pd
import numpy as np


def compress(df, column, avg_pts, tol = 0.5):
    """
    compresses the frame by averaging rows with close-enough
    row values for the selected column around the avg_pts,
    within +/- tol.

    returns a compressed data frame.
    """

    out = pd.DataFrame(columns = df.columns)

    for pt in avg_pts:
        # get values in tolerance
        _temp_df = df[((df[column] - tol) < pt) 
                      & (pt < (df[column] + tol))]

        l = len(out)
        out.loc[l] = _temp_df.mean(axis = 0)

        for col_idx, col in enumerate(df.columns):
            if col.startswith("STD"):
                out.loc[l, col] =\
                np.std(_temp_df, axis = 0)[col_idx - 1]

    return out
        
    

    

    