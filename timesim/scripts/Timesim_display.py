from PyQt5.QtCore import Qt 

from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QVBoxLayout, QWidget,
QPushButton, QSlider, QDialog, QTextEdit, QGroupBox)


def displayWindow(display, rows):

        display.mainWidget = QWidget()

        display.mainLayout = QVBoxLayout()

        display.mainWidget.setLayout(display.mainLayout)
    
        display.setCentralWidget(display.mainWidget)


######################### timesim window topsection ###################################

        topLayout = QHBoxLayout()

        frameLoadedLabel = QLabel(f"Replay\nFrames Loaded: {len(rows)}|")

        topLayout.addWidget(frameLoadedLabel)

        topLayout.addStretch()

        topLayout.addWidget(display.errorINFOmark)

        display.mainLayout.addLayout(topLayout)


##################################### camera layout #################################

        cameraLayout = QHBoxLayout()

        cameraZero = QGroupBox("Camera 0:")

        camera0Layout = QVBoxLayout()

        display.camera0Label = QLabel()

        display.camera0Label.setAlignment(Qt.AlignCenter)


        camera0Layout.addWidget(display.camera0Label)

        cameraZero.setLayout(camera0Layout)

        
        cameraOne = QGroupBox("Camera 1:")

        camera1Layout = QVBoxLayout()


        display.camera1Label = QLabel()

        display.camera1Label.setAlignment(Qt.AlignCenter)

        camera1Layout.addWidget(display.camera1Label)

        cameraOne.setLayout(camera1Layout)


        cameraLayout.addWidget(cameraZero)

        cameraLayout.addWidget(cameraOne)

        display.mainLayout.addLayout(cameraLayout)


########################## timesim video control #############################

        display.videoControl = QGroupBox("Video Controls:")

        display.videoControlLayout = QVBoxLayout()

        display.videoControlInfoLabel = QLabel()


        display.videoControlInfoLabel.setAlignment(Qt.AlignCenter)

        display.videoControlLayout.addWidget(display.videoControlInfoLabel)


        display.videoSlider = QSlider(Qt.Horizontal)
        
        display.videoSlider.setMinimum(0)
        
        display.videoSlider.setMaximum(len(rows) - 1)
        
        display.videoSlider.valueChanged.connect(display.showFrame)
        
        display.videoSlider.sliderPressed.connect(display.pausePlayback)
        
        display.videoControlLayout.addWidget(display.videoSlider)


        display.videoControlButtonLayout = QHBoxLayout()
        
        display.previousButton = QPushButton("Previous")
        
        display.playButton = QPushButton("Play")

        display.nextButton = QPushButton("Next")


        display.previousButton.clicked.connect(display.previousFrame)

        display.playButton.clicked.connect(display.playPause)

        display.nextButton.clicked.connect(display.nextFrame)


        display.videoControlButtonLayout.addStretch()

        display.videoControlButtonLayout.addWidget(display.previousButton)

        display.videoControlButtonLayout.addWidget(display.playButton)

        display.videoControlButtonLayout.addWidget(display.nextButton)


        display.videoControlButtonLayout.addStretch()

        display.videoControlLayout.addLayout(display.videoControlButtonLayout)

        display.videoControl.setLayout(display.videoControlLayout)
        

############################### Syned Data text ###############################
  
        display.syncData = QGroupBox("Sync Data:")

        display.syncDataLayout = QVBoxLayout()

        display.infoLabel = QLabel()

        display.infoLabel.setAlignment(Qt.AlignCenter)

        display.syncDataLayout.addWidget(display.infoLabel)

        display.syncData.setLayout(display.syncDataLayout)

        display.mainLayout.addWidget(display.syncData)        

        display.mainLayout.addWidget(display.videoControl)        


############################### Debugging Control ###############################

        display.debugControl = QGroupBox ("Debug Control: ")

        display.debugControlLayout = QHBoxLayout()

        display.errorButton = QPushButton("Error")

        display.previousERRORButton = QPushButton("Previous Error")

        display.nextERRORButton = QPushButton("Next Error")

        display.reportButton = QPushButton("Report")

        display.deleteButton = QPushButton("Delete")


        display.errorButton.clicked.connect(display.errorMark)

        display.previousERRORButton.clicked.connect(display.previousError)

        display.nextERRORButton.clicked.connect(display.nextError)

        display.reportButton.clicked.connect(display.viewReport)

        display.deleteButton.clicked.connect(display.deleteReport)


        display.debugControlLayout.addStretch()

        display.debugControlLayout.addWidget(display.errorButton)

        display.debugControlLayout.addWidget(display.previousERRORButton)

        display.debugControlLayout.addWidget(display.nextERRORButton)
        
        display.debugControlLayout.addWidget(display.reportButton)

        display.debugControlLayout.addWidget(display.deleteButton)
        

        display.debugControlLayout.addStretch()

        display.debugControl.setLayout(display.debugControlLayout)

        display.mainLayout.addWidget(display.debugControl)


        display.resize(1000,900)


def displayShowFrame(display, camera0Path, camera1Path):

        pixmap0 = QPixmap(camera0Path)
        
        if pixmap0.isNull():
                display.camera0Label.setText("camera 0 error")
        
        else:
                pixmap0 = pixmap0.scaled(400,300,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        
                display.camera0Label.setPixmap(pixmap0)
                
        pixmap1 = QPixmap(camera1Path)
                
        if pixmap1.isNull():    
                display.camera1Label.setText("camera 1 error")
                
        else:
                pixmap1 = pixmap1.scaled(400,300,Qt.KeepAspectRatio,Qt.SmoothTransformation)
                
                display.camera1Label.setPixmap(pixmap1)


def displayViewReport(display, reportData):
        
        display.reportWindow = QDialog(display, Qt.Window)
        
        display.reportWindow.setWindowTitle("Timesim Error Logs")
        
        display.reportWindow.resize(700,500)
        
        reportLayout = QVBoxLayout()
        
        display.reportText = QTextEdit()
        
        display.reportText.setReadOnly(True)
                
        display.reportText.setPlainText(reportData)

        reportLayout.addWidget(display.reportText)
        
        display.reportWindow.setLayout(reportLayout)
        
        display.reportWindow.show()