from __future__ import print_function
import datetime
import calendar
import os
import json

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Define the scope for accessing Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_credentials():
    """
    Retrieves user credentials for Google Calendar API access.
    If valid credentials are not available, the user is prompted to log in.
    """
    creds = None
    token_path = 'planner-interface/credentials/token.json'
    credentials_path = 'planner-interface/credentials/credentials.json'

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds


def gather_calendar_events(start_time, end_time, filter_date=None):
    """
    Fetches calendar events from the user's Google Calendar within a specified time range.
    
    :param start_time: ISO formatted start time (e.g., '2022-01-01T00:00:00Z').
    :param end_time: ISO formatted end time (e.g., '2022-01-01T23:59:59Z').
    :param filter_date: Optional date string ('YYYY-MM-DD') to filter events for a specific day.
    :return: A dictionary containing 'all-day events' and 'timed events'.
    """
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    events_result = service.events().list(
        calendarId='primary', 
        timeMin=start_time,
        timeMax=end_time, 
        singleEvents=True, 
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])

    all_day_events = []
    timed_events = []

    for event in events:
        start_date = event['start'].get('date') 
        start_time = event['start'].get('dateTime') 

        if filter_date:
            if start_date and start_date != filter_date:
                continue
            if start_time and start_time[:10] != filter_date:
                continue

        if start_date:
            all_day_events.append({
                "date": start_date,
                "event": event.get('summary', 'No Title')
            })
        elif start_time:
            timed_events.append({
                "date": start_time[:10],
                "start-time": start_time[11:16],
                "end-time": event['end']['dateTime'][11:16],
                "event": event.get('summary', 'No Title')
            })

    return {"all-day events": all_day_events, "timed events": timed_events}


def save_to_json(data, filename):
    """
    Saves the given data into a JSON file at the specified filename path.
    
    :param data: The data to be written into the JSON file.
    :param filename: The path where the JSON file should be saved.
    """
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)


def get_current_day_events():
    """
    Gathers today's calendar events and saves them to a JSON file.
    """
    today = datetime.datetime.now().date()
    today_str = today.isoformat()

    start_of_day = datetime.datetime.combine(today, datetime.time.min).isoformat() + 'Z'
    end_of_day = datetime.datetime.combine(today, datetime.time.max).isoformat() + 'Z'

    calendar_events = gather_calendar_events(start_of_day, end_of_day, filter_date=today_str)
    json_filename = 'planner-interface/data/day-data.json'
    save_to_json(calendar_events, json_filename)
    print(f"Today's events successfully saved to {json_filename}")


def get_current_week_events():
    """
    Gathers this week's calendar events and saves them to a JSON file.
    """
    now = datetime.datetime.utcnow()
    start_of_week = now.isoformat() + 'Z'
    end_of_week = (now + datetime.timedelta(days=7)).isoformat() + 'Z'

    calendar_events = gather_calendar_events(start_of_week, end_of_week)
    json_filename = 'planner-interface/data/week-data.json'
    save_to_json(calendar_events, json_filename)
    print(f"This week's events successfully saved to {json_filename}")


def get_current_month_events():
    """
    Gathers this month's calendar events and saves them to a JSON file.
    """
    today = datetime.datetime.now().date()

    # Get the first day of the current month
    start_of_month = today.replace(day=1)
    
    # Get the last day of the current month
    _, last_day = calendar.monthrange(today.year, today.month)
    end_of_month = today.replace(day=last_day)
    
    # Create ISO format start and end times for the month
    start_of_month_datetime = datetime.datetime.combine(start_of_month, datetime.time.min).isoformat() + 'Z'
    end_of_month_datetime = datetime.datetime.combine(end_of_month, datetime.time.max).isoformat() + 'Z'
    
    # Fetch calendar events for the entire month
    calendar_events = gather_calendar_events(start_of_month_datetime, end_of_month_datetime)
    
    # Save the fetched events to a JSON file
    json_filename = 'planner-interface/data/month-data.json'
    save_to_json(calendar_events, json_filename)
    print(f"Current month's events successfully saved to {json_filename}")


if __name__ == '__main__':
    get_current_day_events()
    get_current_week_events()
    get_current_month_events()