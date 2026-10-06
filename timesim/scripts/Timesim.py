import argparse 
import csv 
import sys
from pathlib import Path


from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget
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



print("----Timesim replay data loaded----")
print("----sync file:", syncFile)
print("Frames loaded:", len(rows))



class WINDOW(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("TimeSim")

        mainWidget = QWidget()
        mainLayout = QVBoxLayout()

        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)

        message = QLabel(
            f"Replay\nFrames Loaded: {len(rows)}|"
        )
        mainLayout.addWidget(message)

        self.camera0Label = QLabel("Camera 0:")
        self.camera0Label.setAlignment(Qt.AlignCenter)

        mainLayout.addWidget(self.camera0Label)



        camera0Path = rows[0]["cam0Path"]

        print("camera 0 image:", camera0Path)

        pixmap = QPixmap(camera0Path)

        if pixmap.isNull():

            self.camera0Label.setText(
                "camera 0 error"
            )

        else:

            pixmap = pixmap.scaled(
                700,
                450,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            self.camera0Label.setPixmap(pixmap)

            print("----cam0 loaded ------")
                        
        self.resize(800,600)
    
application = QApplication(sys.argv)
            
timesimWindow = WINDOW()
timesimWindow.show()
            
sys.exit(application.exec_())