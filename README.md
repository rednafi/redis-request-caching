<div align="center">

# Redis || Request || Caching

🐍 Simple Python App to Demonstrate API Request Caching with Redis

</div>

<div align="center">

[**|| Blog ||**](https://rednafi.github.io/digressions/python/database/2020/05/25/python-redis-cache.html)

</div>

## Description

This app sends request to [Mapbox](https://www.mapbox.com/)'s [route optimization API](https://docs.mapbox.com/api/navigation/#optimization) and caches the return value in a Redis database for 1 hours. Meanwhile, if new a new request arrives, the app first checks if the return value exists in the Redis cache. If the value exists, it shows the cached value, otherwise, it sends a new request to the Mapbox API, cache that value and then shows the result.

The app uses the following stack:

* [Httpx](https://github.com/encode/httpx/) for sending the requests
* [Redis](https://redis.io/) for caching
* [RedisInsight](https://redislabs.com/redisinsight/) for monitoring the caches
* [FastAPI](https://github.com/tiangolo/fastapi) for wrapping the original API and exposing a new one
* [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/) for deployment

## Requirements

* [Docker](https://www.docker.com/)
* [Docker-compose](https://docs.docker.com/compose/)

## Run the App

* Clone the repository.

    ```
    git clone git@github.com:rednafi/redis-request-caching.git
    ```

* Go to `.env` file and provide your `MAPBOX_ACCESS_TOKEN`. You can get it from [here.](https://docs.mapbox.com/help/how-mapbox-works/access-tokens/)

    ```
    MAPBOX_ACCESS_TOKEN="Your-Mapbox-API-token"
    ```

* In the `.env` file, replace the host ip with your own local ip

* Go to the root directory and run:

    ```bash
    docker-compose up -d
    ```

* Go to your browser and hit the following url:

    ```
    http://localhost:5000/route-optima/90.3866,23.7182;90.3742,23.7461
    ```

* This should return a response like the following:

    ```json
    {
    "code":"Ok",
    "waypoints":[
        {
            "distance":26.041809241776583,
            "name":"",
            "location":[
                90.386855,
                23.718213
            ],
            "waypoint_index":0,
            "trips_index":0
        },
        {
            "distance":6.286653078791968,
            "name":"",
            "location":[
                90.374253,
                23.746129
            ],
            "waypoint_index":1,
            "trips_index":0
        }
    ],
    "trips":[
        {
            "geometry":{
                "coordinates":[
                [
                    90.386855,
                    23.718213
                ],
                "...


    ..."
                ],
                "type":"LineString"
            },
            "legs":[
                {
                "summary":"",
                "weight":3303.1,
                "duration":2842.8,
                "steps":[

                ],
                "distance":5250.2
                },
                {
                "summary":"",
                "weight":2536.5,
                "duration":2297,
                "steps":[

                ],
                "distance":4554.8
                }
            ],
            "weight_name":"routability",
            "weight":5839.6,
            "duration":5139.8,
            "distance":9805
        }
    ],
    "cache":false
    }
    ```

* If you've hit the above url for the first time, the `cache` attribute of the json response should show `false`. This means that the response is being served from the original MapBox API. However, hitting the same url with the same coordinates again will show the cached response and this time the `cache` attribute should show `true`.

* You can also go to `localhost:5000/docs` and play around with the swagger UI.

    ![alt](./ext/swagger.png)


* The cached data can be monitored using redisinsight. Go to `localhost:8000`.

    ![alt](./ext/redisinsight.png)

## Remarks

All the pieces of codes in the blog were written and tested with python 3.8 on a machine running Ubuntu 18.04.

## Disclaimer

This app has been made for demonstration purpose only. So it might not reflect the best practices of production ready applications. Using APIs without authentication like this is not recommended.
