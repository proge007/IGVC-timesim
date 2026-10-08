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
    QWidget,
    QPushButton
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
        self.currentFrame = 0


        mainWidget = QWidget()
        mainLayout = QVBoxLayout()

        
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)


        message = QLabel(
            f"Replay\nFrames Loaded: {len(rows)}|"
        )

        mainLayout.addWidget(message)


    ##################### camera layout #################################

        cameraLayout = QHBoxLayout()

        self.camera0Label = QLabel("Camera 0:")
        self.camera0Label.setAlignment(Qt.AlignCenter)

        self.camera1Label = QLabel("Camera 1:")
        self.camera1Label.setAlignment(Qt.AlignCenter)

        cameraLayout.addWidget(self.camera0Label)
        cameraLayout.addWidget(self.camera1Label)


        mainLayout.addLayout(cameraLayout)



    ######################## Syned Data text ###############################

        self.infoLabel = QLabel()

        self.infoLabel.setAlignment(Qt.AlignCenter)
        
        mainLayout.addWidget(self.infoLabel)

       

        ######################## Buttonlayout ########################

        ButtonLayout = QHBoxLayout()

        self.previousButton = QPushButton("Previous")
        self.nextButton = QPushButton("Next")

        self.previousButton.clicked.connect(
            self.previousFrame
        )

        self.nextButton.clicked.connect(
            self.nextFrame
        )

        ButtonLayout.addWidget(
            self.previousButton
        )

        ButtonLayout.addWidget(
            self.nextButton
        )

        mainLayout.addLayout(
            ButtonLayout
        )

        

        ######################## window frame  ########################

        self.showFrame(0)
        
        self.resize(900,700)

    def showFrame(self, frameNumber):

        self.currentFrame = frameNumber
            
        row = rows[self.currentFrame]


        ######################## cam 0  ########################

        
        camera0Path = row["cam0Path"]

        pixmap0 = QPixmap(camera0Path)

        if pixmap0.isNull():
            self.camera0Label.setText("camera 0 error")

        else:
            pixmap = pixmap0.scaled(
                400,
                300,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            self.camera0Label.setPixmap(
                pixmap0
            )



        ######################## cam 1  ########################

        camera1Path = row["cam1Path"]
        
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
        
            self.camera1Label.setPixmap(
                pixmap1
            )


        ######################## synced data output  ########################

        infoText = (
            f"Frame: {self.currentFrame + 1} / {len(rows)}\n"
            f"Time: {float(row['timeSec']):.3f} seconds\n"
            f"LiDAR differene: {float(row['lidarDt']):.4f} seconds\n"
            f"IMU difference: {float(row['imuDt']):.4f} seconds\n"
            f"Joy difference: {float(row['joyDt']):.4f} seconds\n"
            f"Joy Axis 0: {row['joyAxis0']}\n"
            f"Joy Axis 1: {row['joyAxis1']}"
        )

        self.infoLabel.setText(
            infoText
        )


    ###################  previous and next button functions ####################  

    def previousFrame(self):

        if self.currentFrame > 0:

            self.showFrame(
                self.currentFrame - 1
            )


    def nextFrame(self):

        if self.currentFrame < len(rows) - 1:

            self.showFrame(
                self.currentFrame + 1
            )


    ################### timesim intialization ####################  

application = QApplication(sys.argv)
            
timesimWindow = WINDOW()
timesimWindow.show()
            
sys.exit(application.exec_())
