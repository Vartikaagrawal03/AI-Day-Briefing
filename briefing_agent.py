import os
import time
from google import genai
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def format_emails_for_prompt(emails, top_n=5):
    """Convert top priority emails into a clean text block for the prompt"""
    top_emails = emails[:top_n]

    if not top_emails or all(e['urgency_score'] == 0 for e in top_emails):
        return "No high-priority emails today."

    lines = []
    for e in top_emails:
        if e['urgency_score'] > 0:
            lines.append(
                f"- From: {e['sender']} | Subject: {e['subject']} | "
                f"Urgency: {e['urgency_score']}/10 | Category: {e['category']}"
            )

    return "\n".join(lines) if lines else "No high-priority emails today."


def format_events_for_prompt(events):
    """Convert calendar events into a clean text block"""
    if not events:
        return "No meetings scheduled."

    lines = []
    for e in events:
        attendees = ", ".join(e['attendees']) if e['attendees'] else "No attendees listed"
        lines.append(f"- {e['title']} | Start: {e['start']} | Attendees: {attendees}")

    return "\n".join(lines)


def generate_briefing(processed_emails, events):
    """Use Gemini to generate a natural language daily briefing"""

    emails_text = format_emails_for_prompt(processed_emails)
    events_text = format_events_for_prompt(events)

    today = datetime.now().strftime("%A, %B %d, %Y")

    prompt = f"""You are a professional personal assistant. Generate a concise, friendly morning briefing for the user based on the data below.

Today's date: {today}

HIGH PRIORITY EMAILS:
{emails_text}

TODAY/UPCOMING CALENDAR EVENTS:
{events_text}

Instructions:
- Write in a warm, professional tone, like a human assistant
- Keep it under 150 words
- Start with a greeting mentioning the day
- Mention meetings first if any exist, with times
- Then mention urgent emails that need attention
- If nothing urgent, say so positively
- Do NOT use markdown formatting, just plain conversational text
- End with an encouraging note for the day
"""

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"⚠️ Attempt {attempt + 1} failed, retrying in 5 seconds...")
                time.sleep(5)
            else:
                print(f"❌ All retries failed: {e}")
                return "Unable to generate briefing right now due to API issues. Please try again shortly."


if __name__ == "__main__":
    from run_pipeline import run_full_pipeline
    from notifier import send_email_briefing

    emails, events = run_full_pipeline()

    print("\n" + "=" * 50)
    print("📋 YOUR DAILY BRIEFING")
    print("=" * 50)

    briefing = generate_briefing(emails, events)
    print(briefing)

    # Send it to your personal email — replace with your actual email
    send_email_briefing(briefing, "vartikaagrawal0304@gmail.com")