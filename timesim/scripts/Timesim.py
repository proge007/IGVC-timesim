import argparse 
import csv 
import sys
from pathlib import Path


from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
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


        cameraLayout = QHBoxLayout()

        self.camera0Label = QLabel("Camera 0:")
        self.camera0Label.setAlignment(Qt.AlignCenter)

        self.camera1Label = QLabel("Camera 1:")
        self.camera1Label.setAlignment(Qt.AlignCenter)

        cameraLayout.addWidget(self.camera0Label)
        cameraLayout.addWidget(self.camera1Label)


        mainLayout.addLayout(cameraLayout)

        self.resize(900,600)

        row = rows[0]

        self.infoLabel = QLabel()

        self.infoLabel.setAlignment(
            Qt.AlignCenter
        )

        infoText = (
            f"Frame: 1 / {len(rows)}\n"
            f"Time: {float(row['timeSec']):.3f} seconds\n"
            f"LiDAR differene: {float(row['lidarDt']):.4f} seconds\n"
            f"IMU difference: {float(row['imuDt']):.4f} seconds\n"
            f"Joy difference: {float(row['joyDt']):.4f} seconds\n"
            f"Joy Axis 0: {row['joyAxis0']}\n"
            f"Joy Axis 1: {row['joyAxis1']}"
        )

        self.infoLabel.setText(infoText)
        
        mainLayout.addWidget(
            self.infoLabel
        )
        
        self.resize(900,700)

        
        camera0Path = rows[0]["cam0Path"]

        print("camera 0 image:", camera0Path)
        
        pixmap = QPixmap(camera0Path)

        if pixmap.isNull():
            self.camera0Label.setText(
                "camera 0 error"
            )

        else:
            pixmap = pixmap.scaled(
                400,
                300,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            self.camera0Label.setPixmap(pixmap)
        
        print("----cam0 loaded ------")


        
        camera1Path = rows[0]["cam1Path"]

        print("camera 1 image:", camera1Path)
        pixmap1 = QPixmap(camera1Path)

        if pixmap1.isNull():
            self.camera1Label.setText(
                "camera 1 error"
            )

        else:
            pixmap1 = pixmap1.scaled(
                400,
                300,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            self.camera1Label.setPixmap(pixmap1)
        
        print("----cam1 loaded ------")

         
        self.resize(900,600)
    
application = QApplication(sys.argv)
            
timesimWindow = WINDOW()
timesimWindow.show()
            
sys.exit(application.exec_())