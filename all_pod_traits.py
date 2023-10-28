# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 22:24:58 2023

@author: nkgar
"""

import os
import pandas as pd
import re

folder = "C:/Users/nkgar/Desktop/GWAS/test_files/"
# Listing the files of a folder
print('Before rename')
files = os.listdir(folder)
print(files)

dict_tests = {}

for i in files:
    j = i.split(".")[0]
    print(j)
    dict_tests[j] = pd.read_csv("C:/Users/nkgar/Desktop/GWAS/test_files/"+i)
    
cols_to_extract = ["Year", "Location", "NC_Accession", "Plot"]

extracted_dfs = []

for key, df in dict_tests.items():
    if "Block" in df.columns:
        extracted_df = df.loc[:, cols_to_extract + ["Block"]]
    else:
        extracted_df = df.loc[:, cols_to_extract]
    extracted_df["Dataframe"] = key
    extracted_dfs.append(extracted_df)
    
final_df = pd.concat(extracted_dfs, axis = 0)

#final_df = final_df.dropna()

final_df.reset_index(drop=True, inplace=True)

final_df['test_id'] = final_df['Dataframe'].apply(lambda x: x.split('-')[0] + '-' + x.split('-')[1]) + '-' + final_df['Plot'].astype(str)

final_df['test_id'] = final_df['test_id'].str.replace('\.0$','')

#final_df['NC_Accession'] = final_df['NC_Accession'].apply(lambda x: re.sub(r'HTS IL-0(\d)', r'HTS IL-\1', x))



pheno_df = pd.read_csv("./pod_traits.csv")

pheno_df = pheno_df.rename(columns={"ID":"test_id"})

pheno_df['test_id'] = pheno_df['test_id'].str.replace('.jpg.csv','')
pheno_df['test_id'] = pheno_df['test_id'].str.replace('-mixed','')

merged_pa = pd.merge(final_df, pheno_df, on='test_id', how = 'left')

merged_pa = merged_pa.dropna(subset=["pod_width"])

merged_pa["Block"].fillna(merged_pa["Plot"].astype(str).str[0], inplace = True)

col_list = ['Year', 'Location', 'NC_Accession',
                           'Plot', 'pod_area','pod_length','lw_ratio',
                           'pod_per','pod_width','Block']


pa_out = merged_pa[col_list]
pa_out.to_csv("pod_traits_all_1019.csv")


import statsmodels.api as sm
import statsmodels.formula.api as smf

md=smf.mixedlm("mean_pa ~ (Year/Block) + (NC_Accession:Location)", data = pa_out, groups = pa_out["NC_Accession"])
mdf = md.fit(method=["lbfgs"])
print(mdf.summary())
