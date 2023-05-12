import json
import pandas as pd
import re
import os

root = r'C:\Users\Kauan\Desktop\exercicio_ascential\data-eng-test'
files = os.listdir(r'C:\Users\Kauan\Desktop\exercicio_ascential\data-eng-test')
data = []

# Extração de dados dos arquivos JSON para Dicionario

for file in files:
    try:
        f = open(root + '\\' + file, encoding='Latin1')
        fr = f.read()
        d = json.loads(fr)
        d_arr = d['assortment'][0]
        d_select = [ i for i in d_arr.items() if i[0] in ['idRetailerSKU','available','unavailable','priceVariation','modifiedDate']]
        d_dict = dict(d_select)
        if not d_dict['available']:
            d_dict['priceVariation']=0
        if d_dict['priceVariation'] == None:
            continue
        data.append(d_dict)
    except Exception as e:
        print(e)
        print(file)

# Dicionario para Dataframe 

df = pd.DataFrame(data)

# Calculo de Metricas

# Top 10 price variation
df_dedup = df.drop_duplicates()
df_grp_last = df.groupby(by=['idRetailerSKU']).max('modifiedDate')
df_grp_last = df_grp_last.apply(lambda x: abs(df_grp_last['priceVariation']))

df_metric_var = df_grp_last['priceVariation'].nlargest(n=10)

# Top 10 unavaialability
df_unavail = df[df['unavailable']==True]
df_metric_unavail = df_unavail.groupby(by=['idRetailerSKU']).count().nlargest(n=10,columns=['unavailable'])
df_metric_unavail = df_metric_unavail['unavailable']

print('\nTop 10 price variation:\n')
print(df_metric_var)
print('\nTop 10 unavaialability:\n')
print(df_metric_unavail)

