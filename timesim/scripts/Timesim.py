import sys

from PyQt5.QtCore import (Qt, QTimer) 

from Timesim_data import (loadTimesimData, loadErrorReport, 
framePreviousError, frameNextError, dataShowFrame, dataScheduleNextFrame,
dataPreviousFrame, dataNextFrame, dataStartPlayback, dataPlayNextFrame, 
dataErrorMark, dataDeleteReport, dataTimesimDirectory)

from Timesim_display import (displayWindow, displayShowFrame, displayViewReport)

from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow)

timesimDataDirectory = dataTimesimDirectory()

(rows, syncFile, MarkedERRORfile, MarkedERRORframes) = loadTimesimData(timesimDataDirectory)

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

        displayWindow(self, rows)


        ######################## window frame  ########################

        self.showFrame(0)

    def showFrame(self, frameNUM):

        self.currentFrame = frameNUM

        self.videoSlider.blockSignals(True)

        self.videoSlider.setValue(self.currentFrame)

        self.videoSlider.blockSignals(False)

        (videoControlInfoLabel, infoText, camera0Path, camera1Path ) = dataShowFrame(rows, self.currentFrame)

        self.videoControlInfoLabel.setText(videoControlInfoLabel)

        self.infoLabel.setText(infoText)

        displayShowFrame(self,camera0Path,camera1Path)


    ###################  previous and next button functions ####################  

    def previousError(self):
        
        self.pausePlayback()

        errorFrame = framePreviousError(MarkedERRORframes,self.currentFrame)

        if errorFrame is None: 
            return

        self.showFrame(errorFrame)


    def nextError(self):

        self.pausePlayback()

        errorFrame = frameNextError(MarkedERRORframes,self.currentFrame)

        if errorFrame is None: 
            return

        self.showFrame(errorFrame)


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

        frameDelay = dataScheduleNextFrame(rows, self.currentFrame)       

        if frameDelay is None:
            self.pausePlayback()
            return

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


####################### timesim error log format ####################  

    def viewReport(self):

        reportData = loadErrorReport(MarkedERRORfile)

        displayViewReport(self,reportData)
                

    def deleteReport(self):
        
        markedErrorCount = dataDeleteReport(MarkedERRORfile, MarkedERRORframes)

        self.errorINFOmark.setText(f"Marked Errors: {markedErrorCount}")

        if hasattr(self, "reportText"):

          self.reportText.setPlainText("no timesim error have been marked")


    def errorMark(self):

        self.pausePlayback()

        errorMarked = dataErrorMark(MarkedERRORfile, MarkedERRORframes, self.currentFrame, rows)

        if not errorMarked:
            return
        
        self.errorINFOmark.setText(f"Marked Errors: {len(MarkedERRORframes)}")

            
##################### timesim intialization ####################  
                
application = QApplication(sys.argv)
            
timesimWindow = WINDOW()

timesimWindow.show()
            
sys.exit(application.exec_())
