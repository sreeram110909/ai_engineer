import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key)

model = "llama-3.3-70b-versatile"

role = "user"

prompt = "I Love you"

# MESSAGE SYSTEM( what is the relation between user and system)

message_system = {
    "role" : "system",
    "content" : "you are my lovely girlfrined"
}

message = {
    "role" : role,
    "content" : prompt
}

messages = [message_system, message]

response = client.chat.completions.create(model=model, messages=messages)

print(response.choices[0].message.content)

response2 = client.chat.completions.create(
    model = model,
    messages = [
        {
            "role" : "system",
            "content" : "you are my office collegue and also my manager"
        },
        
        {
            "role" : role,
            "content" : prompt
        }
    ]
)
print("#############################################")
print(response2.choices[0].message.content)