import os
from dotenv import load_dotenv
from pathlib import Path
from groq import Groq
from typing import Literal
from pydantic import BaseModel
import json

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"


def read_email(file_path: Path) -> str:
    with file_path.open("r", encoding="utf-8") as file:
        return file.read()

class Email(BaseModel):
    sender_email: str | None
    subject: str | None
    summary: str | None
    category: Literal[
        "Job",
        "Work",
        "Shopping",
        "Promotion",
        "Spam",
        "Finance",
        "Social",
        "Support",
        "Other",
    ] | None
    priority: Literal[
        "High",
        "Medium",
        "Low",
    ] | None
    action_required: str | None
    deadline: str | None
    sentiment: Literal[
        "Positive",
        "Neutral",
        "Negative",
    ] | None
    
email_schema = Email.model_json_schema()

system_prompt = f"""
You are an email analysis assistant.

Return ONLY a valid JSON object matching the provided schema.
you strictly need to follow the schema of {email_schema}

Rules:
- Do not invent information.
- Use null for missing values.
- Summary must be 2–4 concise sentences and include only information explicitly stated.
- Categories:
  Job, Work, Shopping, Promotion, Spam, Finance, Social, Support, Other.
- Priority must be High, Medium, or Low.
- Sentiment must be Positive, Neutral, or Negative.
- If a priority is not explicitly mentioned:
  - "urgent", "asap", "immediately" → High
  - meeting invitations or routine work → Medium
  - newsletters/promotions → Low

- If the email contains a meeting date or time, store it in "deadline".

- If no sender email exists, return null.
"""

def analyze_email(email_text: str) -> Email:
    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": f"Analyze this email:\n\n{email_text}",
        },
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format={"type": "json_object"},
    )

    email_data = json.loads(response.choices[0].message.content)
    return Email.model_validate(email_data)
    

def save_email(email: Email, output_path: Path):

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(email.model_dump_json(indent=4))


email_folder = Path("emails")
output_folder = Path("output")
        

def process_emails():
    email_folder = Path("emails")
    output_folder = Path("output")

    output_folder.mkdir(parents=True, exist_ok=True)

    for file_path in sorted(email_folder.glob("*.txt")):
        print(f"Processing: {file_path.name}")

        try:
            email_text = read_email(file_path)
            email = analyze_email(email_text)

            output_file = output_folder / f"{file_path.stem}.json"
            save_email(email, output_file)

            print(f"Saved: {output_file.name}")

        except Exception as e:
            print(f"Failed: {file_path.name}")
            print(f"Error: {e}")

def load_processed_emails(output_folder : Path) -> list[dict]:
    
    emails = []
    
    json_files = sorted(output_folder.glob("*.json"))

    print(f"Found {len(json_files)} processed email(s).\n")

    for json_file in json_files:
        with json_file.open("r", encoding="utf-8") as file:
            emails.append(json.load(file))

    return emails

def generate_statistics(emails : list[dict]) -> dict:
    
    """Generate summary statistics from processed emails."""
    
    category_frequency = {}
    priority_frequency = {}
    sentiment_frequency = {}
    emails_with_action = 0
    emails_with_deadline = 0
    
    for email in emails:
        
        priority = email["priority"]

        if priority is not None:
            priority_frequency[priority] = (
                priority_frequency.get(priority, 0) + 1
            )
                
        category = email["category"]

        if category is not None:
            category_frequency[category] = (
                category_frequency.get(category, 0) + 1
            )
                
        sentiment = email["sentiment"]

        if sentiment is not None:
            sentiment_frequency[sentiment] = (
                sentiment_frequency.get(sentiment, 0) + 1
            )
        
        if email.get("action_required") is not None:
            emails_with_action += 1
            
        if email.get("deadline") is not None:
            emails_with_deadline += 1
    
    return {
            "total_emails": len(emails),
            "category_frequency": category_frequency,
            "priority_frequency": priority_frequency,
            "sentiment_frequency": sentiment_frequency,
            "emails_with_action": emails_with_action,
            "emails_with_deadline": emails_with_deadline,
        }

def print_report(stats : dict):
    
    print("=" * 50)
    print("EMAIL OPERATIONS REPORT")
    print("=" * 50)

    print(f"Total Emails : {stats['total_emails']}")

    print("\nCategory Breakdown")
    print("-" * 25)

    for category, count in sorted(stats["category_frequency"].items()):
        print(f"{category:<12} : {count}")

    print("\nPriority Breakdown")
    print("-" * 25)

    for priority, count in sorted(stats["priority_frequency"].items()):
        print(f"{priority:<12} : {count}")

    print("\nSentiment Breakdown")
    print("-" * 25)

    for sentiment, count in sorted(stats["sentiment_frequency"].items()):
        print(f"{sentiment:<12} : {count}")

    print("\nOther Statistics")
    print("-" * 25)

    print(f"Emails Requiring Action : {stats['emails_with_action']}")
    print(f"Emails With Deadlines   : {stats['emails_with_deadline']}")


def main():
    output_folder = Path("output")
    
    process_emails()

    emails = load_processed_emails(output_folder)

    stats = generate_statistics(emails)

    print_report(stats)
    
if __name__ == "__main__":
    main()
