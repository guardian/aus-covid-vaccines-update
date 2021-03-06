import pandas as pd 
from modules.yachtCharter import yachtCharter
import datetime 
import numpy as np 
import os, ssl
import math
pd.set_option("display.max_rows", None, "display.max_columns", None)

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

oz_json = 'https://interactive.guim.co.uk/2021/02/coronavirus-widget-data/aus-vaccines.json'
row_csv = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'

uk_json = 'https://raw.githubusercontent.com/guardian/interactive-covid-uk-tracker/master/assets/vaxx-data/vaxx-data-2020.json?token=AEFY5Q5MX26YEWK6X6UWGV3APYWLU'


# #%%
oz_pop = 25203000
# # https://ourworldindata.org/grapher/population

# # Sort out Australia's vaccination per hundred

oz = pd.read_json(oz_json)

oz['REPORT_DATE'] = pd.to_datetime(oz['REPORT_DATE'])
# oz = oz.sort_values(by ="REPORT_DATE", ascending=True)

oz['total_vaccinations_per_hundred'] = (oz["VACC_DOSE_CNT"] / oz_pop) * 100
oz['location'] = "Australia"
oz = oz.sort_values(by="REPORT_DATE", ascending=True)
last_date = datetime.datetime.strftime(oz['REPORT_DATE'].max(), "%Y-%m-%d")

# last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d %H:%M:%S")
# last_date = last_date.strftime("%Y-%m-%d")
# print(last_date)

oz.rename(columns={"REPORT_DATE":"date"}, inplace=True)

oz = oz[['location', 'date', 'total_vaccinations_per_hundred']]

oz = oz.loc[oz['total_vaccinations_per_hundred'] > 0]

# # Sort out everyone else from Our World in Data

our_world = pd.read_csv(row_csv, parse_dates=['date'])
our_world = our_world.sort_values(by="date", ascending=True)

graun_uk = pd.read_json(uk_json)
owid_uk = our_world.loc[our_world['location'] == "United Kingdom"]

graun_uk['allDosesByPublishDate'] = graun_uk['allDosesByPublishDate'].cumsum()
graun_uk.columns = ['date', 'total_vaccinations']

owid_uk = owid_uk.loc[owid_uk['date'] > "2021-01-10"]

owid_uk = owid_uk[['date', 'total_vaccinations']]

uk = graun_uk.append(owid_uk)


## Work out UK dose per hundred
uk_pop = 66650000
## https://ourworldindata.org/grapher/population

uk['location'] = "United Kingdom"
uk['total_vaccinations_per_hundred'] = (uk['total_vaccinations'] / uk_pop) * 100
uk = uk[['date','total_vaccinations_per_hundred', 'location']]

countries = ['Israel', 'Bhutan', 'United States', "Chile", "South Korea", "Japan"]
our_world = our_world.loc[our_world["location"].isin(countries)]

our_world = our_world[['date','total_vaccinations_per_hundred', 'location']]

our_world = our_world.append(uk)

# Append Australia to rest of the world

combined = our_world.append(oz)
combined = combined.sort_values(by="date", ascending=True)
combined['date'] = combined['date'].dt.strftime('%Y-%m-%d')

#%%
# Pivot the dataframe

pivoted = combined.pivot(index="date", columns='location')['total_vaccinations_per_hundred'].reset_index()
pivoted = pivoted.replace({'0':np.nan, 0:np.nan})
pivoted = pivoted.ffill(axis=0)

#%%
# print(pivoted)

includes = ["Australia", "United Kingdom"] + countries

#%%

sinceDayZero = pd.DataFrame()

for col in includes:

	start = pivoted[col].notna().idxmax()
	
	tempSeries = pivoted[col][start:]
	
	tempSeries = tempSeries.replace({0:np.nan})
	
	tempSeries = tempSeries.reset_index()
	
	tempSeries = tempSeries.drop(['index'], axis=1)
	
	sinceDayZero = pd.concat([sinceDayZero, tempSeries], axis=1)


## Automatically work out cutoff (current number of days in rollout rounded up to nearest 10):

rollout_begin = datetime.date(2021, 2, 22)
today = datetime.datetime.today().date()

days_running = today - rollout_begin
days_running = days_running.days

cut_off = math.ceil(days_running/10) * 10

# Cut dataset

upto = sinceDayZero[:cut_off].copy()

upto.to_csv('country-comparison.csv')

# print(upto['United Kingdom'])

def makeSince100Chart(df):
   
    template = [
            {
                "title": "Covid-19 vaccine doses per hundred people for selected countries",
                "subtitle": f"Showing up to the first {cut_off} days starting from the first day of recorded vaccinations in each country or region. Last updated {last_date }",
                "footnote": "",
                "source": "Covidlive.com.au, Our World in Data, The Guardian",
                "dateFormat": "",
                "yScaleType":"",
                "xAxisLabel": "Days since first vaccination",
                "yAxisLabel": "Doses per hundred people",
                "minY": "",
                "maxY": "",
                "periodDateFormat":"",
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
    chartId = [{"type":"linechart"}]
    df.fillna('', inplace=True)
    df = df.reset_index()
    chartData = df.to_dict('records')
    colors = ["#000000", "#e5005a","#f9b000","#ffe500",
    "#bbce00","#00a194","#61c3d9","#0099db","#b29163"]
    # print(since100.head())

    yachtCharter(template=template, data=chartData, chartId=[{"type":"linechart"}], options=[{"colorScheme":colors}], chartName="vaccines_per_hundred_reindexed_to_50_two")

makeSince100Chart(upto)

