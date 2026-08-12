from urllib import response
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("Missing GROQ API Key")

client = Groq(api_key = my_api_key)

model = "llama-3.1-8b-instant"

# step 1
knowledge_base={
    "age" : " The age of sree ram is 25 years",
    "net worth" : "The net worth of sree is 2000"
}

# step 2

def retrieve_info(question):
    question=question.lower()

    if("age" in question):
        return knowledge_base["age"]
    elif("net worth" in question):
        return knowledge_base["net worth"]
    else:
        return ""

def call_llm(question):

    context=retrieve_info(question)

    system_prompt = f"""
    answer in one line only. Answer only based on this context. do not hallucinate.Context: {context}
    """

    system_message = {
        "role" : "system",
        "content" : system_prompt
    }

    user_message = {
        "role" : "user",
        "content" : question
    }
    messages = [system_message , user_message]

    response = client.chat.completions.create(model=model, messages=messages)
    answer=response.choices[0].message.content
    return answer

question = "what is the age of sree ram"

print(call_llm(question))