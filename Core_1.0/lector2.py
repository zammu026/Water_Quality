# -*- coding: utf-8 -*-
"""
Created on Mon Nov  3 16:32:05 2025

@author: Cisneros
"""
import pandas as pd
path= "MEDIDA1.txt"
def load_table(path):
    df = pd.read_csv(path, sep=r"\s+", header=16, encoding='latin1')
    wl = df.iloc[:, 0].values
    val = df.iloc[:, 1].values
    return wl,val

wl,val=load_table(path)
print(wl,val)