# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 11:22:01 2023

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

summary_df = final_df.describe(include='all')

#%% creating 122 list
small_list = pd.read_csv("C:/Users/nkgar/Desktop/GWAS/122_acc.csv")

test_small = final_df.merge(small_list[["NC_Accession"]], on = "NC_Accession", how="inner")


test_small['test_id'] = test_small['Dataframe'].apply(lambda x: x.split('-')[0] + '-' + x.split('-')[1]) + '-' + test_small['Plot'].astype(str)

test_small['test_id'] = test_small['test_id'].str.replace('\.0$','')

test_small['NC_Accession'] = test_small['NC_Accession'].apply(lambda x: re.sub(r'HTS IL-0(\d)', r'HTS IL-\1', x))

pheno_df = pd.read_csv("./raw_pheno.csv")

pheno_df = pheno_df.rename(columns={"ID":"test_id"})

pheno_df['test_id'] = pheno_df['test_id'].str.replace('.jpg','')

merged_small = pd.merge(test_small, pheno_df, on='test_id', how = 'left')

merged_small = merged_small.dropna(subset=["mean_width_el"])

merged_small["Block"].fillna(merged_small["Plot"].astype(str).str[0], inplace = True)

col_list = ['Year', 'Location', 'NC_Accession',
                           'Plot', 'mean_width_el','Block']


gap_122_out = merged_small[col_list]

gap_122_out.to_csv("./122_all_pheno.csv")





#%%
final_df['test_id'] = final_df['Dataframe'].apply(lambda x: x.split('-')[0] + '-' + x.split('-')[1]) + '-' + final_df['Plot'].astype(str)

final_df['test_id'] = final_df['test_id'].str.replace('\.0$','')

final_df['NC_Accession'] = final_df['NC_Accession'].apply(lambda x: re.sub(r'HTS IL-0(\d)', r'HTS IL-\1', x))


pheno_df = pd.read_csv("./raw_pheno.csv")

pheno_df = pheno_df.rename(columns={"ID":"test_id"})

pheno_df['test_id'] = pheno_df['test_id'].str.replace('.jpg','')

merged = pd.merge(final_df, pheno_df, on='test_id', how = 'left')

merged = merged.dropna(subset=['mean_width_el'])

merged["Block"].fillna(merged_small["Plot"].astype(str).str[0], inplace = True)

col_list = ['Year', 'Location', 'NC_Accession',
                           'Plot', 'mean_width_el','Block']

gap_all_out = merged[col_list]

gap_all_out.to_csv("./all_pheno.csv")


merged['avg_width_el'] = merged.groupby('NC_Accession')['mean_width_el'].transform('mean')
merged['avg_width_re'] = merged.groupby('NC_Accession')['mean_width_re'].transform('mean')

merged1 = merged.drop_duplicates(subset="NC_Accession")

selected = merged1[["NC_Accession", "avg_width_el", "avg_width_re"]]
selected.reset_index(drop=True, inplace=True)

geno_df = pd.read_csv("./filtered_geno_pivot.csv")
geno_df = geno_df.rename(columns={"names":"NC_Accession"})

geno_df['NC_Accession'] = geno_df['NC_Accession'].apply(lambda x: re.sub(r'HTS IL-0(\d)', r'HTS IL-\1', x))

geno_df = geno_df.drop_duplicates(subset = "NC_Accession")

p_and_g = pd.merge(selected, geno_df, on="NC_Accession", how = "left")

p_and_g.to_csv("p_and_g.csv", index = False)
