from PyQt5.QtCore import Qt 

from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QVBoxLayout, QWidget, QPushButton, QSlider, QDialog, QTextEdit, QGroupBox)


def displayWindow(window, rows):

        window.mainWidget = QWidget()

        window.mainLayout = QVBoxLayout()

        window.mainWidget.setLayout(window.mainLayout)
    
        window.setCentralWidget(window.mainWidget)


######################### timesim window topsection ###################################

        topLayout = QHBoxLayout()

        frameLoadedLabel = QLabel(f"Replay\nFrames Loaded: {len(rows)}|")

        topLayout.addWidget(frameLoadedLabel)

        topLayout.addStretch()

        topLayout.addWidget(window.errorINFOmark)

        window.mainLayout.addLayout(topLayout)


##################################### camera layout #################################

        cameraLayout = QHBoxLayout()

        cameraZero = QGroupBox("Camera 0:")

        camera0Layout = QVBoxLayout()

        window.camera0Label = QLabel()

        window.camera0Label.setAlignment(Qt.AlignCenter)


        camera0Layout.addWidget(window.camera0Label)

        cameraZero.setLayout(camera0Layout)

        
        cameraOne = QGroupBox("Camera 1:")

        camera1Layout = QVBoxLayout()


        window.camera1Label = QLabel()

        window.camera1Label.setAlignment(Qt.AlignCenter)

        camera1Layout.addWidget(window.camera1Label)

        cameraOne.setLayout(camera1Layout)


        cameraLayout.addWidget(cameraZero)

        cameraLayout.addWidget(cameraOne)

        window.mainLayout.addLayout(cameraLayout)


########################## timesim video control #############################

        window.videoControl = QGroupBox("Video Controls:")

        window.videoControlLayout = QVBoxLayout()

        window.videoControlInfoLabel = QLabel()


        window.videoControlInfoLabel.setAlignment(Qt.AlignCenter)

        window.videoControlLayout.addWidget(window.videoControlInfoLabel)


        window.videoSlider = QSlider(Qt.Horizontal)
        
        window.videoSlider.setMinimum(0)
        
        window.videoSlider.setMaximum(len(rows) - 1)
        
        window.videoSlider.valueChanged.connect(window.showFrame)
        
        window.videoSlider.sliderPressed.connect(window.pausePlayback)
        
        window.videoControlLayout.addWidget(window.videoSlider)


        window.videoControlButtonLayout = QHBoxLayout()
        
        window.previousButton = QPushButton("Previous")
        
        window.playButton = QPushButton("Play")

        window.nextButton = QPushButton("Next")


        window.previousButton.clicked.connect(window.previousFrame)

        window.playButton.clicked.connect(window.playPause)

        window.nextButton.clicked.connect(window.nextFrame)


        window.videoControlButtonLayout.addStretch()

        window.videoControlButtonLayout.addWidget(window.previousButton)

        window.videoControlButtonLayout.addWidget(window.playButton)

        window.videoControlButtonLayout.addWidget(window.nextButton)


        window.videoControlButtonLayout.addStretch()

        window.videoControlLayout.addLayout(window.videoControlButtonLayout)

        window.videoControl.setLayout(window.videoControlLayout)

     

############################### Syned Data text ###############################
  
        window.syncData = QGroupBox("Sync Data:")

        window.syncDataLayout = QVBoxLayout()

        window.infoLabel = QLabel()

        window.infoLabel.setAlignment(Qt.AlignCenter)

        window.syncDataLayout.addWidget(window.infoLabel)

        window.syncData.setLayout(window.syncDataLayout)

        window.mainLayout.addWidget(window.syncData)        

        window.mainLayout.addWidget(window.videoControl)        


############################### Debugging Control ###############################

        window.debugControl = QGroupBox ("Debug Control: ")

        window.debugControlLayout = QHBoxLayout()

        window.errorButton = QPushButton("Error")

        window.previousERRORButton = QPushButton("Previous Error")

        window.nextERRORButton = QPushButton("Next Error")

        window.reportButton = QPushButton("Report")

        window.deleteButton = QPushButton("Delete")


        window.errorButton.clicked.connect(window.errorMark)

        window.previousERRORButton.clicked.connect(window.previousError)

        window.nextERRORButton.clicked.connect(window.nextError)

        window.reportButton.clicked.connect(window.viewReport)

        window.deleteButton.clicked.connect(window.deleteReport)


        window.debugControlLayout.addStretch()

        window.debugControlLayout.addWidget(window.errorButton)

        window.debugControlLayout.addWidget(window.previousERRORButton)

        window.debugControlLayout.addWidget(window.nextERRORButton)
        
        window.debugControlLayout.addWidget(window.reportButton)

        window.debugControlLayout.addWidget(window.deleteButton)
        

        window.debugControlLayout.addStretch()

        window.debugControl.setLayout(window.debugControlLayout)

        window.mainLayout.addWidget(window.debugControl)


        window.resize(1000,900)
