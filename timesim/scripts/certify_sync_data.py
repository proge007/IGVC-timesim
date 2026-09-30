import argparse
import csv
from pathlib import Path


timesimParser = argparse.ArgumentParser()

timesimParser.add_argument(
    "--syncTIMESIMdata", required=True,
    help="timesim  sync data"
)

args = timesimParser.parse_args()

timesimDATAdirectory = Path(args.syncTIMESIMdata)

syncFile = timesimDATAdirectory / "sync-data-timesim.csv"


cam1Constrast = []
lidarConstrast = []
imuConstrast = []
joyConstrast = []



with syncFile.open("r") as file:

    reader = csv.DictReader(file)

    for row in reader:
        cam0Time = float(row["cam0Timestamp"])

        cam1Time = float(row["cam1Timestamp"])

        cam1Constrast.append(abs(cam0Time - cam1Time))

        lidarConstrast.append(float(row["lidarDt"]))

        imuConstrast.append(float(row["imuDt"]))

        joyConstrast.append(float(row["joyDt"]))



def showResults(name, differences):

    average = sum(differences) / len(differences)
    maxDif = max(differences)
    minDif = min(differences)

    print()
    print("--timstamp difference--")
    print(" ")
    print(name)
    print("average:", average, "seconds")
    print("max:", maxDif, "seconds")
    print("min:", minDif, "seconds")



print("timesim synchronization checked")
print("frames checked:", len(cam1Constrast))

showResults("cam 1", cam1Constrast)
showResults("lidar", lidarConstrast)
showResults("imu", imuConstrast)
showResults("joy stick control", joyConstrast)
