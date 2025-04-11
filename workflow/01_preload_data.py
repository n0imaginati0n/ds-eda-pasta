
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
import pandas as pd

def make_connection():
    load_dotenv()
    return create_engine(os.getenv('DB_STRING'))

def read_data(connection, query):
    return pd.read_sql(
        query,
        con=connection
    )

if __name__ == '__main__':
    query = '''
        SELECT hd.*, hs."date" as "sell_date", hs."price"
        FROM eda.king_county_house_details hd
            LEFT JOIN eda.king_county_house_sales hs
        ON
            hd.id = hs.house_id
        ;
    '''

    data = read_data(make_connection(), query)
    data.to_csv('data/houses_sales.csv')
    



