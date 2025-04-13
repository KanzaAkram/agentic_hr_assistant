# Agentic HR Assistant Pro 👔

A Streamlit-based application leveraging multiple AI agents to automate and streamline the initial stages of the recruitment process, from job description creation to candidate analysis and initial communication.

![Screenshot (Optional - Add a screenshot of your app here)]

## Table of Contents

1.  [Project Overview](#project-overview)
2.  [Key Features](#key-features)
3.  [How it Works: The Agents](#how-it-works-the-agents)
    *   [Job Description Agent](#job-description-agent)
    *   [Resume Parser Agent](#resume-parser-agent)
    *   [Candidate Analyzer Agent](#candidate-analyzer-agent)
    *   [Communication Agent](#communication-agent)
4.  [Technology Stack](#technology-stack)
5.  [Project Setup](#project-setup)
    *   [Prerequisites](#prerequisites)
    *   [Installation](#installation)
    *   [Configuration](#configuration)
6.  [Running the Application](#running-the-application)
7.  [Usage Guide](#usage-guide)
    *   [Step 1: Configuration](#step-1-configuration)
    *   [Step 2: Job Description](#step-2-job-description)
    *   [Step 3: Resume Analysis](#step-3-resume-analysis)
    *   [Step 4: Communication Dashboard](#step-4-communication-dashboard)

## Project Overview

Agentic HR Assistant Pro is designed to assist HR professionals and hiring managers by automating repetitive tasks in the recruitment pipeline. It uses a multi-agent system, where each agent specializes in a specific task, collaborating to provide a seamless workflow. The application helps in:

*   Generating and refining professional job descriptions.
*   Parsing candidate resumes (PDFs) to extract text.
*   Analyzing resumes against the job description to score and evaluate candidates.
*   Automating initial candidate screening based on predefined criteria.
*   Generating personalized interview invitation emails.
*   Sending emails automatically to approved candidates.
*   Managing interview schedules and communication history.

## Key Features

*   **AI-Powered Job Description:** Generate comprehensive JDs or refine existing ones using Google Gemini.
*   **JD Validation:** Analyze JDs for clarity, completeness, and potential bias.
*   **PDF Resume Parsing:** Extract text content from uploaded PDF resumes.
*   **Automated Candidate Analysis:** Score candidates based on skills and experience match against the JD using AI.
*   **Structured Candidate Insights:** Provides key skills, strengths, weaknesses, and recommendations for each candidate.
*   **Configurable Auto-Approval:** Set a score threshold for automatic candidate approval.
*   **AI-Assisted Interview Scheduling:** Recommends optimal interview slots for approved candidates.
*   **Automated Email Communication:** Generates and sends personalized interview invitations via Gmail.
*   **Centralized Dashboard:** View candidate rankings, analysis results, interview schedules, and email history.
*   **Interview Slot Management:** Add and manage available interview time slots.
*   **User-Friendly Interface:** Built with Streamlit for an interactive web application experience.

## How it Works: The Agents

The core of this application lies in its specialized agents, each handling a distinct part of the recruitment workflow:

### Job Description Agent (`agents/job_description_agent.py`)

*   **Purpose:** Handles all tasks related to job descriptions.
*   **Technology:** Uses Google Gemini (via `langchain_google_genai`) for natural language understanding and generation.
*   **Functions:**
    *   `generate_job_description()`: Creates a new JD based on role, industry, experience, skills, and company details.
    *   `refine_job_description()`: Modifies an existing JD based on user instructions and company context.
    *   `validate_job_description()`: Analyzes a JD for potential issues like bias, vagueness, and missing sections, offering suggestions.

### Resume Parser Agent (`agents/resume_parser_agent.py`)

*   **Purpose:** Extracts raw text and basic information from PDF resumes.
*   **Technology:** Uses `PyPDF2` for PDF text extraction and `re` (regular expressions) for simple pattern matching (email, phone).
*   **Functions:**
    *   `extract_text_from_pdf()`: Reads a PDF file object and returns its text content.
    *   `extract_email()`: Finds potential email addresses in the text.
    *   `extract_phone()`: Finds potential phone numbers in the text.
    *   `extract_name()`: Attempts to identify the candidate's name from the text or filename.
    *   *Note:* This agent focuses on extraction, not complex analysis.

### Candidate Analyzer Agent (`agents/candidate_analyzer_agent.py`)

*   **Purpose:** Analyzes the extracted resume text against the confirmed job description to evaluate candidate suitability.
*   **Technology:** Uses Google Gemini (via `langchain_google_genai`) for in-depth analysis and structured data generation (JSON).
*   **Functions:**
    *   `analyze_resume()`: Compares resume text to the JD, outputting a JSON containing name, email, skill/experience match percentages, overall score, key skills, strengths, weaknesses, and a hiring recommendation.
    *   `_make_automatic_decision()`: (Internal helper) Determines an initial status (Approved, Pending, Rejected) based on the analysis score and recommendation.
    *   `rank_candidates()`: Ranks a list of analyzed candidates based on weighted scores (customizable).
    *   `get_best_interview_time_slot()`: Recommends an available interview slot for a candidate using AI, considering their profile and availability.

### Communication Agent (`agents/communication_agent.py`)

*   **Purpose:** Manages automated communication with candidates.
*   **Technology:** Uses Google Gemini (via `langchain_google_genai`) for email content generation and Python's `smtplib` and `email` modules for sending emails via Gmail SMTP.
*   **Functions:**
    *   `generate_interview_email()`: Creates a personalized interview invitation email body and subject line based on candidate info, JD, and interview details.
    *   `generate_rejection_email()`: Creates a professional rejection email (optional feedback included).
    *   `send_email()`: Connects to Gmail using provided credentials (email and App Password) and sends the generated email. Requires SMTP configuration.

## Technology Stack

*   **Backend/Logic:** Python 3.x
*   **Web Framework:** Streamlit
*   **AI/LLM:** Google Gemini (via `langchain-google-genai`)
*   **PDF Parsing:** PyPDF2
*   **Data Handling:** Pandas
*   **Email:** smtplib, email (Python Standard Libraries)
*   **Configuration:** (Optional but recommended) `python-dotenv`

## Project Setup

### Prerequisites

*   Python 3.8 or higher
*   `pip` (Python package installer)
*   Git (for cloning the repository)
*   **Google Gemini API Key:** Obtain from [Google AI Studio](https://aistudio.google.com/app/apikey) or Google Cloud Console.
*   **Gmail Account:** For sending emails.
*   **Gmail App Password:** **Crucially, you need an App Password, not your regular Gmail password.** Generate one from your Google Account settings:
    1.  Go to your Google Account -> Security.
    2.  Ensure 2-Step Verification is ON.
    3.  Go to App passwords.
    4.  Select "Mail" for the app and "Other (Custom name)" for the device (e.g., "HR Assistant Pro").
    5.  Generate the password and copy the 16-character code. **Save this securely.**

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Create a `requirements.txt` file:**
    Based on the imports in your code, create a file named `requirements.txt` in the project root with the following content:

    ```txt
    streamlit
    pandas
    PyPDF2
    langchain-google-genai
    # Add any other specific dependencies if needed
    # Optional: python-dotenv (if using .env for keys)
    ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

You need to provide your API keys and email credentials to the application. You can do this directly via the Streamlit sidebar when the app runs, or for better security and management (especially if deploying), use environment variables.

**Option 1: Input via Sidebar (as coded)**

*   Run the application (`streamlit run main.py`).
*   Enter your Google Gemini API Key, Gmail Email Address, and the generated Gmail App Password in the sidebar fields.

**Option 2: Using Environment Variables (Recommended Practice)**

1.  Create a file named `.env` in the project root directory.
2.  Add your credentials to the `.env` file:
    ```env
    GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
    GMAIL_EMAIL="your_email@gmail.com"
    GMAIL_PASSWORD="your_16_character_app_password"
    ```
3.  (Optional) Install `python-dotenv`: `pip install python-dotenv`
4.  Modify `main.py` (and potentially agent initializations) to load these variables at the start using `load_dotenv()` from the `dotenv` library. *Note: The current code reads directly from `st.text_input`, so you would need to adjust it to prioritize environment variables if they exist.*

## Running the Application

1.  Ensure your virtual environment is activated.
2.  Make sure you are in the project's root directory (where `main.py` is located).
3.  Run the Streamlit application:
    ```bash
    streamlit run main.py
    ```
4.  The application should open in your default web browser.

## Usage Guide

### Step 1: Configuration

1.  Open the application in your browser.
2.  Navigate to the **sidebar** on the left.
3.  Enter your **Google Gemini API Key**.
4.  Enter your **Gmail Email Address**.
5.  Enter your **Gmail App Password** (the 16-character code you generated).
6.  Adjust **Automation Settings**:
    *   Set the **Auto-approve threshold** (score percentage).
    *   Enable/disable **Auto-generate & send interview emails**.
    *   Enter the default **Interviewer Name** and **Company Name**.
7.  The application will initialize the agents once the Gemini API key is provided. Check for any error messages in the sidebar.

### Step 2: Job Description (Tab 1)

1.  Select whether you want to **Generate New** or **Refine Existing**.
2.  **Generate New:**
    *   Enter the **Job Role**.
    *   Fill in **Company Name** and **Company Specialization**.
    *   Select **Industry**, **Experience Level**.
    *   Provide comma-separated **Key Skills Required**.
    *   Click **Generate Job Description**.
3.  **Refine Existing:**
    *   Paste the existing job description into the text area.
    *   Provide **Refinement instructions**.
    *   Click **Refine Job Description**.
4.  The generated/refined JD will appear. You can **edit it directly** in the text area below.
5.  (Optional) Click **Validate JD** to get AI feedback on the description.
6.  Once satisfied, click **Confirm and Continue**. This saves the JD in the application's state for the next steps.

### Step 3: Resume Analysis (Tab 2)

1.  Ensure a Job Description has been confirmed in Tab 1.
2.  Click **Browse files** under "Upload candidate resumes (PDF)" and select one or more PDF resume files.
3.  Click **Process Resumes**.
4.  The application will:
    *   Extract text from each PDF using the `ResumeParserAgent`.
    *   Analyze each resume against the confirmed JD using the `CandidateAnalyzerAgent`.
    *   Score each candidate (Skills Match %, Experience Match %, Overall Score).
    *   Provide key skills, strengths, weaknesses, and a recommendation.
    *   Apply an **Automated Decision** based on the score and the threshold set in the sidebar.
5.  **Automated Actions (if enabled):**
    *   If **Auto-generate & send interview emails** is checked and email credentials are valid, the system will automatically:
        *   Identify candidates whose status is "Approved".
        *   Use the `CandidateAnalyzerAgent` to pick the best available interview slot.
        *   Use the `CommunicationAgent` to generate a personalized interview email.
        *   Send the email via Gmail.
        *   Mark the interview slot as unavailable.
        *   Update the candidate's "Email Sent" status.
6.  **Review Results:**
    *   The candidate analysis results appear in an editable table.
    *   Use the **filters** (Minimum Score, Recommendation, Status) to narrow down the list.
    *   You can **manually change the Status** of any candidate directly in the table (e.g., change "Pending" to "Approved" or "Rejected"). *Note: Manually approving might trigger email sending if auto-email is enabled for newly approved candidates (check the specific logic implemented around the "Send Interview Invitations" button).*
    *   View the **Analysis Summary** metrics.

### Step 4: Communication Dashboard (Tab 3)

1.  **Interview Schedule:** View a table of all candidates who have been sent interview invitations, including the scheduled date and time.
2.  **Email History:** See a list of all emails sent by the system.
    *   Check the **View Email Content** box and select an email from the dropdown to see the exact subject and body sent.
3.  **Interview Slot Management:**
    *   View the list of currently available/unavailable interview slots.
    *   Add a **New Interview Slot** by entering the date and time and clicking "Add Slot".
    *   Add **Multiple Slots** in bulk by specifying a date range and times per day.

