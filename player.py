import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QAbstractButton, QRadioButton, QButtonGroup, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QFont
from PyQt5.QtCore import pyqtSlot
import soundfile as sf
import sounddevice as sd
import numpy as np
import time
from os import listdir, getcwd, remove, system
from os.path import join, exists
import multiprocessing
from aubiolib import get_file_beats

folder = getcwd() + "/songs"
files = []
file_index = 0
beat_gaps=[]
isPlaying=False

def send_boom():
    global beat_gaps
    k=0
    #aa=np.average(beat_gaps)
    while(k<len(beat_gaps)):
        time.sleep(beat_gaps[k])
        k +=1
        print("Boom")

parallel_thread = multiprocessing.Process(name="Boom sender", target=send_boom)

def get_wav_files():
    global folder
    global files
    files = [f for f in listdir(folder) if f.endswith('.mp3')]

    for file in files:
        if exists(join(folder, file)[:-3] + "wav"):
            remove(join(folder, file)[:-3] + "wav")
        
        command = "ffmpeg -i " + join(folder, file) + " -vn -acodec pcm_s16le -ac 1 -ar 44100 -f wav " + join(folder, file)[:-3] + "wav"
        print(command)
        system(command)

        if exists(join(folder, file)):
            remove(join(folder, file))
    files = [join(folder, f) for f in listdir(folder) if f.endswith('.wav')]

def play_current():
    global isPlaying
    if isPlaying:
        return
    isPlaying = True

    global file_index
    global files
    global beat_gaps
    global parallel_thread

    if file_index < 0 or file_index >= len(files):
        return

    wav_file = files[file_index]
    wav, s = sf.read(wav_file)

    if appWindow.pace == 0:
        win_s = 4096
    else:
        win_s = 2048

    beat_gaps = get_file_beats(wav_file, 44100, win_s)
    #print(beat_gaps)
    print(('Playing ' + wav_file[wav_file.rfind('/')+1:]))
    appWindow.statusBar().showMessage('Playing ' + wav_file[wav_file.rfind('/')+1:])
    sd.play(wav, s)
    parallel_thread.start()
    
def stop_current():
    global isPlaying
    if not isPlaying:
        return
    isPlaying = False
    global parallel_thread
    sd.stop()
    parallel_thread.terminate()
    parallel_thread = multiprocessing.Process(name="Boom sender", target=send_boom)
    appWindow.statusBar().showMessage('Stopped.')

def go_next():
    global file_index
    global files

    file_index = file_index + 1
    file_index = file_index % len(files)

    stop_current()
    play_current()


class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()

class App(QMainWindow):
    pace=0

    def __init__(self):
        super().__init__()
        self.title = 'Music player'
        self.left = 900
        self.top = 430
        self.width = 450
        self.height = 100
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar().showMessage('Stopped.')
        nbutton = PicButton(QPixmap('/media/sayan/Data/Programmer/SongX/res/neic.png'), self)
        nbutton.move(50, 13)
        nbutton.resize(55,55)
        nbutton.setToolTip('Play next')
        nbutton.clicked.connect(self.next_on_click)
        pbutton = PicButton(QPixmap('/media/sayan/Data/Programmer/SongX/res/plic.png'), self)
        pbutton.move(135, 20)
        pbutton.resize(40,40)
        pbutton.setToolTip('Play song')
        pbutton.clicked.connect(self.play_on_click)
        sbutton = PicButton(QPixmap('/media/sayan/Data/Programmer/SongX/res/stic.png'), self)
        sbutton.move(200, 13)
        sbutton.resize(55,55)
        sbutton.setToolTip('Stop song')
        sbutton.clicked.connect(self.stop_on_click)
        rlabel = QLabel("pace", self)
        rlabel.move(350,15)
        myFont=QFont()
        myFont.setBold(True)
        rlabel.setFont(myFont)
        rb1 = QRadioButton("fast", self)
        rb1.move(300,35)
        rb1.toggled.connect(self.toggle_pace)
        rb2 = QRadioButton("slow", self)
        rb2.move(370, 35)
        rb2.setChecked(True)
        self.show()
 
    @pyqtSlot()
    def play_on_click(self):
        print('Start clicked')
        play_current()

    @pyqtSlot()
    def stop_on_click(self):
        print('Stop clicked')
        stop_current()

    @pyqtSlot()
    def next_on_click(self):
        print('Next Clicked')
        go_next()

    @pyqtSlot()
    def set_slow(self):
        print('Slow set')
        self.pace = 0

    @pyqtSlot()
    def toggle_pace(self):
        self.pace = (self.pace + 1) % 2
        if self.pace == 0:
            print('Slow set')
        else:
            print('Fast set')

if __name__ == '__main__':
    get_wav_files()
    print(files)
    app = QApplication(sys.argv)
    appWindow = App()
    sys.exit(app.exec_())