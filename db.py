import sqlite3
import logging

DATABASE = "database.db"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_connection():
    """
    Returns SQLite connection.
    """

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


def initialize_database():
    """
    Creates resumes table if it doesn't exist.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS resumes
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            filename TEXT NOT NULL,

            candidate_name TEXT,

            email TEXT,

            mobile TEXT,

            skills TEXT,

            match_score INTEGER,

            upload_time DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()

    conn.close()

    logging.info("Database initialized successfully.")
