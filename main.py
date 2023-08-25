import json
import pygsheets
import pandas as pd
from flask import Flask, render_template
from flask_sockets import Sockets


app = Flask(__name__)
sockets = Sockets(app)

@sockets.route("/foo")
def handler(websocket):
    gc = pygsheets.authorize(service_file = "./creds.json")
    while not websocket.closed:
        message = websocket.receive()
        if message == None:
            continue
        d = dict(json.loads(message))
        print(d)
        # Extract the availability dictionary
        availability_dict = d["availability"]
        subteams = d["subteams"]
        print(subteams)
        # Create lists to store data for each column
        names = [d["name"]] * len(availability_dict)  # Repeat name for each availability entry
        available = list(availability_dict.values())

        available.insert(0,names[0])
        sh = gc.open('motomeet')
        subteams.append("Teamwide")
        for subteam in subteams:
            teamSheet = sh.worksheet_by_title(subteam)
            cur_names = teamSheet.get_col(1)
            dup = False
            for ix, n in enumerate(cur_names):
                if n == names[0]: #duplicate entry found
                    teamSheet.update_row(index = ix+1, values = available)
                    dup = True
                    print("duplicate found!")
            if not dup:
                teamSheet.append_table(values = available)
                print("success added")

@app.route("/")
def index():
    return render_template("index.html")
"""async def main():
    async with websockets.serve(handler, "", 8080):
        await asyncio.Future()  # run forever

"""
if __name__ == "__main__":
    print(
        """
        This can not be run directly because the Flask development server does not
        support web sockets. Instead, use gunicorn:

        gunicorn -b 127.0.0.1:8080 -k flask_sockets.worker main:app

        """
            )