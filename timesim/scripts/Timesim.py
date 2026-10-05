import argparse 
import csv 
import sys
from pathlib import Path


from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow
)


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



class WINDOW(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("TimeSim")

        message = QLabel(
            f"Replay \nFrames loaded: {len(rows)}"
        ) 

        self.setCentralWidget(message)

        self.resize(800, 800)

application = QApplication(sys.argv)

WINDOW = WINDOW()
WINDOW.show()

sys.exit(application.exec_())