import pandas as pd
import os
import ast
import re

def csv_cleanup(folder):
    data = pd.DataFrame()
    for foldername, subfolders, filenames in os.walk(folder):
        for filename in filenames:
            file_path = os.path.join(foldername,filename)
            df = pd.read_csv(file_path, encoding='utf-8', delimiter=';')
            data = pd.concat([data,df])
    
    data.to_csv(f'{folder}/all_product_data.csv', sep=';',encoding='utf-8',index=False)






def product_id_sep(data):
    df = pd.read_csv(data, encoding='utf-8',delimiter=';')
    df = df.rename(columns={'0':'NUMMER','1':'BESCHREIBUNG'})
    df = df[['NUMMER', 'BESCHREIBUNG']]
    df['NUMMER'] = df['NUMMER'].map(ast.literal_eval) 
    cleaned_table = {}
    for num,value in zip(df['NUMMER'],df['Beschreibung']):

        if len(num) == 1:
            num = num[0].strip('Nr.')
            num = num.strip()
            cleaned_table[num] = value
        elif len(num) > 1:
            for item in num:
                item = item.strip('Nr.')
                item = item.strip()
                cleaned_table[item] = value
        else:
            continue
    cleaned_data = pd.DataFrame(list(cleaned_table.items()),columns=['NUMMER','BESCHREIBUNG'])

    return cleaned_data


