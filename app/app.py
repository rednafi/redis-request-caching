import json
from datetime import timedelta
from typing import Any

import aioredis
import httpx
from fastapi import FastAPI
from konfik import Konfik

konfik = Konfik(".env")
config = konfik.config
redis = aioredis.from_url(config.REDIS_DSN, encoding="utf-8", decode_responses=True)


async def get_routes_from_api(coordinates: str) -> dict:
    """Data from mapbox api."""

    async with httpx.AsyncClient() as client:
        base_url = "https://api.mapbox.com/optimized-trips/v1/mapbox/driving"

        geometries = "geojson"
        access_token = config.MAPBOX_ACCESS_TOKEN

        url = f"{base_url}/{coordinates}?geometries={geometries}&access_token={access_token}"

        response = await client.get(url)
        return response.json()


async def get_routes_from_cache(redis: aioredis.client.Redis, key: str) -> str:
    """Data from redis."""

    val = await redis.get(key)
    return val


async def set_routes_to_cache(
    redis: aioredis.client.Redis, key: str, value: str
) -> bool:
    """Data to redis."""

    state = await redis.setex(
        key,
        timedelta(seconds=int(config.CACHE_EXPIRE)),
        value=value,
    )
    return state


async def route_optima(coordinates: str) -> dict:

    # First it looks for the data in redis cache.
    val = await get_routes_from_cache(redis, key=coordinates)

    # If cache is found then serves the data from cache.
    if val is not None:
        data = json.loads(val)
        data["cache"] = True
        return data

    else:
        # If cache is not found then sends request to the MapBox API.
        data = await get_routes_from_api(coordinates)

        # This block sets saves the respose to redis and serves it directly.
        if data.get("code") == "Ok":
            data["cache"] = False
            data = json.dumps(data)
            state = await set_routes_to_cache(redis, key=coordinates, value=data)

            if state is True:
                return data
        return data


app = FastAPI()


@app.get("/route-optima/{coordinates}")
async def view(coordinates: str) -> dict[str, Any]:
    """This will wrap our original route optimization API and
    incorporate Redis Caching. You'll only expose this API to
    the end user."""

    # coordinates = "90.3866,23.7182;90.3742,23.7461"

    return await route_optima(coordinates)
