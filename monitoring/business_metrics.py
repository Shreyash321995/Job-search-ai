from prometheus_client import Counter, Histogram
import time

# Business Metrics

resume_upload_counter = Counter(
    "resume_upload_total",
    "Total resumes uploaded"
)

duplicate_resume_counter = Counter(
    "duplicate_resume_total",
    "Total duplicate resumes"
)

upload_duration = Histogram(
    "resume_upload_duration_seconds",
    "Resume upload duration"
)


def start_timer():
    return time.time()


def stop_timer(start):
    upload_duration.observe(time.time() - start)

from prometheus_client import Gauge

current_resume_count = Gauge(
    "current_resume_count",
    "Current number of resumes stored in database"
)

import db

#def update_current_resume_count():
 #   conn = db.get_connection()
  #  cursor = conn.cursor()

   # cursor.execute("SELECT COUNT(*) FROM resumes")

    #count = cursor.fetchone()[0]

    #current_resume_count.set(count)

    #conn.close()
def update_current_resume_count():
    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM resumes")

    count = cursor.fetchone()[0]

    print("Resume Count =", count)

    current_resume_count.set(count)

    print("Gauge Updated")

    conn.close()
