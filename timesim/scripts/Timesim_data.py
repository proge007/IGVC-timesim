import csv
from pathlib import Path 



def loadTimesimData(timesimDataDirectory):


    syncFile = (timesimDataDirectory / "sync-data-timesim.csv")

    MarkedERRORfile = (timesimDataDirectory / "markedIGVerror.txt")


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


