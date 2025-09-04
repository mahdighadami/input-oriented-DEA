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

        total_needed = self.number_input + self.number_output
        if df.shape[1]-1 != total_needed:
            return ["Error", 
                f"Dimension mismatch: expected {self.number_input} inputs and {self.number_output} outputs (total {total_needed} columns), but file has {df.shape[1]-1} numeric columns."
            ]
        if df.isnull().any().any():
            return ["Error", "your file contains missing (NaN) values."]

        dmu_names = df[df.columns[0]].tolist()
        df = df.drop(df.columns[0], axis=1)

        if not np.issubdtype(df.values.dtype, np.number):
            return ["Error", "your file contains non-numeric values."]
        
        if (df.values < 0).any():
            return ["Error", "Inputs and outputs must be nonnegative. Negative values found."]
        
        self.df = df
        return dmu_names
    
    def process(self):
        inps = self.df.iloc[:, :self.number_input]
        outs = self.df.iloc[:, self.number_input:]
        x = inps.to_numpy()
        y = outs.to_numpy()
        return x, y
    
