import json
import pygsheets
import pandas as pd
from flask import Flask, render_template
from flask_sockets import Sockets


app = Flask(__name__)
sockets = Sockets(app)

@sockets.route("/chat")
def chat_socket(ws):
    gc = pygsheets.authorize(service_file = "./creds.json")
    while not ws.closed:
        message = ws.receive()
        if message is None:  # message is "None" if the client has closed.
            continue
        d = dict(json.loads(message))
        print(d)
        # Extract the availability dictionary
        availability_dict = d["availability"]
        subteams = d["subteams"]
        print(subteams)
        # Create lists to store data for each column
        names = [d["name"]] * len(availability_dict)  # Repeat name for each availability entry
        times = list(availability_dict.keys())
        available = list(availability_dict.values())

        # Create a DataFrame
        df = pd.DataFrame({
            "name": names,
            "time": times,
            "available": available
        })
        available.insert(0,names[0])
        print(df)
        sh = gc.open('motomeet')
        subteams.append("Teamwide")
        for subteam in subteams:
            teamSheet = sh.worksheet_by_title(subteam)
            teamSheet.append_table(values = available)

# [END gae_flex_websockets_app]
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    print("oops")