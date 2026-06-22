# Job Search AI 🚀

A FastAPI-based Resume Screening and Job Matching System that automatically analyzes resumes, extracts candidate details, identifies technical skills, and calculates job match scores.

## Features

### Resume Upload

* Upload resumes in:

  * PDF
  * DOCX
  * TXT

### Candidate Information Extraction

* Candidate Name
* Email Address
* Mobile Number

### Skill Detection

The system currently detects:

* AWS
* Docker
* Kubernetes
* Terraform
* Jenkins
* Git
* Linux
* Python
* Ansible
* Prometheus
* Grafana
* MySQL
* Oracle
* Bash

### Job Matching Engine

The application compares candidate skills against predefined job requirements and calculates:

* Match Score (%)
* Matched Skills
* Recommended Jobs

### Database Storage

All uploaded resumes are stored in SQLite with:

* Resume Filename
* Candidate Name
* Email
* Mobile Number
* Skills
* Match Score
* Upload Timestamp

---

## Tech Stack

### Backend

* FastAPI
* Python 3

### Resume Parsing

* python-docx
* pypdf

### Database

* SQLite

### Future Enhancements

* Docker
* AWS EC2
* Nginx
* Prometheus
* Grafana

---

## Project Structure

job-search-ai/

├── app.py

├── jobs.py

├── database.db

├── uploads/

├── requirements.txt

└── README.md

---

## API Endpoints

### Home

GET /

Response:

{
"message": "Welcome to Job Search AI"
}

### Upload Resume

POST /upload

Upload:

* PDF
* DOCX
* TXT

Response:

{
"filename": "resume.pdf",
"candidate_name": "John Doe",
"email": "[john@example.com](mailto:john@example.com)",
"mobile": "+919999999999",
"skills": ["AWS","Docker","Linux"],
"job_matches": [...]
}

### Get All Resumes

GET /resumes

Returns all uploaded resumes.

### Get Resume By ID

GET /resume/{id}

Returns a specific resume record.

---

## Installation

Clone Repository

git clone https://github.com/yourusername/job-search-ai.git

cd job-search-ai

Create Virtual Environment

python3 -m venv venv

source venv/bin/activate

Install Dependencies

pip install -r requirements.txt

Run Application

uvicorn app:app --reload --host 0.0.0.0 --port 8000

Open Browser

http://localhost:8000/docs

---

## Sample Output

Extracted Candidate Details:

Name: SHREYASH SADANAND DESHPANDE

Email: [shreyash.deshpande.ssd@gmail.com](mailto:shreyash.deshpande.ssd@gmail.com)

Mobile: +918999245956

Skills:

AWS, Docker, Kubernetes, Jenkins, Git, Linux, Python, Prometheus, Grafana, MySQL, Oracle, Bash

Match Score:

100%

---

## Roadmap

Phase 1 ✅

* Resume Upload
* Resume Parsing
* Skill Extraction
* Job Matching
* SQLite Storage

Phase 2 🚀

* Docker Containerization
* AWS Deployment
* Nginx Reverse Proxy
* CI/CD Pipeline

Phase 3 🚀

* Terraform Infrastructure
* Prometheus Monitoring
* Grafana Dashboards
* CloudWatch Integration

---

## Author

Shreyash Sadanand Deshpande

DevOps Engineer | Linux | AWS | Terraform | Docker | Kubernetes
