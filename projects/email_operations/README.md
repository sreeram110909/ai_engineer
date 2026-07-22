# Email Operations

An AI-powered email analysis and reporting system that processes raw email files, extracts structured information using a Large Language Model (LLM), validates the output with Pydantic, and generates summary analytics.

This project demonstrates practical AI engineering concepts including prompt engineering, structured output generation, schema validation, batch processing, and analytics.

---

## Features

- Process multiple email files automatically
- Extract structured information using an LLM
- Validate responses with Pydantic
- Save structured outputs as JSON
- Generate analytics and summary reports
- Handle missing values gracefully
- Organized and reusable Python functions

---

## Project Structure

```text
email_operations/
│
├── emails/                # Input email files (.txt)
├── output/                # Generated JSON files
├── email_operations.py    # Main application
├── .env                   # Environment variables
├── requirements.txt
└── README.md
```

---

## Technologies Used

- Python 3.11+
- Groq API
- Pydantic
- python-dotenv
- pathlib
- JSON

---

## Workflow

```text
          Raw Email (.txt)
                  │
                  ▼
          Read Email Files
                  │
                  ▼
       LLM Email Analysis (Groq)
                  │
                  ▼
      Pydantic Schema Validation
                  │
                  ▼
         Structured JSON Output
                  │
                  ▼
        Analytics & Report Generation
```

---

## Extracted Information

Each email is converted into a structured JSON object containing:

- Sender Email
- Subject
- Summary
- Category
- Priority
- Action Required
- Deadline
- Sentiment

Example:

```json
{
    "sender_email": "hr@company.com",
    "subject": "Interview Invitation",
    "summary": "The candidate is invited for an interview on Friday at 2 PM.",
    "category": "Job",
    "priority": "Medium",
    "action_required": "Confirm attendance",
    "deadline": "Friday 2:00 PM",
    "sentiment": "Positive"
}
```

---

## Generated Analytics

After processing all emails, the application generates a report including:

- Total Emails Processed
- Category Distribution
- Priority Distribution
- Sentiment Distribution
- Emails Requiring Action
- Emails Containing Deadlines

Example:

```text
==================================================
EMAIL OPERATIONS REPORT
==================================================

Total Emails : 10

Category Breakdown
-------------------------
Finance      : 1
Job          : 2
Promotion    : 1
Shopping     : 1
Support      : 2
Work         : 3

Priority Breakdown
-------------------------
Low          : 2
Medium       : 6

Sentiment Breakdown
-------------------------
Neutral      : 6
Positive     : 4

Other Statistics
-------------------------
Emails Requiring Action : 8
Emails With Deadlines   : 4
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd email_operations
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

macOS/Linux

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_api_key_here
```

---

## Running the Project

Place email files inside the `emails` directory.

Run:

```bash
python email_operations.py
```

Processed JSON files will be saved inside the `output` directory.

---

## Sample Input

```text
emails/
├── 01_meeting_request.txt
├── 02_leave_request.txt
├── 03_job_application.txt
├── ...
```

---

## Sample Output

```text
output/
├── 01_meeting_request.json
├── 02_leave_request.json
├── 03_job_application.json
├── ...
```

---

## Concepts Demonstrated

- Prompt Engineering
- Structured Output Generation
- Pydantic Validation
- Batch File Processing
- JSON Serialization
- Frequency Map Analytics
- Error Handling
- Modular Function Design
- Environment Variable Management

---

## Future Improvements

- Modular project structure (`main.py`, `analytics.py`, `analyzer.py`, `models.py`)
- Command Line Interface (CLI)
- CSV and Excel report export
- Interactive dashboard
- Email thread analysis
- Date parsing and timeline visualization
- REST API using FastAPI
- Unit testing
- Docker support

---

## Learning Outcomes

This project demonstrates practical AI engineering workflows by combining LLM-powered information extraction with structured validation, data processing, and analytics. It provides hands-on experience in building reliable AI applications that transform unstructured text into actionable insights.

---

## License

This project is intended for educational and learning purposes.