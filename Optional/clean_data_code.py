
import os.path
import pandas as pd
import numpy as np

def load_raw_data(name: str):
    return pd.read_csv(name, sep=',')

def clean_column_names(df: pd.DataFrame):
    df.drop("Unnamed: 0", axis="columns", inplace=True)
    df.rename(columns={"id": "house_id"}, inplace=True)

def set_column_types(df: pd.DataFrame):
    '''
    'house_id' - id of the house, int64
    'bedrooms' - # of bedrooms, [ 3,  2,  4,  5,  1,  6,  7,  8,  9, 11, 10, 33]
    'bathrooms' - # of bathrooms. contains crazy rational numbers
    'sqft_living' - 
    'sqft_lot'
    'floors' - floors (levels) in house
    'waterfront'
    'view'
    'condition' - How good the condition is ( Overall ). values are: [3, 5, 4, 1, 2]
    'grade' - overall grade given to the housing unit, based on King County grading system. values are: [ 7,  6,  8, 11,  9,  5, 10, 12,  4,  3, 13]
    'sqft_above'
    'sqft_basement'
    'yr_built' - Built Year
    'yr_renovated' - Year when house was renovated
    'zipcode'
    'lat' - Latitude coordinate, float
    'long' - 
    'sqft_living15'
    'sqft_lot15'
    'sell_date' - house was sold
    'price'
    '''
    # as there is anyway has no reason to do arithmetics on those fields
    # and they has a limited set of int values, convert them to category
    df['condition'] = df['condition'].astype("category")
    df['grade'] = df['grade'].astype("category")

    # these columns contain data. no values less than 1900, no NaN
    df['yr_built'] = pd.to_datetime(df.yr_built, format='%Y', errors="raise")
    # renovated contains 17005 times "0." , 3848 times "nan".
    # 21597 - 17005 - 3848 = 744 houses where renovated. 
    # years in format Y0.0
    df['yr_renovated'] = df['yr_renovated'].apply(
        lambda f: pd.NaT if np.isnan(f) or f < 0.1 else pd.to_datetime(int(f/10), format='%Y', errors="raise"))
    # there are no records about renovation before built
    # date of the sell
    df['sell_date'] = pd.to_datetime(df['sell_date'], format='%Y-%m-%d', errors="raise")
    # some numbers are just numbers
    df['bedrooms'] = df['bedrooms'].astype(np.int8, errors="raise")

    df['price'] = df['price'] / 1e6


def clean_data(in_csv_file: str, out_pkl_file: str, force: bool = False):
    """ convert input csv file to a pkl file, fix column types, clean the values.
        nothing will happen, if PKL file with this name already exist

    Args:
        in_csv_file (str): input CSV file
        out_pkl_file (str): output PKL file
        force (bool, optional): overwrite PKL file. Defaults to False.
    """
    if force or not os.path.isfile(out_pkl_file):
        df_sales = load_raw_data(in_csv_file)
        clean_column_names(df_sales)
        set_column_types(df_sales)
        df_sales.to_pickle(out_pkl_file)
