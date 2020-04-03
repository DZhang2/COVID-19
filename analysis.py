import pandas as pd
import numpy as np

def load_file(path):
    file = pd.read_csv(path)
    return file

confirmed_US = load_file("./csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")
april1 = load_file("./csse_covid_19_data/csse_covid_19_daily_reports/04-01-2020.csv")
print(confirmed_US.head())
print(april1.head())
