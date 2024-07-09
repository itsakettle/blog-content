from fastapi import FastAPI, Depends, Header, HTTPException
import pymysql

app = FastAPI()
connection_parameters = \
    {
    'host': 'localhost',
    'user': 'user',
    'password': 'passwd',
    'database': 'db',
    'cursorclass': pymysql.cursors.DictCursor
    }

insecure_sql = "SELECT location from locations where feather_code = '{feather_code}'"

def get_locations_from_db(feather_code: str):
    
    with pymysql.connect(**connection_parameters) as connection:
        with connection.cursor() as cursor:
            sql = insecure_sql.format_map({'feather_code': feather_code})
            locations_list_of_dict = cursor.execute(sql).fetch_all()
            return [location_dict['location'] for location_dict in locations_list_of_dict]
    

@app.get("/my-treasure-locations")
async def locations(x_feather_code: Header(...)):
    locations = get_locations_from_db(x_feather_code)
    return {"treasure_locations": locations}
