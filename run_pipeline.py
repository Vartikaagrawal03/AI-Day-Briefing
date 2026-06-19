from auth import get_google_services
from fetch_data import fetch_emails, fetch_calendar_events
from nlp_processor import process_all_emails
from database import init_db, save_emails, save_calendar_events, get_all_emails


def run_full_pipeline():
    print("=" * 50)
    print("🚀 STARTING DAILY BRIEFING PIPELINE")
    print("=" * 50)

    # Step 1: Initialize database
    init_db()

    # Step 2: Authenticate
    gmail, calendar = get_google_services()

    # Step 3: Fetch raw data
    raw_emails = fetch_emails(gmail)
    raw_events = fetch_calendar_events(calendar)

    # Step 4: Run NLP processing
    processed_emails = process_all_emails(raw_emails)

    # Step 5: Save everything to database
    save_emails(processed_emails)
    save_calendar_events(raw_events)

    print("\n" + "=" * 50)
    print("✅ PIPELINE COMPLETE")
    print("=" * 50)

    return processed_emails, raw_events


if __name__ == "__main__":
    emails, events = run_full_pipeline()

    print(f"\n📊 Summary: {len(emails)} emails processed, {len(events)} events found")
    
    high_priority = [e for e in emails if e['urgency_score'] >= 4]
    print(f"⚠️  High priority emails: {len(high_priority)}")