import os
import csv
from datetime import datetime
from multiprocessing import Pool
import sqlite3

# Database configuration (Chnange this values to configure the database)
DB_NAME = 'sensor_data.db'
TABLE_NAME = 'sensor_data'

# Target directory path (Change this value to configure the target directory)
TARGET_DIR = 'target-directory'

# Create the database and table if they don't exist
def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, sensor_name TEXT, value REAL)")

    conn.commit()
    conn.close()


# Function to process a single file
def process_file(file):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        headers = next(reader)  # Read the header row

        for row in reader:
            try:
                timestamp = datetime.fromisoformat(row[0])
                sensor_name = row[1]
                value = float(row[2])

                # Check if the record already exists
                cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE timestamp = ? AND sensor_name = ? AND value = ?",
                               (timestamp, sensor_name, value))
                count = cursor.fetchone()[0]

                if count == 0:
                    # Insert the record into the database
                    cursor.execute(f"INSERT INTO {TABLE_NAME} (timestamp, sensor_name, value) VALUES (?, ?, ?)",
                                   (timestamp, sensor_name, value))
                else:
                    # Handle duplicate record
                    print(f"Duplicate record found: {row}")

            except (IndexError, ValueError):
                # Ignore invalid records
                continue

    conn.commit()
    conn.close()

# Function to process files in parallel
def process_files_parallel():
    file_list = [os.path.join(TARGET_DIR, f) for f in os.listdir(TARGET_DIR) if f.endswith('.csv')]

    with Pool() as pool:
        pool.map(process_file, file_list)



# Entry point of the program
if __name__ == '__main__':
    create_database()
    process_files_parallel()