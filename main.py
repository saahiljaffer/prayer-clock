# // SELECT * from times WHERE month == 3 AND day >= 10 OR month > 3 AND month < 11;

# how to check if dst
# target_date = datetime.datetime.strptime(arg_date, "%Y-%m-%d")
# time_zone = pytz.timezone('US/Eastern')
# dst_date = time_zone.localize(target_date, is_dst=None)
# est_hour = 24
# if bool(dst_date.dst()) is True:
#     est_hour -= 4
# else:
#     est_hour -= 5

# https://github.com/achaudhry/adhan

#!/usr/bin/python3

import datetime
import time
import sys
from os.path import dirname, abspath, join as pathjoin
import argparse
import sqlite3


root_dir = dirname(abspath(__file__))
sys.path.insert(0, pathjoin(root_dir, 'crontab'))

from crontab import CronTab
system_cron = CronTab(user='saahiljaffer')

#HELPER FUNCTIONS
#---------------------------------
#---------------------------------

def addAzaanTime (strPrayerName, strPrayerTime, objCronTab, strCommand):
  job = objCronTab.new(command=strCommand,comment=strPrayerName)  
  timeArr = strPrayerTime.split(':')
  hour = timeArr[0]
  min = timeArr[1]
  job.minute.on(int(min))
  job.hour.on(int(hour))
  job.set_comment(strJobComment)
  print(job)
  return

def addUpdateCronJob (objCronTab, strCommand):
  job = objCronTab.new(command=strCommand)
  job.minute.on(15)
  job.hour.on(3)
  job.set_comment(strJobComment)
  print(job)
  return

def addClearLogsCronJob (objCronTab, strCommand):
  job = objCronTab.new(command=strCommand)
  job.day.on(1)
  job.minute.on(0)
  job.hour.on(0)
  job.set_comment(strJobComment)
  print(job)
  return
#---------------------------------
#---------------------------------
#HELPER FUNCTIONS END

#Set calculation method, utcOffset and dst here
#By default system timezone will be used
#--------------------
isDst = time.localtime().tm_isdst
print(isDst)

now = datetime.datetime.now()
strPlayAzaanMP3Command = 'python {}/play.py >> {}/adhan.log 2>&1'.format(root_dir, root_dir)
strUpdateCommand = 'python {}/main.py >> {}/adhan.log 2>&1'.format(root_dir, root_dir)
strClearLogsCommand = 'truncate -s 0 {}/adhan.log 2>&1'.format(root_dir)
strJobComment = 'rpiAdhanClockJob'

# Remove existing jobs created by this script
system_cron.remove_all(comment=strJobComment)

# Calculate prayer times
conn = sqlite3.connect('prayertimes.db')
print ("Opened database successfully")
prayers = ["fajr", "zuhr", "maghrib"]
command = "SELECT fajr, zuhr, maghrib from times WHERE month = " + str(now.month) + " AND day = " + str(now.day)
todaysTimes = conn.execute(command).fetchone()
# hour = timedelta(hours=+1)
print(todaysTimes)           
conn.close()

# Add times to crontab
addAzaanTime('fajr',todaysTimes[0],system_cron,strPlayAzaanMP3Command)
addAzaanTime('dhuhr',todaysTimes[1],system_cron,strPlayAzaanMP3Command)
addAzaanTime('maghrib',todaysTimes[2],system_cron,strPlayAzaanMP3Command)

# Run this script again overnight
addUpdateCronJob(system_cron, strUpdateCommand)

# Clear the logs every month
addClearLogsCronJob(system_cron,strClearLogsCommand)

system_cron.write_to_user(user='saahiljaffer')
print('Script execution finished at: ' + str(now))