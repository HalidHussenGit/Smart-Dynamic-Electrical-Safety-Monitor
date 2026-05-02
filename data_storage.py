"""CSV history storage for SDESM.

This module saves, loads, and clears analysis history using only the standard library.
"""

import csv
from datetime import datetime
from pathlib import Path


HISTORY_FILE = Path(__file__).with_name("sdesm_history.csv")
HEADER = [
    "Timestamp",
    "Temperature",
    "WindSpeed",
    "Humidity",
    "Weather",
    "Resistance",
    "Power",
    "SafeCurrent",
    "Status",
    "Alerts",
]


# Save one SDESM analysis record to the CSV history file.
# The parameters are the measured values and computed results for a single analysis run.
def save_record(temperature, wind_speed, humidity, weather, resistance, power, safe_current, status, alerts):
    file_exists = HISTORY_FILE.exists()
    alert_text = "; ".join(alerts) if isinstance(alerts, list) else str(alerts)

    with HISTORY_FILE.open("a", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        if not file_exists:
            writer.writerow(HEADER)

        writer.writerow(
            [
                datetime.now().isoformat(timespec="seconds"),
                temperature,
                wind_speed,
                humidity,
                weather,
                resistance,
                power,
                safe_current,
                status,
                alert_text,
            ]
        )


# Load the entire SDESM history file and return each row as a dictionary.
# No parameters are needed because the file is always stored beside this module.
def load_history():
    if not HISTORY_FILE.exists():
        return []

    with HISTORY_FILE.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)


# Clear all saved SDESM records while keeping the CSV header in place.
# No parameters are needed because the function always resets the same history file.
def clear_history():
    with HISTORY_FILE.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(HEADER)


if __name__ == "__main__":
    print("SDESM Data Storage Test")

    clear_history()
    save_record(28.5, 3.2, 55, "Clear", 12.4, 650.2, 8.98, "SAFE", ["All conditions normal"])
    save_record(66.1, 1.4, 88, "Humid", 13.8, 940.5, 8.52, "WARNING", ["High humidity detected", "Low wind speed detected"])

    history = load_history()
    print("Loaded history after saving two records:")
    for row in history:
        print(row)

    clear_history()
    print("History after clearing:")
    print(load_history())