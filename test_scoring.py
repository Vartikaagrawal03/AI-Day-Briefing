from nlp_processor import calculate_urgency_score, classify_email_type

subject = "Urgent: Team meeting tomorrow, deadline reminder"
snippet = "Hi, this is urgent. We have an important meeting scheduled for tomorrow. Please complete the action required before the deadline. Reply ASAP."

score, keywords = calculate_urgency_score(subject, snippet)
category = classify_email_type(subject, snippet, "test@test.com")

print(f"Score: {score}")
print(f"Matched keywords: {keywords}")
print(f"Category: {category}")
