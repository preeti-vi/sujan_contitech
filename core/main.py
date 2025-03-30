from utilities import generate_response
from dotenv import load_dotenv
from utilities import db_store


load_dotenv()


def get_response(user_query):
    response = db_store.query_db(user_query)

    response = generate_response.get_response(response, user_query)

    # print("\n\nResponse : ",response)

    return response
