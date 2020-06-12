import pandas as pd

file = 'C:/Users/wchen/Downloads/Book1.xlsx'

xl = pd.ExcelFile(file)

df1 = xl.parse('Sheet1')

print(len(df1))
df1.drop_duplicates(inplace=True)
print(len(df1))

df1.to_csv('med_data.csv')