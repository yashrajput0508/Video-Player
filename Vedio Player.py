# Vedio player using pyqt
# Made by Yash Rajput  Date : 21-05-2020,Time : 01:55
import os
import sys
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from demovedio import *
class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Video Player")
        self.setWindowIcon(QIcon(r"C:\Users\Yash\PycharmProjects\ppppp\App-Media-icon.png"))
        self.ui.files.setCheckable(True)
        self.setMinimumSize(500,500)
        status=QStatusBar(self)
        status.setStyleSheet("background-color: rgb(177, 177, 177);")
        self.setStatusBar(status)
        self.player=QMediaPlayer()
        self.player.play()
        self.player.error.connect(self.erroralert)

        self.playlist = QMediaPlaylist()
        self.ui.play.clicked.connect(self.plays)
        self.current=False
        self.player.setPlaylist(self.playlist)
        self.player.setVolume(30)
        self.ui.horizontalSlider_2.setValue(30)
        self.videoWidget = QVideoWidget(self)
        self.videoWidget.setGeometry(10,300,141,111)
        self.videoWidget.setStyleSheet("background-color: rgb(0,0,0);")
        self.player.setVideoOutput(self.videoWidget)

        style="""QSlider::groove:horizontal {
        border: 1px solid #bbb;
        background: black;
        height: 10px;
        border-radius: 4px;
        }
        
        QSlider::sub-page:horizontal {
        background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,
            stop: 0 #66e, stop: 1 #bbf);
        background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
            stop: 0 #bbf, stop: 1 #55f);
        border: 1px solid #777;
        height: 10px;
        border-radius: 4px;
        }
        
        QSlider::add-page:horizontal {
        background: #fff;
        border: 1px solid #777;
        height: 10px;
        border-radius: 4px;
        }
        
        QSlider::handle:horizontal {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #eee, stop:1 #ccc);
        border: 1px solid #777;
        width: 13px;
        margin-top: -2px;
        margin-bottom: -2px;
        border-radius: 4px;
        }
        
        QSlider::handle:horizontal:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #000, stop:1 #ddd);
        border: 1px solid #444;
        border-radius: 4px;
        }
        
        QSlider::sub-page:horizontal:disabled {
        background: #bbb;
        border-color: #999;
        }
        
        QSlider::add-page:horizontal:disabled {
        background: #eee;
        border-color: #999;
        }
        
        QSlider::handle:horizontal:disabled {
        background: #eee;
        border: 1px solid #aaa;
        border-radius: 4px;
        }"""
        self.ui.horizontalSlider_3.setMinimum(0)
        self.ui.horizontalSlider_3.setMaximum(2)
        self.ui.horizontalSlider_3.setValue(1)
        self.player.setPlaybackRate(1)
        self.ui.horizontalSlider_3.valueChanged.connect(self.volume)
        self.ui.horizontalSlider.setStyleSheet(style)
        self.ui.horizontalSlider.setPageStep(5)
        self.ui.horizontalSlider.setSingleStep(5)
        self.ui.play.setToolTip("Play")
        self.ui.horizontalSlider_2.valueChanged.connect(self.voice)
        self.ui.next.pressed.connect(self.playlist.next)
        self.ui.prev.pressed.connect(self.playlist.previous)
        self.ui.reset.pressed.connect(self.stop)
        self.working=False
        self.ui.files.pressed.connect(self.check)
        self.ui.sound.pressed.connect(self.voice1)
        self.ui.actionIncrease_Sound.triggered.connect(self.voice2)
        self.ui.actionDecrease_Sound.triggered.connect(self.voice3)
        self.ui.actionSilent_Sound.triggered.connect(self.silent)
        self.ui.actionLight_Background.setCheckable(True)
        self.ui.actionDark_Background.setCheckable(True)
        self.ui.actionLight_Background.setChecked(True)
        self.ui.actionLight_Background.toggled.connect(self.background2)
        self.ui.actionDark_Background.toggled.connect(self.background1)
        self.ui.actionOpen_Folder.triggered.connect(self.open_folder)
        self.ui.actionhelp.triggered.connect(self.help)
        self.ui.actionabout.triggered.connect(self.about)
        #self.ui.files.toggled.connect(self.toggle_viewer)
        self.ui.listView.doubleClicked.connect(self.plays)
        self.ui.listView.setWindowIcon(QIcon(r"C:\Users\Yash\PycharmProjects\ppppp\App-Media-icon.png"))
        self.ui.comboBox.currentTextChanged.connect(self.change)
        self.ui.lineEdit.textEdited.connect(self.text_folder)
        #self.viewer.state.connect(self.ui.files.setChecked)
        self.ui.horizontalSlider.setFocusPolicy(Qt.StrongFocus)
        self.ui.horizontalSlider.setSingleStep(2)
        self.ui.horizontalSlider.setPageStep(2)

        play=QAction(self)
        play.setShortcut("Space")
        play.triggered.connect(self.plays)
        self.addAction(play)
        self.player.durationChanged.connect(self.update_duration)
        self.player.positionChanged.connect(self.update_position)
        self.list=[]

        self.timer=QTimer(self)
        self.timer.timeout.connect(self.time)
        self.timer.start(1000)
        self.model = PlaylistModel(self.playlist)
        self.ui.listView.setModel(self.model)
        self.playlist.currentIndexChanged.connect(self.playlist_position_changed)
        selection_model = self.ui.listView.selectionModel()
        selection_model.selectionChanged.connect(self.playlist_selection_changed)
        try:
            path=sys.argv[1]
            self.playlist.addMedia(
                QMediaContent(QUrl.fromLocalFile(path))
            )
            self.model.layoutChanged.emit()
            # If not playing, seeking to first of newly added + play.
            self.list.append(path)
            self.plays()
        except:
            pass
        right_arrow=QAction(self)
        right_arrow.setShortcut("Right")
        self.addAction(right_arrow)
        right_arrow.triggered.connect(self.forward)
        super_right=QAction(self)
        super_right.setShortcut("Ctrl+Right")
        self.addAction(super_right)
        super_right.triggered.connect(self.forwards)
        left_arrow=QAction(self)
        left_arrow.setShortcut("Left")
        self.addAction(left_arrow)
        left_arrow.triggered.connect(self.backward)
        super_left=QAction(self)
        super_left.setShortcut("Ctrl+Left")
        self.addAction(super_left)
        super_left.triggered.connect(self.backwards)

        self.ui.actionOpen_File.triggered.connect(self.open_file)
        self.setAcceptDrops(True)
        self.show()

    def help(self):
        QMessageBox.information(self, "Help", "This is your video player using Python")

    def about(self):
        QMessageBox.information(self, "About", "This is the video player made by Yash Rajput")
    def backwards(self):
        temp=self.player.position()-60000
        if temp>0:
            self.player.setPosition(temp)
            self.update_position(temp)
        else:
            temp=0
            self.player.setPosition(temp)
            self.update_position(temp)
    def forwards(self):
        temp=self.player.position()+60000
        if temp<self.player.duration():
            self.player.setPosition(temp)
            self.update_position(temp)
        else:
            self.playlist.next()
    def backward(self):
        temp=self.player.position()-30000
        if temp>0:
            self.player.setPosition(temp)
            self.update_position(temp)
        else:
            temp=0
            self.player.setPosition(temp)
            self.update_position(temp)
    def forward(self):
        temp=self.player.position()+30000
        if temp<self.player.duration():
            self.player.setPosition(temp)
            self.update_position(temp)
        else:
            self.playlist.next()
    def dropEvent(self, e):
        for url in e.mimeData().urls():
            self.playlist.addMedia(
                QMediaContent(url)
            )

        self.model.layoutChanged.emit()
        # If not playing, seeking to first of newly added + play.
        if self.player.state() != QMediaPlayer.PlayingState:
            i = self.playlist.mediaCount() - len(e.mimeData().urls())
            self.playlist.setCurrentIndex(i)
            self.player.play()
    def dragEnterEvent(self, e):
        for url in e.mimeData().urls():
            self.playlist.addMedia(
                QMediaContent(url)
            )

        self.model.layoutChanged.emit()
        # If not playing, seeking to first of newly added + play.
        if self.player.state() != QMediaPlayer.PlayingState:
            i = self.playlist.mediaCount() - len(e.mimeData().urls())
            self.playlist.setCurrentIndex(i)
            self.player.play()
    def volume(self):
        self.player.setPlaybackRate(self.ui.horizontalSlider_3.value())
    def time(self):
        time = QTime.currentTime()
        text = time.toString("hh:mm:ss")
        self.ui.lcdNumber.setNumDigits(8)
        self.ui.lcdNumber.display(text)
        self.ui.lcdNumber.setFrameShadow(QFrame.Sunken)
        self.ui.lcdNumber.setFrameShape(QFrame.Panel)
    def check(self):
        if self.working==False:
            self.ui.widget.hide()
            self.videoWidget.setGeometry(0,21,self.ui.widget.geometry().width(),self.ui.widget.geometry().height())
            self.working=True
        else:
            self.videoWidget.setGeometry(0,self.ui.widget.height()-90,151,111)
            self.working=False
            self.ui.widget.show()
    def resizeEvent(self, event):
        self.ui.widget.setGeometry(self.geometry().x()-self.geometry().getCoords()[0],self.geometry().y()-self.geometry().getCoords()[1],self.geometry().width(),self.geometry().height()-161)
        self.ui.listView.setGeometry(150,0,self.ui.widget.geometry().width()-152,self.ui.widget.height())
        self.ui.widget_2.setGeometry(0,self.ui.widget.geometry().height()+9,self.geometry().width(),30)
        self.ui.horizontalSlider.setGeometry(50,0,self.ui.widget_2.width()-102,self.ui.widget_2.height())
        self.ui.label_2.setGeometry(49+self.ui.horizontalSlider.geometry().width(),0,51,31)
        self.ui.widget_3.setGeometry(0,self.ui.widget_2.geometry().y()+40,self.geometry().width(),30)
        self.ui.sound.setGeometry(self.ui.widget_3.geometry().width()-153,0,28,24)
        self.ui.horizontalSlider_2.setGeometry(self.ui.widget_3.geometry().width()-113,0,108,31)
        self.ui.widget_4.setGeometry(0,self.ui.widget_3.geometry().y()+40,self.geometry().width(),30)
        self.ui.label_5.setGeometry(0,0,self.ui.widget_4.geometry().width()-102,21)
        self.ui.label_14.setGeometry(self.ui.widget_4.geometry().width()-91,0,91,21)
        if self.working==False:
            self.videoWidget.setGeometry(0,self.ui.widget.height()-90,151,111)
        else:
            self.videoWidget.setGeometry(0, 21, self.ui.widget.geometry().width(), self.ui.widget.geometry().height())
    def text_folder(self):
        temp=self.list
        self.playlist.clear()
        if self.ui.lineEdit.text()!='':
            for i in temp:
                import re
                if re.search(self.ui.lineEdit.text(),i):
                    self.playlist.addMedia(
                        QMediaContent(
                            QUrl.fromLocalFile(i)
                        )
                    )
        else:
            for i in temp:
                self.playlist.addMedia(
                        QMediaContent(
                            QUrl.fromLocalFile(i)
                        )
                    )
        self.model.layoutChanged.emit()
    def change(self):
        if self.ui.comboBox.currentText()=="View Mode":
            self.ui.listView.setViewMode(QListView.IconMode)
        else:
            self.ui.listView.setViewMode(QListView.ListMode)
    def stop(self):
        self.player.stop()
        self.ui.play.setIcon(QIcon(r'C:\Users\Yash\PycharmProjects\ppppp\images\Pause-icon.png'))
        self.current = True
    def background1(self):
        if self.ui.actionDark_Background.isChecked()==True:
            self.ui.actionLight_Background.setChecked(False)
            app.setApplicationName("Failamp")
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            app.setPalette(palette)
    def background2(self):
        if self.ui.actionLight_Background.isChecked()==True:
            self.ui.actionDark_Background.setChecked(False)
            palette = QPalette()
            palette.setColor(QPalette.Window, Qt.white)
            palette.setColor(QPalette.WindowText, Qt.black)
            palette.setColor(QPalette.Base, Qt.white)
            palette.setColor(QPalette.AlternateBase, QColor(246,246,246))
            palette.setColor(QPalette.ToolTipBase, QColor(255,255,220))
            palette.setColor(QPalette.ToolTipText, Qt.black)
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, QColor(240,240,240))
            palette.setColor(QPalette.ButtonText, Qt.black)
            palette.setColor(QPalette.BrightText, Qt.white)
            palette.setColor(QPalette.Link, Qt.blue)
            palette.setColor(QPalette.Highlight, Qt.darkBlue)
            palette.setColor(QPalette.HighlightedText, Qt.white)
            app.setPalette(palette)
    def open_folder(self):
        dir_ = QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QFileDialog.ShowDirsOnly)
        for (dirpath, dirnames, filenames) in os.walk(dir_):
            for tfile in filenames :
                if tfile.endswith(".264") or tfile.endswith(".3ga") or tfile.endswith(".3gp") or tfile.endswith(".aac") or tfile.endswith(".avi") or tfile.endswith(".cda") or tfile.endswith(".dash") or tfile.endswith(".dvr")  or tfile.endswith(".flac") or tfile.endswith(".ifo") or tfile.endswith(".m2t") or tfile.endswith(".m2ts") or tfile.endswith(".m3u8") or tfile.endswith(".m4v") or tfile.endswith(".mkv") or tfile.endswith(".mov") or tfile.endswith(".mp3") or tfile.endswith(".mp4") or tfile.endswith(".mpg") or tfile.endswith(".mts") or tfile.endswith(".ogg") or tfile.endswith(".ogu") or tfile.endswith(".opus") or tfile.endswith(".pls") or tfile.endswith(".rec") or tfile.endswith(".rmvb") or tfile.endswith(".snd") or tfile.endswith(".sub") or tfile.endswith(".ts") or tfile.endswith(".vob") or tfile.endswith(".webm") or tfile.endswith(".wma") or tfile.endswith(".wmv") or tfile.endswith(".zab"):
                    if (dirpath + "/" + tfile) not in self.list:
                        self.playlist.addMedia(
                            QMediaContent(
                                QUrl.fromLocalFile(dirpath + "/" + tfile)
                            )
                        )
                        self.list.append(dirpath + "/" + tfile)
        self.model.layoutChanged.emit()
    def erroralert(self, *args):
        pass
    def playlist_selection_changed(self, ix):
        # We receive a QItemSelection from selectionChanged.
        i = ix.indexes()[0].row()
        self.playlist.setCurrentIndex(i)
        self.ui.label_5.setText(os.path.basename(self.list[i]))
    def playlist_position_changed(self, i):
        if i > -1:
            ix = self.model.index(i)
            self.ui.listView.setCurrentIndex(ix)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "vedio files(*.264;*.3ga;*.3gp;*.aac;*.avi;*.cda;*.dash;*.dvr;*flac;*.ifo;*.m2t;*.m2ts;*.m3u8;*.m4v;*.mkv;*.mov;*.mp3;*.mp4;*.mpg;*.mts;*.ogg;*.ogu;*.opus;*.pls;*.rec;*.rmvb;*.snd;*.sub;*.ts;*.vob;*.webm;*.wma;*.wmv;*.zab")
        if path and path not in self.list:
            self.playlist.addMedia(
                QMediaContent(
                    QUrl.fromLocalFile(path)
                )
            )
            self.list.append(path)

        self.model.layoutChanged.emit()
        self.plays()
    def update_duration(self, duration):
        self.ui.horizontalSlider.setMaximum(duration)

        if duration >= 0:
            self.ui.label_2.setText(self.hhmmss(duration))
            self.time=self.hhmmss(duration)
    def update_position(self, position):
        if position >= 0:
            self.ui.label_14.setText(str(self.hhmmss(position))+"/"+str(self.time))
            self.ui.label_3.setText(self.hhmmss(position))
        # Disable the events to prevent updating triggering a setPosition event (can cause stuttering).
        self.ui.horizontalSlider.blockSignals(True)
        self.ui.horizontalSlider.setValue(position)
        self.ui.horizontalSlider.blockSignals(False)

    def hhmmss(self,ms):

        # s = 1000
        # m = 60000
        # h = 360000
        h, r = divmod(ms,3600000)
        m, r = divmod(r,60000)
        s, _ = divmod(r,1000)
        return ("%d:%02d:%02d" % (h, m, s)) if h else ("%d:%02d" % (m, s))
    def plays(self):
        if self.current==False:
            self.player.play()
            self.ui.play.setIcon(QIcon(r'C:\Users\Yash\PycharmProjects\ppppp\images\Pause-icon.png'))
            self.current=True
        else:
            self.player.pause()
            self.ui.play.setIcon(QIcon(r'C:\Users\Yash\PycharmProjects\ppppp\images\Button-Play-icon.png'))
            self.current=False
        self.videoWidget.setGeometry(0, 21, self.ui.widget.geometry().width(), self.ui.widget.geometry().height())
        self.working = True
    def voice(self):
        self.player.setVolume(self.ui.horizontalSlider_2.value())
        if self.ui.horizontalSlider_2.value()==0:
            self.ui.sound.setIcon(QIcon(r'C:\Users\Yash\PycharmProjects\ppppp\images\Status-audio-volume-muted-icon.png'))
        else:
            self.ui.sound.setIcon(QIcon(r'C:\Users\Yash\PycharmProjects\ppppp\images\62788-speaker-low-volume-icon.png'))
    def voice1(self):
        if self.ui.horizontalSlider_2.value()>0:
            self.ui.horizontalSlider_2.setValue(0)
            self.player.setVolume(self.ui.horizontalSlider_2.value())
            self.ui.sound.setIcon(QIcon(r'C:\Users\Yash\PycharmProjects\ppppp\images\Status-audio-volume-muted-icon.png'))
        else:
            self.ui.horizontalSlider_2.setValue(30)
            self.player.setVolume(self.ui.horizontalSlider_2.value())
            self.ui.sound.setIcon(QIcon(r'C:\Users\Yash\PycharmProjects\ppppp\images\62788-speaker-low-volume-icon.png'))
    def voice2(self):
        if self.player.volume()<100:
            self.player.setVolume(self.player.volume()+1)
            self.ui.sound.setIcon(
                QIcon(r'C:\Users\Yash\PycharmProjects\ppppp\images\62788-speaker-low-volume-icon.png'))
            self.ui.horizontalSlider_2.setValue(self.player.volume())
    def voice3(self):
        if self.player.volume()>-1:
            self.player.setVolume(self.player.volume()-1)
        if self.player.volume()==0:
            self.ui.sound.setIcon(QIcon(r'C:\Users\Yash\PycharmProjects\ppppp\images\Status-audio-volume-muted-icon.png'))
        self.ui.horizontalSlider_2.setValue(self.player.volume())
    def silent(self):
        self.player.setVolume(0)
        self.ui.sound.setIcon(QIcon(r'C:\Users\Yash\PycharmProjects\ppppp\images\62788-speaker-low-volume-icon.png'))
class ViewerWindow(QMainWindow):
    state = pyqtSignal(bool)
    def closeEvent(self, e):
        # Emit the window state, to update the viewer toggle button.
        self.state.emit(False)


class PlaylistModel(QAbstractListModel):
    def __init__(self, playlist, *args, **kwargs):
        super(PlaylistModel, self).__init__(*args, **kwargs)
        self.playlist = playlist

    def data(self, index, role):
        if role == Qt.DisplayRole:
            media = self.playlist.media(index.row())
            return media.canonicalUrl().fileName()

    def rowCount(self, index):
        return self.playlist.mediaCount()
if __name__=="__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(r'C:\Users\Yash\PycharmProjects\ppppp\App-Media-icon.png'))
    w = GUI()
    app.setStyle("Fusion")
    w.background2()
    app.exec_()
