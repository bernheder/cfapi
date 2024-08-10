import json
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from .config import DATABASE


@dataclass
class CalibrationFile:
    file_name: str
    modified_at: datetime
    data: dict


@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE)
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS calibration_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            modified_at TIMESTAMP,
            data JSON
            )
        """)
        conn.commit()

def store_file(calibration_file: CalibrationFile):
    data = json.dumps(calibration_file.data)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO calibration_files (file_name, modified_at, data)
        VALUES (?, ?, ?)
        ''', (calibration_file.file_name, calibration_file.modified_at.isoformat(), data))
        conn.commit()


def get_files(show_field: str = None):
    with get_db() as conn:
        cursor = conn.cursor()
        if show_field:
            cursor.execute(f'''
            SELECT file_name, modified_at, json_extract(data, '$.{show_field}') as {show_field}
            FROM calibration_files
            ''')
        else:
            cursor.execute('''
            SELECT file_name, modified_at
            FROM calibration_files
            ''')
        files = cursor.fetchall()
    return files


def get_file(filename):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT file_name, modified_at, data
        FROM calibration_files
        WHERE file_name = ?
        ''', (filename,))
        file = cursor.fetchone()
    return file
