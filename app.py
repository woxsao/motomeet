import asyncio
import itertools
import json
import websockets
import pygsheets
import pandas as pd
import os
import signal

async def handler(websocket):
    gc = pygsheets.authorize(service_file = "./creds.json")
    async for message in websocket:
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
async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    port = int(os.environ.get("PORT", "8001"))
    async with websockets.serve(handler, "", port):
        await stop


if __name__ == "__main__":
    asyncio.run(main())