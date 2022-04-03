import pandas as pd

p_csv = pd.read_csv('BD.csv', sep=';')
print(p_csv)

p_xlsx = pd.read_excel('BD.xlsx')
print(p_xlsx)
