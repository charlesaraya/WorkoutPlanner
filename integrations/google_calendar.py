import os
from dotenv import load_dotenv
import pickle
from datetime import datetime, timedelta

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from tzlocal import get_localzone

# Scope for read/write access to Calendar events
load_dotenv()  # Load environment variables
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
CREDENTIALS_FILE = os.getenv("CREDENTIALS_FILE")
TOKEN_FILE = os.getenv("TOKEN_FILE")
PORT = int(os.getenv("PORT"))

def get_calendar_service():
    """Authenticate and return a Google Calendar API service object."""
    creds = None
    # Load existing token if it exists
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    # If no valid credentials, prompt user to authenticate
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=8080)
        # Save the credentials for next run
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    return build("calendar", "v3", credentials=creds)

def save_plan_to_calendar(task: str, final_plan: str, total_time: int, start_time: str):
    """Save a workout plan as a Google Calendar event."""
    service = get_calendar_service()

    # Get local time zone
    local_tz = get_localzone()

    start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
    end_time = (start_time + timedelta(minutes=total_time))

    event = {
        "summary": f"Workout Plan: {task}",
        "description": final_plan,
        "start": {"dateTime": start_time.isoformat(), "timeZone": str(local_tz)},
        "end": {"dateTime": end_time.isoformat(), "timeZone": str(local_tz)},
    }

    event = service.events().insert(calendarId="primary", body=event).execute()
    return event.get("htmlLink")