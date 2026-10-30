import csv
import argparse

from pathlib import Path 


def dataTimesimDirectory():
     
    timesimParser = argparse.ArgumentParser()

    timesimParser.add_argument( "--syncTIMESIMdata", required=True, help="timesim sync data dict")

    args = timesimParser.parse_args()

    timesimDATADirectory = Path(args.syncTIMESIMdata)

    return timesimDATADirectory


def loadTimesimData(timesimDATADirectory):

    syncFile = (timesimDATADirectory / "sync-data-timesim.csv")

    MarkedERRORfile = (timesimDATADirectory / "markedIGVerror.txt")

    if not syncFile.exists():

        raise FileNotFoundError(f"ERROR: TimeSim sync file not found: {syncFile}")

    rows = []

    with syncFile.open("r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            rows.append(row)

    if len(rows) ==0:

        raise RuntimeError("ERROR: timesim sync file contains no frames")

    MarkedERRORframes = []

    if MarkedERRORfile.exists():

        with MarkedERRORfile.open("r") as file:

            for line in file:

                if line.startswith("Frame:"):

                    frameNUM = int(line.split(":")[1].strip())

                    MarkedERRORframes.append(frameNUM - 1)

    return (rows, syncFile, MarkedERRORfile, MarkedERRORframes) 


def keepErrorData(MarkedERRORfile,frameNumber,row):
            
    with MarkedERRORfile.open("a") as file:

        file.write("----- TimeSim Error Information ----- \n")

        file.write(f"Frame: {frameNumber}\n")

        file.write(f"timeSec: {row['timeSec']}\n")

        file.write(f"cam0Timestamp: {row['cam0Timestamp']}\n")

        file.write(f"cam1Timestamp: {row['cam1Timestamp']}\n")

        file.write(f"lidarTimestamp: {row['lidarTimestamp']}\n")

        file.write(f"imuTimestamp: {row['imuTimestamp']}\n")

        file.write(f"joyTimestamp: {row['joyTimestamp']}\n")

        file.write(f"joyAxis0: {row['joyAxis0']}\n")

        file.write(f"joyAxis1: {row['joyAxis1']}\n")

        file.write("\n")


def deleteErrorData(MarkedERRORfile):
        
    with MarkedERRORfile.open("w") as file:

        file.write("")


def loadErrorReport(MarkedERRORfile):

    if MarkedERRORfile.exists():

        with MarkedERRORfile.open("r") as file:

            return file.read()

    return "No timesim errors been marked"


def framePreviousError(MarkedERRORframes,currentFrame):
        
    previousErrors = []

    for frame in MarkedERRORframes:

            if frame < currentFrame:
                
                previousErrors.append(frame)

    if len(previousErrors) == 0:
            
            return None
    
    return max(previousErrors)


def frameNextError(MarkedERRORframes,currentFrame):

    nextErrors = []

    for frame in MarkedERRORframes:

        if frame > currentFrame:

            nextErrors.append(frame)

    if len(nextErrors) == 0:

            return None

    return min(nextErrors)


def dataShowFrame(rows, currentFrame):

    row = rows[currentFrame]

    frameNum = currentFrame + 1

    totalFrames = len(rows)
    
    videoControlInfoLabel = (f"Frame: {frameNum} / {totalFrames}"
        f"    |    "
        f"Time: {float(row['timeSec']):.3f} seconds")

    infoText = (
        f"Frame: {frameNum} / {totalFrames}\n"
        f"Time: {float(row['timeSec']):.3f} seconds\n"
        f"LiDAR difference: {float(row['lidarDt']):.4f} seconds\n"
        f"IMU difference: {float(row['imuDt']):.4f} seconds\n"
        f"Joy difference: {float(row['joyDt']):.4f} seconds\n"
        f"Joy Axis 0: {row['joyAxis0']}\n"
        f"Joy Axis 1: {row['joyAxis1']}"
    )

    camera0Path = row["cam0Path"]
    camera1Path = row["cam1Path"]
    return (videoControlInfoLabel, infoText, camera0Path, camera1Path)


def dataScheduleNextFrame(rows, currentFrame):

    if currentFrame >= len(rows) - 1:
        return None

    currentTime = float(rows[currentFrame]["timeSec"])   

    nextTime = float(rows[currentFrame + 1]["timeSec"])    

    delaySeconds = nextTime - currentTime

    frameDelay = max(1, int(delaySeconds * 1000))       
    return frameDelay


def dataPreviousFrame(currentFrame):

    if currentFrame > 0:

        currentFrame = currentFrame - 1

    return currentFrame


def dataNextFrame(rows, currentFrame):

    if currentFrame < len(rows) - 1:

        currentFrame = currentFrame + 1

    return currentFrame


def dataStartPlayback(rows, currentFrame):

    if currentFrame >= len(rows) - 1:

        currentFrame = 0

    return currentFrame


def dataPlayNextFrame(rows, currentFrame):

    if currentFrame < len(rows) - 1:

        currentFrame = currentFrame + 1

    return currentFrame


def dataErrorMark(MarkedERRORfile, MarkedERRORframes, currentFrame, rows ):

        if currentFrame in MarkedERRORframes:

            return False

        row = rows[currentFrame]

        keepErrorData(MarkedERRORfile, currentFrame + 1, row)

        MarkedERRORframes.append(currentFrame)

        return True


def dataDeleteReport(MarkedERRORfile, MarkedERRORframes):
        
        deleteErrorData(MarkedERRORfile)

        MarkedERRORframes.clear()

        return len(MarkedERRORframes)