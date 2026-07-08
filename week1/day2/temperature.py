import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=api_key)

messages = [
    {
        "role": "system",
        "content": "You are a creative storyteller."
    },
    {
        "role": "user",
        "content": "Write a funny name for an alien pet."
    }
]

# Temperature = 0
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    temperature=0,
)

print("Temperature = 0")
print(response.choices[0].message.content)

print("\n" + "#" * 40 + "\n")

# Temperature = 1
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    temperature=1,
)

print("Temperature = 1")
print(response.choices[0].message.content)

print("\n" + "#" * 40 + "\n")

# Temperature = 2
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    temperature=2,
)

print("Temperature = 2")
print(response.choices[0].message.content)