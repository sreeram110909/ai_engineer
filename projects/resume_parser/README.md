# AI-Powered ATS Resume Screening System

## Overview

This project is an AI-powered Applicant Tracking System (ATS) that
automates resume screening using a Large Language Model (LLM). It
extracts structured information from both job descriptions and resumes,
validates the extracted data using Pydantic models, compares candidates
against the job requirements, assigns an ATS score, and ranks candidates
based on their suitability.

The project demonstrates how modern LLMs can be combined with structured
validation and document processing to build an end-to-end recruitment
assistant.

------------------------------------------------------------------------

# System Architecture

``` text
                    Job Description
                           │
                           ▼
                LLM extracts information
                           │
                           ▼
                 Structured Job Data
                           │
                           ▼
                 Pydantic Validation
                           │

══════════════════════════════════════════════

                  Resume PDF / DOCX
                           │
                           ▼
                  Resume Text Extraction
                           │
                           ▼
                  Resume Parser (LLM)
                           │
                           ▼
               Structured Resume Data
                           │
                           ▼
                 Pydantic Validation
                           │

══════════════════════════════════════════════

           Structured Job + Structured Resume
                           │
                           ▼
                 Resume Matching (LLM)
                           │
                           ▼
               Structured Match Result
                           │
                           ▼
                     ATS Score
                           │
                           ▼
                  Candidate Ranking
                           │
                           ▼
                    Final Report
```

------------------------------------------------------------------------

# Workflow

1.  Load the Groq API key from the environment.
2.  Read the job description.
3.  Send the job description to the LLM.
4.  Convert the LLM response into a validated `JobD` object using
    Pydantic.
5.  Read every resume from the `resumes` directory.
6.  Extract text from PDF or DOCX files.
7.  Send the resume text to the LLM.
8.  Convert the response into a validated `Resume` object.
9.  Compare the structured resume with the structured job description
    using the LLM.
10. Generate an ATS score and evaluation.
11. Rank candidates by score.
12. Display the highest and lowest ranked candidates.

------------------------------------------------------------------------

# Features

-   Job description parsing using LLMs
-   Resume parsing from PDF and DOCX
-   Structured JSON generation
-   Pydantic schema validation
-   Resume-to-job matching
-   ATS score generation
-   Candidate ranking
-   Batch processing of multiple resumes
-   Support for PDF and DOCX formats
-   Environment variable configuration using `.env`

------------------------------------------------------------------------

# Technology Stack

-   Python 3.11+
-   Groq API
-   openai/gpt-oss-120b
-   Pydantic
-   python-dotenv
-   pypdf
-   python-docx
-   pathlib
-   JSON

------------------------------------------------------------------------

# Project Structure

``` text
project/
│
├── mini_project.py
├── README.md
├── requirements.txt
├── .env
└── resumes/
    ├── candidate1.pdf
    ├── candidate2.pdf
    └── candidate3.pdf
    
```

------------------------------------------------------------------------

# Pydantic Models

The application uses four primary models:

-   JobD
    -   Role
    -   Required Skills
    -   Preferred Skills
    -   Education Requirements
    -   Minimum Experience
    -   Responsibilities
-   Experience
    -   Company
    -   Role
    -   Duration
    -   Description
    -   Skills Used
-   Resume
    -   Personal Information
    -   Skills
    -   Experience
    -   Education
    -   Projects
    -   Certifications
-   MatchResult
    -   ATS Score
    -   Matching Details

------------------------------------------------------------------------

# Installation

## Clone the repository

``` bash
git clone https://github.com/<your-username>/day5.git
cd day5
```

## Create a virtual environment

``` bash
uv venv
```

Activate the environment.

macOS/Linux

``` bash
source .venv/bin/activate
```

Windows

``` bash
.venv\Scripts\activate
```

## Install dependencies

``` bash
uv pip install -r requirements.txt
```

------------------------------------------------------------------------

# Environment Variables

Create a `.env` file.

``` text
GROQ_API_KEY=your_api_key
```

------------------------------------------------------------------------

# Running the Project

Place all resumes inside the `resumes` folder.

Run:

``` bash
python mini_project.py
```

------------------------------------------------------------------------

# Input

## Job Description

A job description string containing:

-   Role
-   Responsibilities
-   Required Skills
-   Preferred Skills
-   Education
-   Experience

## Resume Files

Supported formats:

-   PDF
-   DOCX

------------------------------------------------------------------------

# Output

For every candidate the application produces:

-   Structured Resume
-   ATS Score
-   Matching Skills
-   Missing Skills
-   Experience Match
-   Final Verdict

After all resumes are processed the candidates are ranked according to
their ATS score.

------------------------------------------------------------------------

# Error Handling

The project includes validation for:

-   Missing API key
-   Invalid JSON responses
-   Unsupported file formats
-   Missing resume directory
-   Pydantic schema validation

------------------------------------------------------------------------

# Skills Demonstrated

-   Prompt Engineering
-   Structured Output Generation
-   LLM Integration
-   Information Extraction
-   Resume Parsing
-   Job Description Parsing
-   Pydantic Validation
-   Python File Handling
-   JSON Processing
-   Batch Processing
-   Candidate Ranking
-   Object-Oriented Programming

------------------------------------------------------------------------

# Future Improvements

-   Streamlit dashboard
-   FastAPI REST API
-   Excel export
-   Database integration
-   Recruiter dashboard
-   OCR support
-   Docker deployment
-   Authentication
-   Skill gap analysis
-   Resume improvement recommendations

------------------------------------------------------------------------

# Author

Banoth Sree Ram Nayak

B.Tech, Data Science and Artificial Intelligence

Indian Institute of Technology Guwahati
