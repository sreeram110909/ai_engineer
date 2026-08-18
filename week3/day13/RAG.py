import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import numpy as np
from sentence_transformers import SentenceTransformer
import sys

model = SentenceTransformer("all-MiniLM-L6-v2") #384

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError(" Environment variable GROQ_API_KEY not found")

client = Groq(api_key=my_api_key)
groqmodel = "openai/gpt-oss-20b"

documents = [
    "Employees receive 24 days of paid leave per year.",
   
    "Employees work from the office on Tuesday, Wednesday and Thursday. "
    "Monday and Friday are optional work-from-home days.",
   
    "Employees receive Rs 3000 per month for gym reimbursement.",
   
    "Employees can claim Rs 2000 per month for home internet.",
   
    "Employees have a 90 day notice period."
]

documents_embeddings = model.encode(documents)

print(sys.getsizeof(documents_embeddings))

def cosine_similarity(query_embedding, doc_embedding):

    return np.dot(query_embedding,doc_embedding)/(np.linalg.norm(query_embedding)*np.linalg.norm(doc_embedding))

def retrieve(qembedding):

    scores = []
    for i, document in enumerate(documents_embeddings):
        score = cosine_similarity(qembedding, document)
        scores.append((score, documents[i]))
    scores.sort(reverse = True)
    return scores[0]

def ask_llm(question,context):

    sys_prompt=f"""answer in one line only. Answer only based on this context. do not hallucinate. Context: {context}"""
    system_message={
        "role": "system",
        "content": sys_prompt

    }
    message={
        "role": "user",
        "content": question
    }
    messages=[system_message, message]
    response=client.chat.completions.create(model=groqmodel, messages=messages)
    answer=response.choices[0].message.content
    return answer

query = "how many days of paid leave do employees get?"
qembedding = model.encode(query)

score,context = retrieve(qembedding)

answer = ask_llm(query, context)

print(answer)
