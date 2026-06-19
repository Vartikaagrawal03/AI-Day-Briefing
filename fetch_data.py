import base64
import json
from datetime import datetime, timedelta, timezone
from auth import get_google_services

def fetch_emails(gmail_service, max_results=20):
    print("📧 Fetching emails...")
    
    emails = []
    
    # Get emails from last 24 hours
    results = gmail_service.users().messages().list(
        userId='me',
        maxResults=max_results,
        q='newer_than:1d'  # only last 24 hours
    ).execute()

    messages = results.get('messages', [])

    for msg in messages:
        # Get full message details
        message = gmail_service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='full'
        ).execute()

        headers = message['payload']['headers']

        # Extract subject, sender, date
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')
        snippet = message.get('snippet', '')

        emails.append({
            'id': msg['id'],
            'subject': subject,
            'sender': sender,
            'date': date,
            'snippet': snippet
        })

    print(f"✅ Fetched {len(emails)} emails")
    return emails


def fetch_calendar_events(calendar_service):
    print("📅 Fetching calendar events...")

    # Get events from today to next 2 days
    now = datetime.now(timezone.utc)
    time_min = now.isoformat()
    time_max = (now + timedelta(days=2)).isoformat()

    events_result = calendar_service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    calendar_events = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        
        calendar_events.append({
            'title': event.get('summary', 'No Title'),
            'start': start,
            'end': end,
            'description': event.get('description', ''),
            'attendees': [a['email'] for a in event.get('attendees', [])]
        })

    print(f"✅ Fetched {len(calendar_events)} calendar events")
    return calendar_events


if __name__ == "__main__":
    gmail, calendar = get_google_services()
    
    emails = fetch_emails(gmail)
    events = fetch_calendar_events(calendar)

    print("\n--- EMAILS ---")
    for e in emails[:3]:  # show first 3
        print(f"From: {e['sender']}")
        print(f"Subject: {e['subject']}")
        print(f"Preview: {e['snippet'][:100]}")
        print("---")

    print("\n--- CALENDAR EVENTS ---")
    for e in events:
        print(f"Event: {e['title']}")
        print(f"Start: {e['start']}")
        print(f"Attendees: {e['attendees']}")
        print("---")