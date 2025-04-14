from sqlalchemy import create_engine
from urllib import request
import pandas as pd
import json


def download_data() -> json:
    db_url