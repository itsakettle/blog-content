from fastapi import FastAPI, Header
from pydantic import BaseModel
from typing import List
import pymysql

app = FastAPI()


connection_parameters = \
    {
    'host': 'mysql',
    # Just a simple example so using root
    'user': 'root',
    'password': 'NotSensitive',
    'database': 'treasure_api',
    'cursorclass': pymysql.cursors.DictCursor
    }


# No hashing+salting of feather codes because this is a simple sql injection example app.
# We assume Crow has created the database entries somehow as there is no endpoint for this
insecure_sql = "SELECT what3words from treasure_location where feather_code = '{feather_code}'"
parametrized_sql = "SELECT what3words from treasure_location where feather_code = %s"

class Location(BaseModel):
    what3words: str

def query_insecure(cursor, feather_code) -> list:
    very_insecure_sql = insecure_sql.format_map({'feather_code': feather_code})
    cursor.execute(very_insecure_sql)
    return cursor.fetchall()

def query_escaped_param(cursor, feather_code) -> list:
    # Note re doesn't escape ' anymore., so doing it manually
    escaped_feather_code = feather_code.replace("'", "\\'").replace('-', '\\-')
    a_little_more_secure_sql = insecure_sql.format_map({'feather_code': escaped_feather_code})
    cursor.execute(a_little_more_secure_sql)
    return cursor.fetchall()

def query_parametrized(cursor, feather_code) -> list:
    cursor.execute(parametrized_sql, (feather_code))
    return cursor.fetchall()

def get_locations_from_db(feather_code: str) -> List[Location]:
    
    with pymysql.connect(**connection_parameters) as connection:
        with connection.cursor() as cursor:
            #locations_list_of_dict = query_insecure(cursor, feather_code)
            #locations_list_of_dict = query_escaped_param(cursor, feather_code)
            locations_list_of_dict = query_parametrized(cursor, feather_code)
            response = [Location(what3words=location_dict['what3words']) for location_dict in locations_list_of_dict]
            return response

@app.get("/my-treasure-locations/", response_model=List[Location])
async def locations(x_feather_code: str = Header(...)):
    return get_locations_from_db(x_feather_code) 
