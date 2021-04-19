import os
import tabula
import pandas as pd 
import datetime
from modules.yachtCharter import yachtCharter

data_path = os.path.dirname(__file__) + "/data/"

## Read in Table from PDF

pdf = 'covid-19-vaccine-rollout-update-12-april-2021_0.pdf'

urlo = f'{data_path}{pdf}'
table = tabula.read_pdf(urlo,pages=7)[0]
table.columns = [x.replace("\r", " ") for x in table.columns]

table.rename(columns={'Unnamed: 0':"Jurisdiction", "Estimated Dose Utilisation % (See note)": "Estimated Dose Utilisation"}, inplace=True)
table['Jurisdiction'] = table['Jurisdiction'].str.replace("\r", " ")


table = table[['Jurisdiction','Available (delivered weeks 1-6, until 4 April)','Administered (weeks 1-7, until 11 April)']]
table.rename(columns={'Available (delivered weeks 1-6, until 4 April)': "Available by 4 April", 'Administered (weeks 1-7, until 11 April)':"Administered by 11 April"}, inplace=True)

table["Available by 4 April"] = table["Available by 4 April"].str.replace(",", "")
table["Administered by 11 April"] = table["Administered by 11 April"].str.replace(",", "")

table["Available by 4 April"] = pd.to_numeric(table["Available by 4 April"])
table["Administered by 11 April"] = pd.to_numeric(table["Administered by 11 April"])

include = ['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'NT', 'ACT','Commonwealth Aged Care and Disability',
 'Commonwealth Primary Care', 'Total']

table = table.loc[table['Jurisdiction'].isin(include)]

# table = table[['Jurisdiction', "Estimated Dose Utilisation"]]
# table['Estimated Dose Utilisation'] = table['Estimated Dose Utilisation'].str.replace("Fully utilised*", "100")
# table['Estimated Dose Utilisation'] = table['Estimated Dose Utilisation'].str.replace("*", "")
# table['Estimated Dose Utilisation'] = table['Estimated Dose Utilisation'].str.replace("%", "")

# table['Estimated Dose Utilisation'] = pd.to_numeric(table['Estimated Dose Utilisation'])

print(table)

def makeChart(df):
   
    template = [
            {
                "title": "Percentage of available Covid-19 vaccines administered by state",
                "subtitle": f"",
                "footnote": "",
                "source": "Covidlive.com.au, Our World in Data ",
                "dateFormat": "",
                "yScaleType":"",
                "xAxisLabel": "Days since first vaccination",
                "yAxisLabel": "Doses per hundred people",
                "margin-left": "25",
                "margin-top": "15",
                "margin-bottom": "20",
                "margin-right": "10",
                "breaks":"no"
            }
        ]
    key = []
    periods = []
    labels = []
    chartId = [{"type":"groupedbar"}]
    df.fillna('', inplace=True)
    # df = df.reset_index()
    chartData = df.to_dict('records')
    # print(since100.head())

    yachtCharter(template=template, data=chartData, chartId=chartId, options=[{"colorScheme":"guardian"}], chartName="vaccine_utilisation_by_juridisction")

makeChart(table)

with open(f"{data_path}state_by_state_grouped.csv", "w") as f:
    table.to_csv(f, index=False, header=True)
