import schedule
import time
import datetime
import sqlite3
import pytz
import subprocess

# Constants
DB_FILE = "prayertimes.db"
TIMEZONE = "US/Eastern"
SOUND_FILE = "azan.webm"  # Ensure this is in the correct location
LOG_FILE = "adhan.log"
CHROMECAST_DEVICE = "10.0.0.30"  # Change this to your Chromecast device name


def get_prayer_times():
    """Fetch prayer times from SQLite and adjust for DST"""
    now = datetime.datetime.now()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    query = f"SELECT maghrib FROM times WHERE month = {now.month} AND day = {now.day}"
    result = cursor.execute(query).fetchone()
    conn.close()

    if not result:
        print(f"No prayer times found for {now.month}-{now.day}.")
        return []

    # Convert prayer times to local time with DST adjustment
    local_tz = pytz.timezone(TIMEZONE)
    today_date = datetime.datetime(now.year, now.month, now.day)
    dst_check = local_tz.localize(today_date, is_dst=None).dst() != datetime.timedelta(
        0
    )
    offset = -1 if dst_check else 0

    def adjust_time(prayer_time):
        hour, minute = map(int, prayer_time.split(":"))
        return f"{hour - offset:02d}:{minute:02d}"

    adjusted_times = [adjust_time(time) for time in result]
    print(f"Fetched prayer times: {adjusted_times}")
    return adjusted_times


def play_adhan():
    """Plays the Adhan sound using catt (Chromecast)"""
    try:
        command = ["catt", "-d", CHROMECAST_DEVICE, "cast", SOUND_FILE]
        subprocess.run(command, check=True)
        print(
            f"Played Adhan on {CHROMECAST_DEVICE} at {datetime.datetime.now().strftime('%H:%M:%S')}"
        )
    except subprocess.CalledProcessError as e:
        print(f"Error playing Adhan: {e}")


def reschedule_jobs():
    """Reschedules jobs with updated prayer times"""
    schedule.clear()
    prayer_times = get_prayer_times()

    if not prayer_times:
        return

    # Schedule Adhan at each prayer time
    schedule.every().day.at(prayer_times[0]).do(play_adhan)
    # schedule.every().day.at(prayer_times[1]).do(play_adhan)
    # schedule.every().day.at(prayer_times[2]).do(play_adhan)

    # Schedule re-fetch of times at 2:00 AM
    schedule.every().day.at("02:00").do(reschedule_jobs)

    print(f"Scheduled Adhan at: {prayer_times}")


def main():
    reschedule_jobs()
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
