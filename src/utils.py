from datetime import datetime, timedelta
import requests
from config.config import DAY


OFFERS_START_DATE = datetime(2024, 3, 4)
OFFERS_END_DATE = datetime(2024, 4, 8)



def get_current_date():
    "Get the actual or artificially set date, time and weekday."
    if DAY:
        now = datetime.strptime(DAY, "%Y-%m-%d")
    else:
        now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    return current_date


def get_week_start_date(date):
    """Given a date, returns the previous Monday's date."""
    date = datetime.strptime(date, "%Y-%m-%d")
    # if date before START_DATE or after END_DATE, throw error:
    if date < OFFERS_START_DATE or date > OFFERS_END_DATE:
        raise ValueError("Date out of range.")
    # To find the last Monday, we subtract the current day's weekday number from the date.
    start_of_week = date - timedelta(days=date.weekday())
    return start_of_week.date()


def is_public_holiday(state: str = "BW"):
    "Returns a dictionary of public holidays in a (German) state."
    url = "https://feiertage-api.de/api/?jahr=2021&nur_land=" + state
    data = requests.get(url).json()
    return data