import os
import requests
import datetime
import json

# Notion API setup
notion_token = os.getenv('NOTION_TOKEN')

# Replace these with your actual database IDs
timed_daily_id = "b22ad5132ba74f6aa62e18c0fb051d1f"
daily_database_id = "0729c0bd7b92484584b3baf4066d3e31"
weekly_database_id = "d948e339bf914f8e8c520e367145b4b7"
monthly_database_id = "57e9f336e39a4e019caa5fbafaa951b8"

NOTION_API_URL_PAGE = "https://api.notion.com/v1/pages"

headers = {
    "Authorization": f"Bearer {notion_token}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Helper functions to handle Notion API tasks
def get_all_tasks(database_id):
    NOTION_API_URL_DATABASE = f"https://api.notion.com/v1/databases/{database_id}/query"
    response = requests.post(NOTION_API_URL_DATABASE, headers=headers)
    if response.status_code == 200:
        tasks = response.json().get('results', [])
        return tasks
    else:
        print(f"Failed to retrieve tasks. Status code: {response.status_code}")
        print(response.text)
        return []

def delete_task(page_id):
    delete_data = {
        "archived": True  # Archive the task (equivalent to deletion)
    }
    response = requests.patch(f"{NOTION_API_URL_PAGE}/{page_id}", headers=headers, data=json.dumps(delete_data))
    if response.status_code == 200:
        print(f"Task '{page_id}' deleted successfully!")
    else:
        print(f"Failed to delete task '{page_id}'. Status code: {response.status_code}")
        print(response.text)

# Function to reset the database (clear tasks)
def reset_database(database_id):
    tasks = get_all_tasks(database_id)
    for task in tasks:
        page_id = task['id']
        delete_task(page_id)

def add_task(task_name, event_date, database_id):
    # Customize the task format for the daily to-do list
    if database_id == daily_database_id:
        new_task_data = {
            "parent": {"database_id": database_id},
            "properties": {
                "Project": {
                    "title": [
                        {
                            "text": {
                                "content": task_name  # Task title
                            }
                        }
                    ]
                }
                # Add any additional daily-specific properties here
            }
        }
    else:
        # Use the existing structure for weekly and monthly databases
        new_task_data = {
            "parent": {"database_id": database_id},
            "properties": {
                "Name": {  # The title of the task
                    "title": [
                        {
                            "text": {
                                "content": task_name
                            }
                        }
                    ]
                },
                "Date": {  # The date of the event
                    "date": {
                        "start": event_date  # The event date (formatted as YYYY-MM-DD)
                    }
                }
            }
        }

    response = requests.post(NOTION_API_URL_PAGE, headers=headers, data=json.dumps(new_task_data))

    if response.status_code == 200:
        print(f"Task '{task_name}' added successfully!")
    else:
        print(f"Failed to add task '{task_name}'. Status code: {response.status_code}")
        print(response.text)



# Function to process all-day events and add them to the correct database
def process_all_day_events(json_file, database_id):
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Get all-day events
    all_day_events = data.get("all-day events", [])

    # Add each event to the respective Notion database
    for event in all_day_events:
        event_date = event["date"]
        task_name = event.get("event")
        if task_name:  # Ensure there's a task name
            print(f"Adding task: {task_name} on date: {event_date} to database {database_id}")
            add_task(task_name, event_date, database_id)

# Specific function to process today's data and update the to-do list
def process_today_data(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Get all-day events
    all_day_events = data.get("all-day events", [])

    # Today's date
    today = datetime.date.today()

    # Add each event happening today to the Notion to-do list (daily)
    for event in all_day_events:
        event_date = event["date"]
        event_date_obj = datetime.datetime.strptime(event_date, "%Y-%m-%d").date()  # Convert string date to date object
        if event_date_obj == today:  # Check if the event is for today
            task_name = event.get("event")
            if task_name:  # Ensure there's a task name
                add_task(task_name, event_date, daily_database_id)  # Pass the event date as well

def add_timed_task(task_name, event_date, start_time, end_time, database_id):
    new_task_data = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {  # The title of the task
                "title": [
                    {
                        "text": {
                            "content": task_name
                        }
                    }
                ]
            },
            "time_begin": {  # The start time of the event
                "rich_text": [
                    {
                        "text": {
                            "content": f"{event_date} {start_time}"  # Combine date and time
                        }
                    }
                ]
            },
            "time_end": {  # The end time of the event
                "rich_text": [
                    {
                        "text": {
                            "content": f"{event_date} {end_time}"  # Combine date and time
                        }
                    }
                ]
            }
        }
    }

    response = requests.post(NOTION_API_URL_PAGE, headers=headers, data=json.dumps(new_task_data))

    if response.status_code == 200:
        print(f"Timed task '{task_name}' added successfully!")
    else:
        print(f"Failed to add timed task '{task_name}'. Status code: {response.status_code}")
        print(response.text)

# Function to process timed events from day-data.json and add them to the timed daily database
def process_timed_events(json_file, database_id):
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Get timed events
    timed_events = data.get("timed events", [])

    # Add each timed event to the respective Notion database
    for event in timed_events:
        event_date = event["date"]
        task_name = event.get("event")
        start_time = event.get("start-time")
        end_time = event.get("end-time")
        if task_name:  # Ensure there's a task name
            print(f"Adding timed task: {task_name} on {event_date} from {start_time} to {end_time}")
            add_timed_task(task_name, event_date, start_time, end_time, database_id)



if __name__ == '__main__':
    # Daily To-Do List: Reset the database and add today's events
    json_file_path = 'planner-interface/data/week-data.json'
    
    # Step 1: Reset the database by deleting all existing tasks for the daily to-do
    reset_database(daily_database_id)
    reset_database(weekly_database_id)
    reset_database(monthly_database_id)
    reset_database(timed_daily_id)

    # Step 2: Add only today's events to the Notion daily to-do list
    process_today_data(json_file_path)

    # Weekly and Monthly: Reset databases and add tasks
    # Process weekly events
    process_all_day_events('planner-interface/data/week-data.json', weekly_database_id)

    # Process monthly events
    process_all_day_events('planner-interface/data/month-data.json', monthly_database_id)

    # Process timed events for the day from 'day-data.json'
    json_file_path = 'planner-interface/data/day-data.json'
    process_timed_events(json_file_path, timed_daily_id)