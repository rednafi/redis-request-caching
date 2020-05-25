import json
import os
import sys
from datetime import timedelta

import httpx
import redis
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()


def redis_connect() -> redis.client.Redis:
    try:
        client = redis.Redis(
            host=os.environ.get("HOST"),
            port=6379,
            password="ubuntu",
            db=0,
            socket_timeout=5,
        )
        ping = client.ping()
        if ping is True:
            return client
    except redis.AuthenticationError:
        print("AuthenticationError")
        sys.exit(1)


client = redis_connect()


def get_routes_from_api(coordinates: str) -> dict:
    """Data from mapbox api."""

    with httpx.Client() as client:
        base_url = "https://api.mapbox.com/optimized-trips/v1/mapbox/driving"

        geometries = "geojson"
        access_token = os.environ.get("MAPBOX_ACCESS_TOKEN")

        url = f"{base_url}/{coordinates}?geometries={geometries}&access_token={access_token}"

        response = client.get(url)
        return response.json()


def get_routes_from_cache(key: str) -> str:
    """Data from redis."""

    val = client.get(key)
    return val


def set_routes_to_cache(key: str, value: str) -> bool:
    """Data to redis."""

    state = client.setex(key, timedelta(seconds=3600), value=value,)
    return state


def route_optima(coordinates: str) -> dict:

    # First it looks for the data in redis cache
    data = get_routes_from_cache(key=coordinates)

    # If cache is found then serves the data from cache
    if data is not None:
        data = json.loads(data)
        data["cache"] = True
        return data

    else:
        # If cache is not found then sends request to the MapBox API
        data = get_routes_from_api(coordinates)

        # This block sets saves the respose to redis and serves it directly
        if data["code"] == "Ok":
            data["cache"] = False
            data = json.dumps(data)
            state = set_routes_to_cache(key=coordinates, value=data)

            if state is True:
                return json.loads(data)
        return data


app = FastAPI()


@app.get("/route-optima/{coordinates}")
def view(coordinates: str) -> dict:
    """This will wrap our original route optimization API and
    incorporate Redis Caching. You'll only expose this API to
    the end user. """

    # coordinates = "90.3866,23.7182;90.3742,23.7461"

    return route_optima(coordinates)
