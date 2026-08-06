import os
from groq import Groq
from dotenv import load_dotenv
from time import sleep

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY not found")

client = Groq(api_key = my_api_key)
model = "llama-3.3-70b-versatile"

JD = """
Job Title: AI/ML Engineer
Company: TechNova Solutions
Location: San Francisco, CA

About the Role:

We are looking for an experienced AI/ML Engineer to join our dynamic R&D team. The ideal candidate will have a strong background in machine learning, deep learning, and natural language processing, with proven experience in developing and deploying AI solutions. You will work on cutting-edge projects, collaborating with cross-functional teams to deliver high-impact solutions that drive business value.

Key Responsibilities:

Design, develop, and deploy machine learning models for various applications.

Build and maintain data pipelines for model training and evaluation.

Implement natural language processing solutions for text understanding and generation.

Collaborate with product managers and software engineers to integrate AI features into products.

Monitor and improve model performance in production environments.

Stay updated with the latest advancements in AI/ML and apply them to solve real-world problems.

Qualifications:

Bachelor's or Master's degree in Computer Science, Data Science, Statistics, or a related field.

3+ years of experience in AI/ML engineering.

Strong programming skills in Python and experience with ML frameworks (TensorFlow, PyTorch, scikit-learn).

Experience with cloud platforms such as AWS, GCP, or Azure.

Familiarity with NLP libraries (spaCy, Hugging Face Transformers) is a plus.

Excellent problem-solving skills and ability to work independently and as part of a team.
"""

resume = """
name: Sreeram Banoth
email: [EMAIL_ADDRESS]
phone: 1234567890
total_experience_years: 3.5
skills: [Python, ML, DL, NLP]
experiences: [{"company": "TechNova", "role": "AI/ML Engineer", "duration": "3.5 years", "responsibilities": ["Design, develop, and deploy machine learning models for various applications.", "Build and maintain data pipelines for model training and evaluation.", "Implement natural language processing solutions for text understanding and generation.", "Collaborate with product managers and software engineers to integrate AI features into products.", "Monitor and improve model performance in production environments.", "Stay updated with the latest advancements in AI/ML and apply them to solve real-world problems."]}]
education: ["Bachelor's degree in Computer Science, Data Science, Statistics, or a related field"]
projects: ["AI/ML project"]
certifications: ["AI/ML certification"]
"""

def ask_llm(system_prompt , user_prompt):

    system_message = {
        "role" : "system",
        "content" : system_prompt
    }

    user_message = {
        "role" : "user",
        "content" : user_prompt
    }

    message = [system_message, user_message]
    response = client.chat.completions.create(
        model = model,
        messages = message
    )
    ans = response.choices[0].message.content
    return ans

def step1_resume_extractor(resume):
    system_prompt="""
    You are a professional HR assistant. Extract the skills from the candidates resume provided.
    Only return the skills no other information. Do not invent any skillsby yourself.
    Output Format:
    Skills should be separated by commas. Just return comma separated skills do not return any other filler information
    """
    user_prompt=f"""
    Extract the skills from this resume
    {resume}
    """
    return ask_llm(system_prompt, user_prompt)

def step2_JD_extract(JD):
    system_prompt="""
    You are a professional HR assistant. Extract the skills from the Job description  provided.
    Only return the skills no other information. Do not invent any skills by yourself.
    Output Format:
    Skills should be separated by commas. Just return comma separated skills do not return any other filler information
    """
    user_prompt=f"""
    Extract the skills from this JD
    {JD}
    """
    return ask_llm(system_prompt, user_prompt)


def step3_match(candidate,jd):
    print("step3")
    system_prompt="""
    You are a professional HR assistant. compare the skills of candidate and the skills required in the JD and produce a final score between
    1 and 100. also produce a short verdict whther the candidate is a good fit for the role.
    """
    user_prompt=f"""
    Compare and match the skills
    JD:
    {jd}
    Candidate:
    {candidate}
    """
    return ask_llm(system_prompt, user_prompt)

candidate=step1_resume_extractor(resume)
print(candidate)
sleep(2)
jd=step2_JD_extract(JD)
print(jd)
sleep(2)
score=step3_match(candidate,jd)
print(score)