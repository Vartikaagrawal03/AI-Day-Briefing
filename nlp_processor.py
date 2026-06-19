import re
import spacy

# Load spaCy English model once
nlp = spacy.load("en_core_web_sm")

# Keywords that signal urgency — this is our simple rule-based classifier
URGENT_KEYWORDS = [
    'urgent', 'asap', 'deadline', 'important', 'action required',
    'reminder', 'today', 'tomorrow', 'meeting', 'interview',
    'last chance', 'expires', 'final notice', 'immediately'
]

PROMOTIONAL_KEYWORDS = [
    'sale', 'discount', 'offer', 'unsubscribe', 'newsletter',
    'webinar', 'free trial', 'limited time', 'save up to', 'last chance'
]


def clean_text(text):
    """Remove zero-width characters, extra whitespace, weird encoding artifacts"""
    text = re.sub(r'[\u200b\u200c\u200d\ufeff]', '', text)  # zero-width chars
    text = re.sub(r'\s+', ' ', text)  # collapse multiple spaces
    return text.strip()


def extract_entities(text):
    """Run NER on email text to extract people, dates, orgs"""
    doc = nlp(text)

    entities = {
        'people': [],
        'dates': [],
        'orgs': []
    }

    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            entities['people'].append(ent.text)
        elif ent.label_ == 'DATE':
            entities['dates'].append(ent.text)
        elif ent.label_ == 'ORG':
            entities['orgs'].append(ent.text)

    # Remove duplicates and empty strings
    entities['people'] = list(set(p for p in entities['people'] if p.strip()))
    entities['dates'] = list(set(d for d in entities['dates'] if d.strip()))
    entities['orgs'] = list(set(o for o in entities['orgs'] if o.strip()))

    return entities


def calculate_urgency_score(subject, snippet):
    """Simple rule-based urgency scoring from 0-10"""
    text = (subject + " " + snippet).lower()

    score = 0
    matched_keywords = []

    for keyword in URGENT_KEYWORDS:
        if keyword in text:
            score += 2
            matched_keywords.append(keyword)

    for keyword in PROMOTIONAL_KEYWORDS:
        if keyword in text:
            score -= 2  # promotional emails are less urgent

    score = max(0, min(10, score))
    return score, matched_keywords


def classify_email_type(subject, snippet, sender):
    """Classify email into categories"""
    text = (subject + " " + snippet).lower()
    sender_lower = sender.lower()

    if any(kw in text for kw in PROMOTIONAL_KEYWORDS):
        return 'promotional'
    elif any(kw in text for kw in ['meeting', 'interview', 'call', 'schedule']):
        return 'meeting-related'
    elif any(kw in text for kw in ['deadline', 'submit', 'action required', 'urgent']):
        return 'action-needed'
    elif 'no-reply' in sender_lower or 'noreply' in sender_lower:
        return 'automated'
    else:
        return 'informational'


def process_email(email):
    """Main function - takes raw email, returns enriched email with NLP data"""
    full_text = clean_text(email['subject'] + " " + email['snippet'])

    entities = extract_entities(full_text)
    urgency_score, matched_keywords = calculate_urgency_score(email['subject'], email['snippet'])
    email_type = classify_email_type(email['subject'], email['snippet'], email['sender'])

    enriched_email = {
        **email,
        'entities': entities,
        'urgency_score': urgency_score,
        'matched_keywords': matched_keywords,
        'category': email_type
    }

    return enriched_email


def process_all_emails(emails):
    """Process a list of emails and sort by urgency"""
    print("🧠 Running NLP analysis on emails...")

    processed = [process_email(email) for email in emails]
    processed.sort(key=lambda x: x['urgency_score'], reverse=True)

    print(f"✅ Processed {len(processed)} emails")
    return processed


if __name__ == "__main__":
    from auth import get_google_services
    from fetch_data import fetch_emails

    gmail, calendar = get_google_services()
    emails = fetch_emails(gmail)

    processed_emails = process_all_emails(emails)

    print("\n--- TOP PRIORITY EMAILS ---")
    for e in processed_emails[:5]:
        print(f"\nSubject: {e['subject']}")
        print(f"From: {e['sender']}")
        print(f"Category: {e['category']}")
        print(f"Urgency Score: {e['urgency_score']}/10")
        print(f"Matched Keywords: {e['matched_keywords']}")
        print(f"People mentioned: {e['entities']['people']}")
        print(f"Dates mentioned: {e['entities']['dates']}")
        print("-" * 50)