# author pretty_printed:
# Chanel: https://www.youtube.com/channel/UC-QDfvrRIDB6F0bIO4I4HkQ
# Video link: https://www.youtube.com/watch?v=kCggyi_7pHg

import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

db = []


class City(BaseModel):
    """you can keep "timezone" data type as datetime, list, dictionary..
    pydantic will do the job to interpret the data in sent request and map it accordingly"""
    name: str
    timezone: str


@app.get('/')
def index():
    return {'key': 'value'}


@app.get('/cities')
def get_all_cities():
    return db


@app.get('/cities_with_time_zone')
def get_all_cities_with_tz():
    response = []
    for city in db:
        r = requests.get(url=f'http://worldtimeapi.org/api/timezone/{city.timezone}')
        current_time = r.json()['datetime']
        response.append({'name': city.name,
                         'timezone': city.timezone,
                         'current_time': current_time})
    return response


@app.post('/cities')
def create_city(city: City):
    db.append(city)
    return city


@app.get('/cities/{city_id}')
def get_one_city(city_id: int):
    return db[city_id - 1]


@app.delete('/cities')
def index(city_id: int):
    db.pop(city_id - 1)
    return {}

# example JSONs
# {
#   "name": "Las Vegas",
#   "timezone": "America/Los_Angeles"
# },
# {
#   "name": "Miami",
#   "timezone": "America/New_York"
# }

# uvicorn fastapi_b_yt:app --reload
