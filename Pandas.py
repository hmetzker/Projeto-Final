import pandas as pd
#from openpyxl import Workbook, load_workbook

p_csv = pd.read_csv('BD.csv', sep=';')
print(p_csv)

p_xlsx = pd.read_excel('BD.xlsx')
print(p_xlsx)

#p_xlsx = load_workbook('BD.xlsx')
#print(p_xlsx)
