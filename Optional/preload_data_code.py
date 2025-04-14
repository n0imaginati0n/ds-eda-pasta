
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
import pandas as pd

def make_connection() -> Engine:
    """ opens a connection to the remote SQL database

    Returns:
        sqlalchemy.Engine: database connection object
    """
    load_dotenv()
    return create_engine(os.getenv('DB_STRING'))

def read_data(connection: Engine, query: str):
    """ read data from remote server according to the specified query

    Args:
        connection (sqlalchemy.Engine): sqlalchemy connection object
        query (string): SQL query string
    """
    return pd.read_sql(
        query,
        con=connection
    )

def preload_data(out_csv_file: str, force: bool = False):
    """ read the data from remote SQL database and save it as csv file.
        a data will be requested and a new file will be create in case of there 
        is no already existent file with this name

    Args:
        out_csv_file (str): output csv file name
        force (bool, optional): force file re-creation. Defaults to False.
    """    

    if force or not os.path.isfile(out_csv_file):
        query = '''
            SELECT hd.*, hs."date" as "sell_date", hs."price"
            FROM eda.king_county_house_details hd
                LEFT JOIN eda.king_county_house_sales hs
            ON
                hd.id = hs.house_id
            ;
        '''
        data = read_data(make_connection(), query)
        data.to_csv(out_csv_file)
