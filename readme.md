# 🚀 Job Search AI

An AI-powered Resume Screening & Job Matching System built using **FastAPI**, **Python**, **SQLite**, **HTML/CSS**, and **Jinja2**.

The application automatically extracts candidate information from uploaded resumes, matches skills against job descriptions, calculates a match score, and provides a recruiter-friendly dashboard.

---

# 📌 Features

## ✅ Resume Upload

* Upload PDF/DOCX resumes
* Automatically extract:

  * Candidate Name
  * Email
  * Mobile Number
  * Skills
* Supports PDF & DOCX formats

---

## ✅ AI Resume Parsing

Automatically extracts:

* Name
* Email
* Phone Number
* Skills
* Resume Text

---

## ✅ Job Matching

Compares resume skills with predefined job roles.

Provides:

* Match Percentage
* Job-wise Skill Matching
* Best Matching Role

---

## ✅ Dashboard

Displays:

* Total Uploaded Resumes
* Highest Match Score
* Average Match Score
* Resume Analytics Chart
* Top Candidates
* Recent Uploads

---

## ✅ Resume Search

Search resumes using:

* Candidate Name
* Email
* Mobile Number
* Match Score

---

## ✅ Duplicate Resume Detection

Duplicate resumes are detected using:

* Email
* Mobile Number

If a duplicate is uploaded:

* Existing record is updated
* Old resume file is removed
* Database remains clean

---

## ✅ Resume Download

Recruiters can download uploaded resumes directly from the dashboard.

---

## ✅ Resume Delete

Deletes:

* Resume record from SQLite
* Resume file from uploads folder

---

## 📂 Project Structure

```
job-search-ai/

│

├── app.py

├── database.db

├── requirements.txt

├── templates/

│ ├── index.html

│ ├── dashboard.html

│ ├── history.html

│ └── result.html

│

├── static/

│ ├── style.css

│ └── script.js

│

├── uploads/

│

├── resume_parser.py

├── job_matcher.py

├── README.md

└── Dockerfile (Coming Soon)
```

---

# 🛠 Tech Stack

Backend

* Python
* FastAPI

Frontend

* HTML5
* CSS3
* Jinja2

Database

* SQLite

Libraries

* pdfplumber
* python-docx
* regex
* Uvicorn

---

# ⚙ Installation

Clone Repository

```bash
git clone https://github.com/<your-github>/job-search-ai.git

cd job-search-ai
```

Create Virtual Environment

```bash
python3 -m venv venv
```

Activate

Ubuntu

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install Packages

```bash
pip install -r requirements.txt
```

Run Application

```bash
uvicorn app:app --reload
```

Open Browser

```
http://localhost:8000
```

---

# 📊 Dashboard

The dashboard provides:

* Resume Statistics
* Candidate Ranking
* Match Score Analytics
* Search Functionality
* Resume Download
* Resume Delete

---

# 📈 Current Progress

✅ Resume Upload

✅ Resume Parsing

✅ Job Matching

✅ Dashboard

✅ Analytics

✅ Resume Search

✅ Duplicate Detection

✅ Resume Download

✅ Resume Delete

---

# 🚧 Upcoming Features

* Docker Containerization
* Docker Compose
* Nginx Reverse Proxy
* AWS EC2 Deployment
* GitHub Actions CI/CD
* Terraform Infrastructure
* Prometheus Monitoring
* Grafana Dashboard
* AI Resume Recommendation
* AI Candidate Ranking
* JWT Authentication
* PostgreSQL Migration

---

# 👨‍💻 Author

**Shreyash Sadanand Deshpande**

Linux | AWS | Docker | DevOps | Site Reliability Engineer

---

# ⭐ If you like this project

Please consider giving this repository a ⭐ on GitHub.
