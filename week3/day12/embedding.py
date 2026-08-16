import os
from dotenv import load_dotenv
import numpy as np
from sentence_transformers import SentenceTransformer


load_dotenv()

def cosine_similarity(vec1,vec2):
    return np.dot(vec1,vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2))

model = SentenceTransformer("all-MiniLM-L6-v2")

text = "Machine learning is fun."

# embedding=model.encode(text)
# print(embedding.shape)
# print(embedding)

vec1 = "There are 24 paid leaves"
vec2 = "There are 24 paid leaves"
vec1_embedding = model.encode(vec1)
vec2_embedding = model.encode(vec2)

print(cosine_similarity(vec1_embedding,vec2_embedding))



