from sqlalchemy import create_engine
from urllib import request
import pandas as pd
import numpy as np
import json
from dotenv import load_dotenv
import os

def download_data(connection_string: str) -> pd.DataFrame:
    """ download EDA data from remote SQL database

    Args:
        connection_string (str): SQLAlchemy string containing 
            login, pass and driver specific syntax

    Returns:
        pd.DataFrame: collected data
    """    
    df = pd.DataFrame()
    engine = create_engine(connection_string)
    query = '''
        SELECT kchs."date" AS sell_date, kchs.price AS price, kchd.*
            FROM eda.king_county_house_sales kchs 
                LEFT JOIN eda.king_county_house_details kchd
                ON kchs.house_id = kchd.id;
    '''
    df = pd.read_sql(query, engine)
    return df

def get_initial_dataset() -> pd.DataFrame:
    """ load initial dfataset from remote server using 
        credentials stored in the .env file

    Returns:
        pd.DataFrame: loaded data frame
    """    
    load_dotenv()
    df = download_data(os.getenv("DB_STRING"))
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """ normalize some columns, their values and their type

    Args:
        df (pd.DataFrame): dataframe object

    Returns:
        pd.DataFrame: processed dataframe
    """    
    df['sell_date'] = pd.to_datetime(df['sell_date'], format="%Y-%m-%d", errors='raise')
    df['yr_built'] = pd.to_datetime(df['yr_built'], format="%Y", errors='raise')
    df['yr_renovated'] = df['yr_renovated'].apply(
        lambda yr: pd.to_datetime(int(yr / 10)) if pd.notnull(yr) and int(yr) != 0 else pd.NaT
    )
    df['price_mln'] = df['price'] / 1e6
    df['price_per_sqft'] = df['price'] / df['sqft_living']
    df['bedrooms'] = df['bedrooms'].astype( np.int16 )

    return df

def get_data_set(pkl_file_name: str, force: bool = False) -> pd.DataFrame:
    """ loads cached dataset, or a new one, if the cached data is not present,
    or 'force' parameter is True

    Args:
        pkl_file_name (str): the file name to keep dataset on disk
        force (bool, optional): force dataset reloading. Defaults to False.

    Returns:
        pd.DataFrame: dataset
    """
    if force or not os.path.isfile(pkl_file_name):
        df = clean_data(get_initial_dataset())
        df.to_pickle(pkl_file_name)
        
    else:
        df = pd.read_pickle(pkl_file_name)
    
    return df

def load_geojson(geojson_filename: str, zipcodes: set = {}, force: bool = False) -> json:
    url = r"https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/refs/heads/master/wa_washington_zip_codes_geo.min.json"

    geojson = {}
    if force or not os.path.isfile(geojson_filename):
        with request.urlopen(url) as response:
            geojson = json.loads(response.read().decode())

        if len(zipcodes):
            areas_before = len(geojson['features'])
            geojson['features'] = [ feat for feat in geojson['features'] if int(feat['properties']['ZCTA5CE10']) in zipcodes ]
            print(f"left {len(geojson['features'])} areas of {areas_before}")

        with open(geojson_filename, "w") as f:
            json.dump(geojson, f)
    else:
        with open(geojson_filename) as f:
            geojson = json.load(f)

    return geojson


if __name__ == '__main__':
    df = get_data_set('data/houses.pkl')
    df.info()

    geo = load_geojson('data/geodata.json', zipcodes={98039, 98040, 98004}, force=True)