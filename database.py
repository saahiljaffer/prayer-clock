#!/usr/bin/python3

import sqlite3
import datetime
import pytz
from datetime import timedelta

conn = sqlite3.connect('prayertimes.db')
print ("Opened database successfully")

prayers = ["imsak", "fajr", "sunrise", "zuhr", "sunset", "maghrib"]

mt = 4
dt = 1

for month in range(4, 13):
    for day in range(1, 32):
        for prayer in prayers:
            command = "SELECT " + prayer + " from times WHERE month = " + str(mt) + " AND day = " + str(dt)
            cursor = conn.execute(command)
            hour = timedelta(hours=+1)
            for row in cursor:
                date_time_obj = datetime.datetime.strptime(row[0], '%I:%M')
                date_time_obj = date_time_obj + hour
                new_time = date_time_obj.strftime('%I:%M')
                updateCommand = "UPDATE times SET " + prayer + " = '" + new_time + "' WHERE month = " + str(mt) + " AND day = " + str(dt)
                print(updateCommand)
                conn.execute(updateCommand)
                conn.commit()
        dt = dt + 1
    dt = 1
    mt = mt + 1        

print ("Operation done successfully")
conn.close()