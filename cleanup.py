import pandas as pd
import numpy as np
import os

def load_file(path):
    file = pd.read_csv(path)
    return file

#date in format mm-dd-yyyy
def getDailyReport(date):
    return load_file("./csse_covid_19_data/csse_covid_19_daily_reports/" + date + ".csv")

apr12 = getDailyReport("04-12-2020")

def cleanTimeSeriesWorld(df):
    confirmed = df.groupby("Country_Region")["Confirmed"].sum()
    deaths = df.groupby("Country_Region")["Deaths"].sum()
    mortality_rate = pd.DataFrame(data=deaths/confirmed*100, columns=["Mortality Rate"])
    res = pd.concat([confirmed, deaths, mortality_rate], axis=1)
    res = res.sort_values(by='Confirmed', ascending=False)
    return res

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



world = cleanTimeSeriesWorld(apr12)
us = cleanTimeSeriesUS(apr12)
ny = cleanTimeSeriesState(apr12, "New York")
print(ny)


