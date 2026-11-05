import argparse 
import csv 
from pathlib import Path
from bisect import bisect_left

import numpy as np 



def nearestTimestamp(target, timestamps):

    index = bisect_left(timestamps, target)

    if index == 0:
        return timestamps[0]

    if index == len(timestamps):
        return timestamps[-1]
    
    before = timestamps[index - 1]

    after = timestamps[index]

    if abs(after - target) <  abs(target - before):
        return after
    return before 


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


cam0Times = sorted(cam0.keys())
cam1Times = sorted(cam1.keys())
lidarTimes = sorted(lidar.keys())
imuTimes = sorted(imu.keys())
joyTimes = sorted(joy.keys())


outputFile = timesimDATAdirectory / "sync-data-timesim.csv"

firstCam0Time = cam0Times[0]


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


    for cam0Time in cam0Times:

        cam1Time = nearestTimestamp(cam0Time,cam1Times)   

        lidarTime = nearestTimestamp(cam0Time,lidarTimes)

        imuTime = nearestTimestamp(cam0Time,imuTimes)

        joyTime = nearestTimestamp(cam0Time,joyTimes)

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