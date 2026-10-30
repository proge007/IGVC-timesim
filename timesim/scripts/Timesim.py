import argparse 
import sys
from pathlib import Path


from PyQt5.QtCore import Qt, QTimer 
from PyQt5.QtGui import QPixmap 
from Timesim_data import (loadTimesimData, keepErrorData, deleteErrorData, loadErrorReport, 
                          framePreviousError, frameNextError, dataShowFrame, dataScheduleNextFrame,
                          dataPreviousFrame, dataNextFrame, dataStartPlayback, dataPlayNextFrame, dataErrorMark)


from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QSlider,
    QDialog,
    QTextEdit,
    QGroupBox
)


timesimParser = argparse.ArgumentParser()

timesimParser.add_argument( "--syncTIMESIMdata", required=True, help="timesim sync data dict")

args = timesimParser.parse_args()

timesimDataDirectory = Path(args.syncTIMESIMdata)

(rows, syncFile, MarkedERRORfile, MarkedERRORframes) = loadTimesimData(timesimDataDirectory)

############################## moved code 

print("----Timesim replay data loaded----")
print("----sync file:", syncFile)
print("Frames loaded:", len(rows))




class WINDOW(QMainWindow):

    def __init__(self):
        super().__init__()

        self.errorINFOmark = QLabel(f"Marked Errors: {len(MarkedERRORframes)}")

        self.errorINFOmark.setAlignment(Qt.AlignCenter)


        self.setWindowTitle("TimeSim")
        
        self.currentFrame = 0


        self.isPlaying = False
        
        self.timer = QTimer(self)
        
        self.timer.setSingleShot(True)

        self.timer.timeout.connect(self.playNextFrame)


        mainWidget = QWidget()
        mainLayout = QVBoxLayout()

        
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)


######################### timesim window topsection ###################################


        topLayout = QHBoxLayout()

        frameLoadedLabel = QLabel(f"Replay\nFrames Loaded: {len(rows)}|")

        topLayout.addWidget(frameLoadedLabel)

        topLayout.addStretch()

        topLayout.addWidget(self.errorINFOmark)

        mainLayout.addLayout(topLayout)


##################################### camera layout #################################

        cameraLayout = QHBoxLayout()

        cameraZero = QGroupBox("Camera 0:")

        camera0Layout = QVBoxLayout()

        self.camera0Label = QLabel()

        self.camera0Label.setAlignment(Qt.AlignCenter)


        camera0Layout.addWidget(self.camera0Label)

        cameraZero.setLayout(camera0Layout)

        
        cameraOne = QGroupBox("Camera 1:")

        camera1Layout = QVBoxLayout()


        self.camera1Label = QLabel()

        self.camera1Label.setAlignment(Qt.AlignCenter)

        camera1Layout.addWidget(self.camera1Label)

        cameraOne.setLayout(camera1Layout)


        cameraLayout.addWidget(cameraZero)

        cameraLayout.addWidget(cameraOne)

        mainLayout.addLayout(cameraLayout)


########################## timesim video control #############################

        videoControl = QGroupBox("Video Controls:")

        videoControlLayout = QVBoxLayout()

        self.videoControlInfoLabel = QLabel()


        self.videoControlInfoLabel.setAlignment(Qt.AlignCenter)

        videoControlLayout.addWidget(self.videoControlInfoLabel)


        self.videoSlider = QSlider(Qt.Horizontal)
        
        self.videoSlider.setMinimum(0)
        
        self.videoSlider.setMaximum(len(rows) - 1)
        
        self.videoSlider.valueChanged.connect(self.showFrame)
        
        self.videoSlider.sliderPressed.connect(self.pausePlayback)
        
        videoControlLayout.addWidget(self.videoSlider)


        videoControlButtonLayout = QHBoxLayout()
        
        self.previousButton = QPushButton("Previous")
        
        self.playButton = QPushButton("Play")

        self.nextButton = QPushButton("Next")


        self.previousButton.clicked.connect(self.previousFrame)

        self.playButton.clicked.connect(self.playPause)

        self.nextButton.clicked.connect(self.nextFrame)


        videoControlButtonLayout.addStretch()

        videoControlButtonLayout.addWidget(self.previousButton)

        videoControlButtonLayout.addWidget(self.playButton)

        videoControlButtonLayout.addWidget(self.nextButton)


        videoControlButtonLayout.addStretch()

        videoControlLayout.addLayout(videoControlButtonLayout)

        videoControl.setLayout(videoControlLayout)


        mainLayout.addWidget(videoControl)


############################### Syned Data text ###############################
  
        syncData = QGroupBox("Sync Data:")

        syncDataLayout = QVBoxLayout()

        self.infoLabel = QLabel()

        self.infoLabel.setAlignment(Qt.AlignCenter)

        syncDataLayout.addWidget(self.infoLabel)

        syncData.setLayout(syncDataLayout)

        mainLayout.addWidget(syncData)


############################### Debugging Control ###############################

        debugControl = QGroupBox ("Debug Control: ")

        debugControlLayout = QHBoxLayout()

        self.errorButton = QPushButton("Error")

        self.previousERRORButton = QPushButton("Previous Error")

        self.nextERRORButton = QPushButton("Next Error")

        self.reportButton = QPushButton("Report")

        self.deleteButton = QPushButton("Delete")


        self.errorButton.clicked.connect(self.errorMark)

        self.previousERRORButton.clicked.connect(self.previousError)

        self.nextERRORButton.clicked.connect(self.nextError)

        self.reportButton.clicked.connect(self.viewReport)

        self.deleteButton.clicked.connect(self.deleteReport)
        

        debugControlLayout.addStretch()

        debugControlLayout.addWidget(self.errorButton)

        debugControlLayout.addWidget(self.previousERRORButton)

        debugControlLayout.addWidget(self.nextERRORButton)
        
        debugControlLayout.addWidget(self.reportButton)

        debugControlLayout.addWidget(self.deleteButton)
        

        debugControlLayout.addStretch()

        debugControl.setLayout(debugControlLayout)

        mainLayout.addWidget(debugControl)


        ######################## window frame  ########################

        self.showFrame(0)
        
        self.resize(1000,900)


    def showFrame(self, frameNUM):

        self.currentFrame = frameNUM

        self.videoSlider.blockSignals(True)

        self.videoSlider.setValue(self.currentFrame)

        self.videoSlider.blockSignals(False)

        (row, frameNum, totalFrames, videoControlInfoLabel, infoText, 
         camera0Path, camera1Path ) = dataShowFrame(rows, self.currentFrame)

        self.videoControlInfoLabel.setText(videoControlInfoLabel)

        self.infoLabel.setText(infoText)

        pixmap0 = QPixmap(camera0Path)

        if pixmap0.isNull():
            self.camera0Label.setText("camera 0 error")

        else:
            pixmap = pixmap0.scaled(400,300,Qt.KeepAspectRatio,Qt.SmoothTransformation)

            self.camera0Label.setPixmap(pixmap)

        camera1Path = row["cam1Path"]
        
        pixmap1 = QPixmap(camera1Path)
        
        if pixmap1.isNull():    
            self.camera1Label.setText("camera 1 error")
        
        else:
            pixmap1 = pixmap1.scaled(400,300,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        
            self.camera1Label.setPixmap(pixmap1)

    ###################  previous and next button functions ####################  


    def previousError(self):
        
        self.pausePlayback()

        errorFrame = framePreviousError(MarkedERRORframes,self.currentFrame)

        if errorFrame is None: 
            return

        self.showFrame(errorFrame)

        print("Moved to PREVIOUS error frame:", errorFrame + 1)


    def nextError(self):

        self.pausePlayback()

        errorFrame = frameNextError(MarkedERRORframes,self.currentFrame)

        if errorFrame is None: 
            return

        self.showFrame(errorFrame)

        print("Moved to NEXT error frame:", errorFrame + 1)


    def playPause(self):

        if self.isPlaying:
            self.pausePlayback()

        else:
            self.startPlayback()



    def startPlayback(self):

        startFrame = dataStartPlayback(rows, self.currentFrame)

        if startFrame != self.currentFrame:

            self.showFrame(startFrame)

        self.isPlaying = True

        self.playButton.setText("Pause")

        self.scheduleNextFrame()



    def pausePlayback(self):

        self.isPlaying = False

        self.timer.stop()

        self.playButton.setText("Play")


    def scheduleNextFrame(self):

        if not self.isPlaying:
            return

        if self.currentFrame >= len(rows) - 1:
            self.pausePlayback()
            return

        currentTime = float(rows[self.currentFrame]["timeSec"])   

        nextTime = float(rows[self.currentFrame + 1]["timeSec"])    

        delaySeconds = nextTime - currentTime


        frameDelay = max(1, int(delaySeconds * 1000))       

        self.timer.start(frameDelay)


    def playNextFrame(self):

        if not self.isPlaying:
            return

        nextFrame = dataPlayNextFrame(rows, self.currentFrame)

        self.showFrame(nextFrame)

        self.scheduleNextFrame()



    def previousFrame(self):

        self.pausePlayback()

        previousFrame = dataPreviousFrame(self.currentFrame)
        
        self.showFrame(previousFrame)


    def nextFrame(self):

        self.pausePlayback()

        nextFrame = dataNextFrame(rows, self.currentFrame)

        self.showFrame(nextFrame)

    ################### timesim error log format ####################  


    def viewReport(self):
                
        self.reportWindow = QDialog(self, Qt.Window)

        self.reportWindow.setWindowTitle("Timesim Error Logs")

        self.reportWindow.resize(700,500)

        reportLayout = QVBoxLayout()

        self.reportText = QTextEdit()

        self.reportText.setReadOnly(True)

        reportData = loadErrorReport(MarkedERRORfile)

        self.reportText.setPlainText(reportData)

        reportLayout.addWidget(self.reportText)

        self.reportWindow.setLayout(reportLayout)

        self.reportWindow.show()


    def deleteReport(self):
        
        deleteErrorData(MarkedERRORfile)

        MarkedERRORframes.clear()
        
        self.errorINFOmark.setText("Marked Errors: 0")

        if hasattr(self, "reportText"):

            self.reportText.setPlainText("no timesim error have been marked")

        print("timesim error log clears")


    def errorMark(self):

        self.pausePlayback()

        errorMarked = dataErrorMark(MarkedERRORfile, MarkedERRORframes, self.currentFrame, rows)

        if not errorMarked:
            
            print("TimeSim: error marked at frame:", self.currentFrame +1)

            return

        self.errorINFOmark.setText(f"marked errors: {len(MarkedERRORframes)}")

    ################### timesim intialization ####################  

application = QApplication(sys.argv)
            
timesimWindow = WINDOW()
timesimWindow.show()
            
sys.exit(application.exec_())
