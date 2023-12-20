import subprocess
import os
import json
from datetime import datetime
import pandas as pd
import sys
import time


import os
download_directory = f"{os.path.dirname(os.path.abspath(__file__))}/pvc_download"

def collect_data():
    #Shell command to get data.
    process = subprocess.Popen(
        f"wget -O- -P {download_directory} https://web.peacefulvanilla.club/maps/tiles/players.json",
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )

    data = json.loads(process.stdout.read())

    # Map dimensions to letters
    dimension_map = {
        "minecraft_the_nether": "n",
        "minecraft_overworld": "o"
    }

    # Removing UUIDs and shortening keys
    simplified_data = [
        {'Time':datetime.now(),'Name': player['name'], 'World': dimension_map[player['world']] if player['world'] in dimension_map else player['world'], 'Armor': player['armor'], 'Health': player['health'], 'Yaw': player['yaw'], 'X': player['x'], 'Z': player['z']}
        for player in data['players']
    ]

    # Convert data to a pandas DataFrame and save
    df = pd.DataFrame(simplified_data)

    file_name = f"{download_directory}/pvc_log.csv"
    file_exists = os.path.isfile(file_name)

    df.to_csv(file_name, mode='a', index=False, header=not file_exists)

def collect_data_continuously(delay = 60):
    pid = os.getpid()
    pid_file = open(f"{download_directory}/pid","w")
    pid_file.write(str(pid))
    pid_file.close()

    while True:
        try:
            collect_data()
            time.sleep(delay)
        except Exception as e:
            print(e)

collect_data_continuously()

