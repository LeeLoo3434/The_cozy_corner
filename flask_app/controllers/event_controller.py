from pprint import pprint
from flask_app import app, render_template, redirect, request, session
from flask_app.models.user_model import User
# from flask_app.models.event_model import Event
import requests
# print(response.json())


@app.get('/')
def redirect_user():
    return render_template('dashboard.html')


@app.post("/search")
def searchApi():
    print(request.form)
    response = requests.get(
        url="https://api.predicthq.com/v1/events?q=queer/",
        headers={
            "Authorization": "Bearer UXML4-8IbsvSvTWOgX5xyQr74kNrrVfYQWixd63V",
            "Accept": "application/json"
        }
    )
    pprint(response.json())
    return render_template("nologin_events.html", response=response.json())
