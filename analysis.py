import numpy as np
import pandas as pd
import csv
import time
import matplotlib.pyplot as plt
import json
import os

def load_file(path):
    file = pd.read_csv(path)
    return file

def getDictList(path):
    reader = csv.DictReader(open(path))
    reader = [dict(line) for line in reader]
    return reader

confirmed_US = load_file("./csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")
apr8 = load_file("./csse_covid_19_data/csse_covid_19_daily_reports/04-08-2020.csv")

def printData(date):
    confirmed = deaths = recovered = 0
    usC = usD = usR = 0
    wdC = wdD = wdR = 0
    for i in range(len(date)):
        if date.loc[i, 'Province_State'] == 'Georgia':
            confirmed += date.loc[i, 'Confirmed']
            deaths += date.loc[i, 'Deaths']
            recovered += date.loc[i, 'Recovered']
        if date.loc[i, 'Country_Region'] == 'US':
            usC += date.loc[i, 'Confirmed']
            usD += date.loc[i, 'Deaths']
            usR += date.loc[i, 'Recovered']
        wdC += date.loc[i, 'Confirmed']
        wdD += date.loc[i, 'Deaths']
        wdR += date.loc[i, 'Recovered'] 
    dr = deaths/confirmed*100
    udr = usD/usC*100
    wdr = wdD/wdC*100
    print(f'GA confirmed: {confirmed}, deaths: {deaths}, recovered: {recovered}, mr: {dr}')
    print(f'US confirmed: {usC}, deaths: {usD}, recovered: {usR}, mr: {udr}')
    print(f'World confirmed: {wdC}, deaths: {wdD}, recovered: {wdR}, mr: {wdr}')

def getCountryDict(date):
    countries = {}
    for i in range(len(date)):
        confirmed = int(date.loc[i, 'Confirmed'])
        deaths = int(date.loc[i, 'Deaths'])
        country = date.loc[i, 'Country_Region']
        mortality = 0
        if country in countries:
            countries[country]['confirmed'] += confirmed
            countries[country]['deaths'] += deaths
            countries[country]['mortality rate'] = 0
        else:
            countries[country] = {'confirmed': confirmed, 'deaths': deaths, 'mortality rate': mortality}
    for country in countries:
        c = countries[country]['confirmed']
        d = countries[country]['deaths']
        countries[country]['mortality rate'] = d/c*100
    return countries

def getCountryArray(date):
    countries = getCountryDict(date)
    country_list = [country for country in countries.keys()]
    confirmed_list = [int(countries[country]['confirmed']) for country in countries.keys()]
    death_list = [int(countries[country]['deaths']) for country in countries.keys()]
    lethality_list = [round(float(death/confirmed*100), 4) for confirmed, death in zip(confirmed_list, death_list)]
    master = [[country, confirmed, deaths, lethality] for country, confirmed, deaths, lethality in zip (country_list, confirmed_list, death_list, lethality_list)]
    return master

master = getCountryArray(apr8)
countries = getCountryDict(apr8)
with open("countries.json", 'w') as f:
    json.dump(countries, f)

with open("country_data.csv", 'w') as fout:
    writer = csv.writer(fout)
    writer.writerows(master)

#don't use createMassiveData() because utilizing time_series data is better
daily_report_files = os.listdir('./csse_covid_19_data/csse_covid_19_daily_reports')
def createMassiveData():
    for i in range(0, len(daily_report_files)):
        date_file = daily_report_files[i]
        print(date_file)
        #removing old months with different data (up to 3-21)
        if date_file[0] != '0' or date_file[1] == '1' or date_file[1] == '2':
            continue
        if date_file[1] == '3':
            if date_file[3] == '1' or date_file[3] == '0':
                continue
            elif date_file[3] == '2' and (date_file[4] == '0' or date_file[4] == '1'):
                continue
        afile = load_file(f"./csse_covid_19_data/csse_covid_19_daily_reports/{date_file}")
        stats = getCountryArray(afile)
        with open(f"./cleaned_data/daily/{date_file}", 'w') as f:
            writer = csv.writer(f)
            writer.writerows(stats)
            print('added 1 file')

createMassiveData()




#notes
#tableau time series data
#sql integration of csv files to make joins easier
#R analysis/regression + python plotting tools