from httpcore import stream
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY not found")

client = Groq(api_key=my_api_key)

model = "llama-3.3-70b-versatile"

prompt = "tell me about the chernobyle disaster and who is the only person responsible for that."
message={
    "role" : "user",
    "content" : prompt
}

message = [message]

# response = client.chat.completions.create(model=model , messages= message)
# print(response)
# ans = response.choices[0].message.content
# print(ans)

stream = client.chat.completions.create(model=model , messages= message , stream = True)

for chunks in stream:
    content = chunks.choices[0].delta.content
    if content:
       print(content, end="", flush=True)



