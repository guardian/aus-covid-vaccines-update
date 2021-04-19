import os
import tabula
import pandas as pd 
import datetime

data_path = os.path.dirname(__file__) + "/data/"

## Read in Table from PDF

pdf = 'covid-19-vaccine-rollout-update-12-april-2021_0.pdf'

urlo = f'{data_path}{pdf}'
table = tabula.read_pdf(urlo,pages=7)[0]
table.columns = [x.replace("\r", " ") for x in table.columns]

## Read in inferred vaccine supply


supply = pd.read_csv(f"{data_path}inferred_vaccine_supply.csv", parse_dates=["Month"])
# Round to nearest million
supply["Allocated"] = round(supply["Allocated"], -6)
supply.columns = ["Month", "Forecast supply"]



table = table[['Unnamed: 0', 'Available (delivered weeks 1-6, until 4 April)']]
table.rename(columns={'Unnamed: 0':"Jurisdiction"}, inplace=True)

table['Jurisdiction'] = table['Jurisdiction'].str.replace("\r", " ")

print(table)
print(table.columns)
print(supply)








# Initial cleaning

# supply = pd.read_csv(f"{data_path}inferred_vaccine_supply.csv", names=["Month", "Allocated"])
# count = 3
# for row in supply.index:
#     supply.loc[row, 'Month'] = f"{count}/21"
#     count += 1

# with open(f"{data_path}inferred_vaccine_supply.csv", "w") as f:
#     supply.to_csv(f, index=False, header=True)

