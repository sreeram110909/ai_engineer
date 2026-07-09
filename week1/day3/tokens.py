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

prompt1 = "hi!"
prompt2 = "explain the fundamentals of LLMs"
prompt3 = "Write a 1000 word essay on Machine learning"

prompts = [prompt1, prompt2, prompt3]

for prompt in prompts:
    message = {
        "role" : "user",
        "content" : prompt
    }
    
    messages = [message]
    
    response = client.chat.completions.create(model=model , messages=messages , max_tokens=500)
    
    usage = response.usage
    
    print(f"Prompt: {prompt} --> Your Tokens Used: {usage.prompt_tokens} , Completion Tokens Used: {usage.completion_tokens} , Total Tokens Used: {usage.total_tokens} && Finish Reason: {response.choices[0].finish_reason}")
