import subprocess
import os
import json
from datetime import datetime
import pandas as pd
import sys
import time
import sqlite3 as sql

import os
download_directory = f"{os.path.dirname(os.path.abspath(__file__))}/pvc_download"

def collect_data(conn):
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

    curr_time = datetime.now()

    # Removing UUIDs and shortening keys
    simplified_data = [
            (curr_time,
            player['name'],
            dimension_map[player['world']] if player['world'] in dimension_map else player['world'],
            player['armor'],
            player['health'],
            player['yaw'],
            player['x'],
            player['z'])
        for player in data['players']
    ]

    #Load db
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS player_locations(time, name, world, armor, health, yaw, x, z)")
    conn.commit() 

    cur.executemany("INSERT INTO player_locations VALUES(?, ?, ?, ?, ?, ?, ?, ?)", simplified_data)
    conn.commit()

def collect_data_continuously(delay = 30):
    pid = os.getpid()
    pid_file = open(f"{download_directory}/pid","w")
    pid_file.write(str(pid))
    pid_file.close()

    conn = sql.connect(download_directory+"/pvc_log.db")
    while True:
        try:
            collect_data(conn)
            time.sleep(delay)
        except Exception as e:
            print(e)

collect_data_continuously()

