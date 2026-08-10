import select
import sys

from .config import client, model
from .matcher import calculate_match, explain_match
from .models import Resume
from .parsers import jd_parser, resume_parser


def get_user_input(prompt: str = "\nRecruiter: ") -> str:
    """Reads single-line or pasted multi-line input from the terminal in one go."""
    print(prompt, end="", flush=True)
    first_line = sys.stdin.readline()
    if not first_line:
        return ""

    lines = [first_line]
    while True:
        readable, _, _ = select.select([sys.stdin], [], [], 0.08)
        if readable:
            line = sys.stdin.readline()
            if not line:
                break
            lines.append(line)
        else:
            break

    return "".join(lines).strip()


def chatwith_resume(resume: Resume | str):
    """Interactive recruiter chatbot interface with independent fresh question calls."""
    if isinstance(resume, Resume):
        candidate_info = resume.model_dump_json(indent=2)
        resume_obj = resume
    else:
        candidate_info = resume
        resume_obj = resume_parser(resume)

    # Current JD and its match result
    current_jd = None
    current_match = None

    print("\n" + "=" * 55)
    print("🤖 AI Portfolio Chatbot Ready!")
    print("You can ask questions, or type '/jd' to evaluate a Job Description.")
    print("Type 'exit' or 'quit' to end the session.")
    print("=" * 55)

    while True:
        user_question = get_user_input("\nRecruiter: ")

        # Ignore empty input
        if not user_question:
            continue

        # Exit
        if user_question.lower() in ["exit", "quit", "bye"]:
            print("\nAI: Thank you for your time! Goodbye.")
            break

        # --------------------------------------------------
        # JOB DESCRIPTION MODE (/jd)
        # --------------------------------------------------
        if user_question.lower().startswith("/jd"):
            rest = user_question[3:].strip()
            if rest:
                jd_text = rest
            else:
                print("\nPaste the complete job description.")
                print("Type END on a new line when finished.\n")
                jd_lines = []
                while True:
                    line = input()
                    if line.strip() == "END":
                        break
                    jd_lines.append(line)
                jd_text = "\n".join(jd_lines).strip()

            if not jd_text:
                print("\nAI: No job description provided.")
                continue

            print("\nAI: Analyzing the job description against Chinnu's resume across skills, experience, and projects...")

            current_jd = jd_parser(jd_text)
            current_match = calculate_match(resume_obj, current_jd)
            analysis = explain_match(resume_obj, current_jd, current_match)

            print("\n" + "=" * 55)
            print(f"📊 MATCH EVALUATION: {current_match.match_score}%")

            if current_jd.job_title:
                print(f"💼 Role: {current_jd.job_title}")

            print("=" * 55)

            print("\nMatching Skills:")
            if current_match.matching_skills:
                for skill in current_match.matching_skills:
                    print(f"  ✓ {skill}")
            else:
                print("  None")

            print("\nMissing / Gap Skills:")
            if current_match.missing_skills:
                for skill in current_match.missing_skills:
                    print(f"  ✗ {skill}")
            else:
                print("  None")

            if current_match.matching_preferred_skills:
                print("\n🌟 Matching Preferred Skills:")
                for skill in current_match.matching_preferred_skills:
                    print(f"  ✓ {skill}")

            if current_match.relevant_experience:
                print("\n💼 Relevant Experience:")
                for experience in current_match.relevant_experience:
                    print(f"  ✓ {experience}")

            if current_match.relevant_projects:
                print("\n🚀 Relevant Projects:")
                for project in current_match.relevant_projects:
                    print(f"  ✓ {project}")

            print("\n🎓 Qualification Checks:")
            if current_jd.minimum_experience_years is not None and current_jd.minimum_experience_years > 0:
                if resume_obj.total_experience_years is None:
                    exp_status = "⚠ Unable to verify required experience from resume"
                elif resume_obj.total_experience_years >= current_jd.minimum_experience_years:
                    exp_status = f"✓ Requirement met ({resume_obj.total_experience_years} yrs vs {current_jd.minimum_experience_years} yrs required)"
                else:
                    exp_status = f"✗ Below requirement ({resume_obj.total_experience_years} yrs vs {current_jd.minimum_experience_years} yrs required)"
            else:
                exp_status = "✓ No minimum experience required"

            edu_status = "✓ Requirement met" if current_match.education_match else "• Review required"
            print(f"  • Experience Criteria: {exp_status}")
            print(f"  • Education Criteria:  {edu_status}")

            print("\n📝 Candidate Suitability Analysis:")
            print(analysis)
            print("=" * 55)

            continue

        # --------------------------------------------------
        # FRESH RECRUITER QUESTION FLOW
        # --------------------------------------------------
        current_context = ""
        if current_jd is not None:
            current_context = f"""
            CURRENT JOB DESCRIPTION:
            {current_jd.model_dump_json(indent=2)}

            CURRENT MATCH RESULT:
            {current_match.model_dump_json(indent=2)}
            """

        system_prompt = f"""
        You are an AI assistant representing the person
        whose resume is provided below.

        CANDIDATE INFORMATION:
        {candidate_info}

        {current_context}

        RULES:
        1. Answer ONLY the recruiter's latest question.
        2. Treat every new recruiter message as a new question.
        3. Do not answer previous questions again.
        4. Do not repeat previous answers.
        5. Do not combine the current question with previous recruiter questions.
        6. Answer directly and concisely.
        7. Never invent information.
        8. Use only the candidate information provided.
        9. If the information is unavailable, say:
           "I don't have that information in Chinnu's portfolio."
        10. Do not unnecessarily mention unrelated skills.
        11. If the recruiter asks for a ranking or evaluation, you may make a reasoned assessment using only the evidence in the resume.
        12. Clearly distinguish an assessment from a factual claim.
        13. If a current JD exists, use it only when the question is related to that JD.
        14. Never change the calculated match score.
        15. Do not repeat the complete JD analysis unless the recruiter explicitly asks for it.
        """

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question},
            ],
            stream=True,
        )

        answer = ""
        print("\nAI: ", end="")
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                print(content, end="", flush=True)
                answer += content
        print()
