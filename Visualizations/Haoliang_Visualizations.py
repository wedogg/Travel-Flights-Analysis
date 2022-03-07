import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import LineString
import seaborn as sns
import plotly.graph_objects as go

import os

airports = pd.read_csv('airports.csv')
flights = pd.read_csv('flights.csv')
columns_to_drop = ['CANCELLATION_REASON', 'AIR_SYSTEM_DELAY', 'SECURITY_DELAY',
                  "AIRLINE_DELAY", "LATE_AIRCRAFT_DELAY", "WEATHER_DELAY"]
flights = flights.drop(columns_to_drop, axis=1, errors='ignore')
flights = flights[flights['CANCELLED'] == 0]
flights = flights[flights['DIVERTED'] == 0]
corr_matrix = flights.corr()
corr_matrix['ARRIVAL_DELAY'].sort_values(ascending=False)
flights.isnull().sum()

def delay_by_attribute(attribute, df=flights, figsize=(10, 7)):
    # Delay with less than 10 min are mapped to 0 otherwise they are mapped to 1
    delay_type = lambda x: 0 if x < 10 else 1
    flights['DELAY_TYPE'] = flights['DEPARTURE_DELAY'].apply(delay_type)


    plt.figure(1, figsize=figsize)
    ax = sns.countplot(y=attribute, hue='DELAY_TYPE', data=df, palette="Set2")

    plt.xlabel('Flight count', fontsize=16, weight='bold')
    plt.ylabel(attribute, fontsize=16, weight='bold')
    plt.title(f'Delay by {attribute}', weight='bold')
    L = plt.legend()
    L.get_texts()[0].set_text('small delay (t < 10 min)')
    L.get_texts()[1].set_text('large delay (t > 10 min)')
    plt.grid(True)
    plt.show()
delay_by_attribute('AIRLINE')
result = pd.merge(flights[['ORIGIN_AIRPORT', 'DELAY_TYPE']], airports[['IATA_CODE', 'STATE']], left_on='ORIGIN_AIRPORT', right_on='IATA_CODE')

delay_by_attribute('STATE', df=result, figsize=(10, 15))
