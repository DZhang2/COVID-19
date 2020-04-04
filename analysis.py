import numpy as np
import pandas as pd
import csv
import time
import matplotlib.pyplot as plt
import json

def load_file(path):
    file = pd.read_csv(path)
    return file

confirmed_US = load_file("./csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")
apr2 = load_file("./csse_covid_19_data/csse_covid_19_daily_reports/04-02-2020.csv")

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

def getCountryStats(date):
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

countries = getCountryStats(apr2)
country_list = [country for country in countries.keys()]
confirmed_list = [int(countries[country]['confirmed']) for country in countries.keys()]
death_list = [int(countries[country]['deaths']) for country in countries.keys()]
lethality_list = [round(float(death/confirmed*100), 4) for confirmed, death in zip(confirmed_list, death_list)]
master = [[country, confirmed, deaths, lethality] for country, confirmed, deaths, lethality in zip (country_list, confirmed_list, death_list, lethality_list)]

with open("countries.json", 'w') as f:
    json.dump(countries, f)

with open("country_data.csv", 'w') as fout:
    writer = csv.writer(fout)
    writer.writerows(master)