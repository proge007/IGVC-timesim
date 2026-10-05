import argparse 
import csv 
from pathlib import Path

timesimParser = argparse.ArgumentParser()

timesimParser.add_argument(
    "--syncTIMESIMdata",
    required=True,
    help="timesim sync data dict"
)

args = timesimParser.parse_args()

timesimDataDirectory = Path(
    args.syncTIMESIMdata
)

syncFile = (
timesimDataDirectory / 
"sync-data-timesim.csv"
)

rows = []

with syncFile.open("r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        rows.append(row)

print("Timesim replay data loaded")
print("sync file:", syncFile)
print("Frames loaded:", len(rows))