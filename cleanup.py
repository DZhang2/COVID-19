import pandas as pd
import numpy as np
import json
import os
import matplotlib.pyplot as plt

def load_file(path):
    file = pd.read_csv(path)
    return file

#date in format mm-dd-yyyy
def getDailyReport(date):
    return load_file("./csse_covid_19_data/csse_covid_19_daily_reports/" + date)

#note up until 3/21, Country/Region is used
def cleanTimeSeriesWorld(df, date):
    confirmed = df.groupby("Country_Region")["Confirmed"].sum()
    deaths = df.groupby("Country_Region")["Deaths"].sum()
    mortality_rate = pd.DataFrame(data=deaths/confirmed*100, columns=["Mortality Rate"])
    res = pd.concat([confirmed, deaths, mortality_rate], axis=1)
    res["Date"] = date
    res = res[["Date", "Confirmed", "Deaths", "Mortality Rate"]]
    res = res.sort_values(by='Confirmed', ascending=False)
    return res

def cleanTimeSeriesWorldOld(df, date):
    country = df.groupby("Country/Region")
    confirmed = country["Confirmed"].sum()
    deaths = country["Deaths"].sum()
    mortality_rate = pd.DataFrame(data=deaths/confirmed*100, columns=["Mortality Rate"])
    res = pd.concat([confirmed, deaths, mortality_rate], axis=1)
    res.rename(index={"Mainland China": "China"}, inplace=True)
    res["Date"] = date
    res = res[["Date", "Confirmed", "Deaths", "Mortality Rate"]]
    res = res.sort_values(by='Confirmed', ascending=False)
    return res

def cleanTimeSeriesCountry(df, country):
    nation = df[df["Country_Region"]==country]
    confirmed = nation.groupby("Province_State")["Confirmed"].sum()
    deaths = nation.groupby("Province_State")["Deaths"].sum()
    mortality_rate = pd.DataFrame(data=deaths/confirmed*100, columns=["Mortality Rate"])
    res = pd.concat([confirmed, deaths, mortality_rate], axis=1)
    res = res.sort_values(by='Confirmed', ascending=False)
    return res

def cleanTimeSeriesState(df, state):
    st = df[df["Province_State"]==state][["Admin2", "Confirmed", "Deaths"]]
    st["Mortality Rate"] = np.where(st["Confirmed"] == 0, 0, st["Deaths"]/st["Confirmed"]*100)
    st = st.sort_values(by="Confirmed", ascending=False)
    st.columns = ["County", "Confirmed", "Deaths", "Mortality Rate"]
    return st

def cleanTimeSeriesUS(df):
    us = df[df["Country_Region"]=="US"]
    confirmed = us.groupby("Province_State")["Confirmed"].sum()
    deaths = us.groupby("Province_State")["Deaths"].sum()
    mortality_rate = pd.DataFrame(data=deaths/confirmed*100, columns=["Mortality Rate"])
    res = pd.concat([confirmed, deaths, mortality_rate], axis=1)
    res = res.sort_values(by='Confirmed', ascending=False)
    return res

def cleanTimeSeriesGA(df):
    ga = df[df["Province_State"]=="Georgia"][["Admin2", "Confirmed", "Deaths"]]
    ga["Mortality Rate"] = ga["Deaths"]/ga["Confirmed"]*100
    ga = ga.sort_values(by="Confirmed", ascending=False)
    ga.columns = ["County", "Confirmed", "Deaths", "Mortality Rate"]
    return ga

def combineTimeSeries():
    daily_report_files = os.listdir('./csse_covid_19_data/csse_covid_19_daily_reports')
    complete = {}
    for i in range(0, len(daily_report_files)):
        useOld = False
        date_file = daily_report_files[i]
        date = date_file.split('.')[0]
        if date_file[0] != '0':
            continue
        if date_file[1] == '1' or date_file[1] == '2':
            useOld = True
        if date_file[1] == '3':
            if date_file[3] == '1' or date_file[3] == '0':
                useOld = True
            elif date_file[3] == '2' and (date_file[4] == '0' or date_file[4] == '1'):
                useOld = True
        afile = getDailyReport(date_file)
        df = 0
        df = cleanTimeSeriesWorldOld(afile, date) if useOld else cleanTimeSeriesWorld(afile, date)
        df.to_csv(f"./cleaned_data/daily/countries/(world)_{date_file}")
        complete[date_file] = df.to_json()
    return complete

def createCompleteTimeSeries():
    daily_report_files = os.listdir('./csse_covid_19_data/csse_covid_19_daily_reports')
    combined_df = 0
    for i in range(0, len(daily_report_files)):
        useOld = False
        date_file = daily_report_files[i]
        date = date_file.split('.')[0]
        if date_file[0] != '0':
            continue
        if date_file[1] == '1' or date_file[1] == '2':
            useOld = True
        if date_file[1] == '3':
            if date_file[3] == '1' or date_file[3] == '0':
                useOld = True
            elif date_file[3] == '2' and (date_file[4] == '0' or date_file[4] == '1'):
                useOld = True
        afile = getDailyReport(date_file)
        current_df = cleanTimeSeriesWorldOld(afile, date) if useOld else cleanTimeSeriesWorld(afile, date)
        combined_df = pd.concat([combined_df, current_df], axis=0) if i != 0 else current_df
    combined_df = combined_df.sort_values(by="Date")
    combined_df.to_csv(f"./cleaned_data/accumulated/fullTimeSeries.csv")


apr12 = getDailyReport("04-12-2020.csv")
apr15 = getDailyReport("04-15-2020.csv")
jan31 = getDailyReport("01-31-2020.csv")

world = cleanTimeSeriesWorld(apr15, "04-15-2020")
us = cleanTimeSeriesUS(apr12)
ny = cleanTimeSeriesState(apr12, "New York")
china = cleanTimeSeriesCountry(apr12, "China")
us = cleanTimeSeriesCountry(apr12, "US")

# us.plot(kind="bar", title="US Data")
# plt.show()

createCompleteTimeSeries()
#complete = combineTimeSeries()
#json.dump(complete, open("./cleaned_data/accumulated/fullTimeSeries.json", 'w'))


