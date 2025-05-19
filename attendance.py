import csv
from datetime import datetime
import os

CSV_FILE = "attendance_record.csv"

def ensure_csv_exists():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Date", "Time"])

def mark_attendance(name):
    ensure_csv_exists()
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    with open(CSV_FILE, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == name and row[1] == date_str:
                return f"✅ Attendance already marked today for {name}"

    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, date_str, time_str])
    return f"📝 Attendance marked for {name} at {time_str}"
