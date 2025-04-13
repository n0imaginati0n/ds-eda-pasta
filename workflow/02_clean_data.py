

import pandas as pd
import numpy as np

def load_raw_data(name):
    return pd.read_csv(name, sep=',')

def clean_column_names(df):
    df.drop("Unnamed: 0", axis="columns", inplace=True)
    df.rename(columns={"id": "house_id"}, inplace=True)

def set_column_types(df):
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



def handle_nan_values(df):
    '''
    according to df_sales.isnull().any()
    only columns 'waterfront', 'view', 'sqft_basement' and 'yr_renovated' has NaN values
    '''
    pass

if __name__ == '__main__':
    df_sales = load_raw_data('data/houses_sales.csv')

    clean_column_names(df_sales)
    print(df_sales.yr_renovated.head())
    set_column_types(df_sales)

    print(df_sales.info())

    df_sales.to_pickle('data/houses_sales.pkl')
