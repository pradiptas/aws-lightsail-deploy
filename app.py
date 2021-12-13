from flask import Flask
from datetime import datetime
import requests
import redis
import os
import pytz
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask("app")


def get_new_cases_from_api():
    API_URL = "https://api.covid19tracker.ca/summary"
    resp = requests.request(
        "GET", API_URL
    )
    if resp.status_code == 200:
        try:
            response_json = resp.json()
            change_cases = response_json["data"][0]["change_cases"]
            print("new cases " + str(change_cases))
            return change_cases
        except (KeyError, IndexError) as e:
            print(e)
            return None
    else:
        return None


@app.route("/")
def index():
    return "Welcome! Please hit the `/newcases` API to get the number of new covid cases of the day in Canada."


@app.route("/newcases")
def new_cases_of_the_day():
    # get today's date in string
    date = datetime.now().strftime("%Y-%m-%d")
    new_cases = redis_client.get("date")
    if not new_cases:
        new_cases = get_new_cases_from_api()
    return "Number of New Covid Cases in Canada on " + date + ": " + new_cases


if __name__ == '__main__':
    # Connect to redis client
    redis_host = os.environ.get("REDIS_HOST", "localhost")
    redis_port = os.environ.get("REDIS_PORT", 6379)
    redis_password = os.environ.get("REDIS_PASSWORD", None)
    redis_client = redis.StrictRedis(
        host=redis_host, port=redis_port, password=redis_password)

    # Run the app
    app.run(port=8080, host="0.0.0.0")