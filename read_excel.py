import os
import numpy as np
import pandas as pd


class read_excel:
    def __init__(self, path, ninp, nout):
        self.file_path = path
        self.number_input = ninp
        self.number_output = nout
    
    def read_file(self):
        _, ext = os.path.splitext(self.file_path)
        ext = ext.lower()
        if ext == ".csv":
            df = pd.read_csv(self.file_path)
        elif ext in [".xlsx", ".xls"]:
            df = pd.read_excel(self.file_path)
        if df.isnull().any().any():
            raise ValueError(f"your file contains missing (NaN) values.")
        dmu_names = df[df.columns[0]].tolist()
        print(df)
        df = df.drop(df.columns[0], axis=1)
        if not np.issubdtype(df.values.dtype, np.number):
            raise ValueError(f"your file contains non-numeric values.")
        self.df = df
        return dmu_names
    
    def process(self):
        inps = self.df.iloc[:, :self.number_input]
        outs = self.df.iloc[:, self.number_input:]
        x = inps.to_numpy()
        y = outs.to_numpy()
        return x, y
    
