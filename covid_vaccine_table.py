import pandas as pd 
from modules.yachtCharter import yachtCharter
import datetime
import os
data_path = os.path.dirname(__file__) + "/data/"

row_csv = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
locations = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/locations.csv'

locations = pd.read_csv(locations)
locations = locations[['location', 'vaccines']]

owid = pd.read_csv(row_csv)

latest = owid.drop_duplicates(subset="location",keep="last")

latest['date'] = pd.to_datetime(latest['date'])
updated_date = datetime.datetime.strftime(latest['date'].max(), "%Y-%m-%d")


df = latest[['location', 'total_vaccinations', 'total_vaccinations_per_hundred', 'daily_vaccinations_per_million']]
exclude = ["World", "Oceania", "Asia", "Europe", "European Union", "South America", "Africa", "North America", "United Kingdom"]

df = df.loc[~df['location'].isin(exclude)]


df.columns = ["Country", "Total vaccinations", "Vaccinations per hundred", "Daily vaccinations per million"]
df['Vax_numeric'] = pd.to_numeric(df["Vaccinations per hundred"])
df = df.sort_values(by="Vax_numeric", ascending=False)
df['Rank'] = df['Vax_numeric'].rank(ascending=False, method="first")

print(df.loc[df['Country'] == "Papua New Guinea"])

df = pd.merge(df, locations, left_on="Country", right_on="location", how="left")
df.drop(columns=['Vax_numeric', "location"], inplace=True)

df = df.dropna()

df = df[['Country', 'Rank', 'Vaccinations per hundred', 'Total vaccinations', 'Daily vaccinations per million',  'vaccines']]

df.rename(columns={"vaccines": "Vaccines used"}, inplace=True)

# print(df.loc[df['Country'] == "Australia"])
print(df.loc[df['Country'] == "Papua New Guinea"])

def makeTable(df):
	
    template = [
            {
                "title": "Covid-19 vaccinations around the world",
                "subtitle": f"Countries are ranked by the number of vaccinations administered per hundred people. Last updated {updated_date}",
                "footnote": "",
                "source": "Our World In Data",
                "yScaleType":"",
                "minY": "0",
                "maxY": "",
                "x_axis_cross_y":"",
                "periodDateFormat":"",
                "margin-left": "50",
                "margin-top": "30",
                "margin-bottom": "20",
                "margin-right": "10"
            }
        ]
    key = []
    # labels = []
    df.fillna("", inplace=True)
    chartData = df.to_dict('records')
    labels = []


    yachtCharter(template=template, labels=labels, data=chartData, chartId=[{"type":"table"}], 
    options=[{"colorScheme":"guardian","format": "scrolling","enableSearch": "TRUE","enableSort": "TRUE"}], chartName="vaccines_country_table")

# makeTable(df)

# with open(f"{data_path}covid_vaccine_table.csv", "w") as f:
#     df.to_csv(f, index=False, header=True)


# df['Total_numeric'] = pd.to_numeric(df["Total vaccinations"])
# df = df.sort_values(by="Total_numeric", ascending=False)
# df['Total_rank'] = df['Total_numeric'].rank(ascending=False, method="first")

# print(df)
# print(df.loc[df['Country'] == "Australia"])

# same_boat = df.loc[(df['Vaccines used'].str.contains("Pfizer")) & (df['Vaccines used'].str.contains("BioNTech"))]
# pd.set_option("display.max_rows", None, "display.max_columns", None)
# same_boat['Count'] = 1
# same_boat['Count'] = same_boat['Count'].cumsum()
# same_boat = same_boat[['Country', 'Vaccinations per hundred', "Count"]]
# print(same_boat)

# print(df['Vaccines used'].str.split(","))
# print(type(df['Vaccines used'].str.split(",")))
# df['Num_vax'] = df['Vaccines used'].str.split(",").str.len()

# import matplotlib.pyplot as plt 
# import seaborn as sns 

# sns.lineplot(x="Rank", y="Vaccinations per hundred",
#                 hue="Num_vax",
#                 data=df)

# sns.countplot(x="Vaccinations per hundred", hue="Num_vax" , data=df)
# sns.kdeplot(data=df, x="Rank", hue="Num_vax")
# sns.swarmplot(y="Vaccinations per hundred", x="Num_vax", data=df)
# sns.scatterplot(y="Vaccinations per hundred", x="Num_vax", data=df)
# sns.regplot(y="Vaccinations per hundred", x="Num_vax", data=df)

# print(df.loc[df['Num_vax'] == 5].shape)
# print(df.loc[df['Num_vax'] == 4].shape)
# print(df.loc[df['Num_vax'] == 3].shape)
# print(df.loc[df['Num_vax'] == 2].shape)

# plt.show()


# print(df)