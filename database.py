import sqlite3
from datetime import datetime

DB_NAME = "briefing_data.db"


def init_db():
    """Create tables if they don't exist"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id TEXT PRIMARY KEY,
            subject TEXT,
            sender TEXT,
            date TEXT,
            snippet TEXT,
            category TEXT,
            urgency_score INTEGER,
            people TEXT,
            dates TEXT,
            orgs TEXT,
            fetched_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calendar_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            start_time TEXT,
            end_time TEXT,
            attendees TEXT,
            fetched_at TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized")


def save_emails(processed_emails):
    """Save processed emails to database, skip duplicates"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    fetched_at = datetime.now().isoformat()
    saved_count = 0

    for email in processed_emails:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO emails 
                (id, subject, sender, date, snippet, category, urgency_score, people, dates, orgs, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                email['id'],
                email['subject'],
                email['sender'],
                email['date'],
                email['snippet'],
                email['category'],
                email['urgency_score'],
                ', '.join(email['entities']['people']),
                ', '.join(email['entities']['dates']),
                ', '.join(email['entities']['orgs']),
                fetched_at
            ))
            if cursor.rowcount > 0:
                saved_count += 1
        except Exception as e:
            print(f"Error saving email: {e}")

    conn.commit()
    conn.close()
    print(f"✅ Saved {saved_count} new emails to database")


def save_calendar_events(events):
    """Save calendar events to database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    fetched_at = datetime.now().isoformat()

    for event in events:
        cursor.execute("""
            INSERT INTO calendar_events (title, start_time, end_time, attendees, fetched_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            event['title'],
            event['start'],
            event['end'],
            ', '.join(event['attendees']),
            fetched_at
        ))

    conn.commit()
    conn.close()
    print(f"✅ Saved {len(events)} calendar events to database")


def get_all_emails():
    """Fetch all stored emails as list of dicts"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emails ORDER BY urgency_score DESC")
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]


if __name__ == "__main__":
    init_db()