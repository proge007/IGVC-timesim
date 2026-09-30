import argparse 
import csv 
from pathlib import Path

import numpy as np 


def nearestTimestamp(target, timestamps):
    return min(
        timestamps, 
        key=lambda timestamp: abs(timestamp - target)
    )


def loadData(dataDir, fileName):
    return np.load(
        dataDir / fileName, 
        allow_pickle=True
    ).item()


timesimParser = argparse.ArgumentParser()

timesimParser.add_argument(
    "--syncTIMESIMdata", required=True,
    help="timesim extracted"
)

args = timesimParser.parse_args()

timesimDATAdirectory = Path(args.syncTIMESIMdata)


cam0 = loadData(timesimDATAdirectory, "cam0.npy")
cam1 = loadData(timesimDATAdirectory, "cam1.npy")
lidar = loadData(timesimDATAdirectory, "lidar.npy")
imu = loadData(timesimDATAdirectory, "imu.npy")
joy = loadData(timesimDATAdirectory, "joy.npy")



outputFile = timesimDATAdirectory / "sync-data-timesim.csv"

firstCam0Time = min(cam0.keys())


with outputFile.open("w", newline="") as file:
    

    writer = csv.writer(file)
    
    writer.writerow([
        "timeSec",
        "cam0Timestamp",
        "cam0Path",
        "cam1Timestamp",
        "cam1Path",
        "lidarTimestamp",
        "lidarDt",
        "imuTimestamp",
        "imuDt",
        "joyTimestamp",
        "joyDt",
        "joyAxis0",
        "joyAxis1",
    ])



    for cam0Time in sorted(cam0.keys()):

        cam1Time = nearestTimestamp(cam0Time,cam1)   

        lidarTime = nearestTimestamp(cam0Time,lidar)

        imuTime = nearestTimestamp(cam0Time,imu)

        joyTime = nearestTimestamp(cam0Time,joy)


        relativeTime = cam0Time - firstCam0Time

        joyValue = joy[joyTime]


        writer.writerow([
            relativeTime,

            cam0Time,
            cam0[cam0Time],

            cam1Time,
            cam1[cam1Time],

            lidarTime,
            abs(cam0Time - lidarTime),

            imuTime,
            abs(cam0Time - imuTime),

            joyTime,
            abs(cam0Time - joyTime),
            joyValue[0],
            joyValue[1]
        ])


    print("synchronization complete")
    print("timeline:", outputFile)
    print("timesim frames:", len(cam0))