# Imports
import pandas as pd
import numpy as np
import geopandas as gpd
from folium import *
import matplotlib.pyplot as plt

from bs4 import BeautifulSoup as Soup
import requests

print('- imports complete -')

# Data Imports

def get_football_stadium_data():
    '''
    This will find geography location for each football stadium 
    in the top 5 English leagues, top 4 Scottish leagues and the 
    top 2 Northern Irish leagues.

    Input:
        None

    Output:
        df - Dataframe of the stadium data
    '''

    print('- finding football stadium data -')
    
    url = 'https://www.doogal.co.uk/FootballStadiums.php'
    response = requests.get(url)
    page_soup = Soup(response.text, features='lxml')

    # print(page_soup)

    table = page_soup.find_all(
        'table',
        {'class':'sortable stadiumsTable table table-striped table-hover'}
    )

    stad_name, team, capacity, lat, long = [],[],[],[],[]

    for r in table[0].find_all('tr')[1:]:
        col = r.find_all('td')
        stad_name.append(col[0].get_text())
        team.append(col[1].get_text())
        capacity.append(col[2].get_text())
        lat.append(col[3].get_text())
        long.append(col[4].get_text())

    df = pd.DataFrame(
        data = {
            'stad_name':stad_name,
            'team':team,
            'capacity':capacity,
            'lat':lat,
            'long':long,
        }
    )

    print('- football stadium data generated from doogal.co.uk -')
    return df

def get_pub_data():
    '''
    This will find geography location for each pub in the UK

    Input:
        None

    Output:
        df - Dataframe of the pub data
    '''

    print('- finding pub location data -')
    
    df = pd.read_csv('http://www.math.uwaterloo.ca/tsp/pubs/files/uk24727_latlong.txt', sep=' ', header=None)
    df.columns = ['lat', 'long']

    print('- pub data generated from math.uwaterloo.ca -')
    return df

stadiums = get_football_stadium_data()
pubs = get_pub_data()

def convert_to_gdf(df, lat_col = 'lat', long_col = 'long'):
    '''
    This fn converts a pandas data frame to a geo data frame
    to enable plotting

    Inputs: 
        - df - Pandas DataFrame
        - long_col - Column with longitude data
        - lat_col - Column with latitude data

    Outputs:
        - gdf - GeoPandas GeoDataFrame
    '''

    gdf = gpd.GeoDataFrame(
        df, 
        geometry = gpd.points_from_xy(df[long_col], df[lat_col])
    )
    return gdf

stadiums_gdf = convert_to_gdf(stadiums)
pubs_gdf = convert_to_gdf(pubs)

def inititalise_map():

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    uk_map = world[world.name=='United Kingdom']

    ax = uk_map.plot(color='white',edgecolor='grey')

    pubs_gdf.plot(ax=ax, color='red', markersize=0.2)
    stadiums_gdf.plot(ax=ax, color='blue', markersize=0.8)

    plt.show()


inititalise_map()