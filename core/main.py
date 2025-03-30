from utilities import web_scrape
from utilities import db_store
from utilities import generate_response
from langchain_chroma import Chroma
from dotenv import load_dotenv


__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import sqlite3


load_dotenv()


def get_response(user_query):
    response = db_store.query_db(user_query)

    response = generate_response.get_response(response, user_query)

    # print("\n\nResponse : ",response)

    return response
