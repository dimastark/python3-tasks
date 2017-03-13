#!/usr/bin/env python3
"""Main module for dimastark's Gif Informer"""
# FIXME: fix this ugly file


import os
import sys

from PyQt5.QtCore import QByteArray
from PyQt5.QtGui import QColor, QMovie
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QSizePolicy
from PyQt5.QtWidgets import QFileDialog, QMenu, QGridLayout, QComboBox, QScrollArea
from PyQt5.QtWidgets import QLabel, QPushButton, QTextEdit, QMessageBox

from gifparse.gifparser import GifInfo

DIR = os.path.dirname(os.path.abspath(__file__))


class ImagePlayer(QWidget):
    """Gif player"""
    def __init__(self, parent=None):
        """Initialisation of GUI"""
        QWidget.__init__(self, parent)
        self.close_with_dialog = True
        self.i_ip = 0
        self.filename = QFileDialog.getOpenFileName(self, 'Open file', '.')[0]
        if not self.filename:
            sys.exit()
        path = os.path.dirname(self.filename)
        ldir = os.listdir(path=path)
        os.chdir(path)
        self.pall_widget = QWidget()
        self.frames_widget = QWidget()
        self.files = [os.path.abspath(i) for i in ldir if os.path.isfile(i) and GifInfo.try_parse(i)]
        if not self.files:
            raise ValueError("There is no correct images")
        if self.filename not in self.files:
            descr = "Corrupt image"
            inform = "Automatic select next image in directory..."
            QMessageBox.about(self, descr, inform)
            self.filename = self.files[0]
        self.gifinfos = {self.filename: GifInfo(self.filename)}
        self.gifinfo = self.gifinfos[self.filename]
        self.f_ip = self.files.index(self.filename)
        self.played = True
        self.init_buttons()
        self.init_qmovie()
        self.init_main_layout()
        self.setWindowTitle("Gif Parse")
        self.tmp_widget = QWidget()
        self.setLayout(self.main_layout)

    def on_start(self):
        """Start playing"""
        if self.played:
            self.play_b.text = "Play"
            self.movie.stop()
        else:
            self.play_b.text = "Stop"
            self.movie.start()
        self.played = not self.played

    def init_qmovie(self):
        """QMovie Initialisation"""
        self.movie = QMovie(self.filename, QByteArray(), self)
        self.movie_screen = QLabel()
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.movie_screen.setMovie(self.movie)
        self.movie.start()

    def init_buttons(self):
        """Buttons Initialisation"""
        self.play_b = QPushButton("&Play")
        self.play_b.clicked.connect(self.on_start)
        self.nxt_b = QPushButton(">")
        self.nxt_b.clicked.connect(self.next_gif_b)
        self.prv_b = QPushButton("<")
        self.prv_b.clicked.connect(self.prev_gif_b)
        self.info_b = QPushButton("&Info")
        self.info_b.clicked.connect(self.on_info)
        self.readme_b = QPushButton("&Readme")
        self.readme_b.clicked.connect(self.on_readme)

    def init_main_layout(self):
        """Initialization of main layout"""
        self.main_layout = QGridLayout()
        self.main_layout.setSpacing(2)
        self.main_layout.addWidget(self.movie_screen, 0, 0, 1, 5)
        self.main_layout.addWidget(self.play_b, 1, 1)
        self.main_layout.addWidget(self.prv_b, 1, 0)
        self.main_layout.addWidget(self.nxt_b, 1, 2)
        self.main_layout.addWidget(self.info_b, 1, 3)
        self.main_layout.addWidget(self.readme_b, 1, 4)

    def on_info(self):
        """Show info"""
        info = self.gifinfo
        infos = []
        infos.append(info.spec)
        infos.append(str(info.size[0]) + "x" + str(info.size[1]))
        infos.append(str(info.aratio))
        infos.append(str(info.loops))
        infos.append(str(len(info.frames)))
        fields_name = ["Type", "Size", "Ratio", "Count of loops", "Count of frames"]
        self.tmp_widget.setLayout(self.layout())
        layout = QGridLayout(self)
        layout.setSpacing(8)
        back = QPushButton("Back")
        back.clicked.connect(self.on_back)
        full = QPushButton("Full info to txt")
        full.clicked.connect(self.on_make_info)
        for text, i in zip(infos, range(len(infos))):
            widget = QLineEdit(text)
            widget.setReadOnly(True)
            layout.addWidget(QLabel(fields_name[i]), i, 0)
            layout.addWidget(widget, i, 1, 1, 1)
        if info.comments:
            widget = QLineEdit(info.comments[0])
            widget.setReadOnly(True)
            layout.addWidget(QLabel("Comments:"), 6, 0)
            layout.addWidget(widget, 6, 1)
        pal_b = QPushButton("Pallete")
        pal_b.clicked.connect(self.on_pallete_b)
        fr_b = QPushButton("About frames")
        fr_b.clicked.connect(self.on_frames_b)
        layout.addWidget(pal_b, 7, 0)
        layout.addWidget(fr_b, 7, 1)
        layout.addWidget(full, 8, 0)
        layout.addWidget(back, 8, 1)
        self.setLayout(layout)

    def on_readme(self):
        """Show readme"""
        self.tmp_widget.setLayout(self.layout())
        layout = QGridLayout(self)
        layout.setSpacing(6)
        back = QPushButton("Back")
        back.clicked.connect(self.on_back)
        with open(DIR + '/readme.txt', mode='r') as txt:
            from_file = txt.read()
            txt_widget = QTextEdit()
            for line in from_file.split('\n'):
                txt_widget.append(line)
            txt_widget.setReadOnly(True)
            layout.addWidget(txt_widget, 0, 0, 1, 5)
        layout.addWidget(back, 5, 1)
        self.setLayout(layout)

    def on_back(self):
        """Back to main_layout"""
        QWidget().setLayout(self.layout())
        self.setLayout(self.tmp_widget.layout())

    def on_back_pal(self):
        """Back to main_layout"""
        QWidget().setLayout(self.layout())
        self.setLayout(self.pall_widget.layout())

    def on_back_frames(self):
        """Back to main_layout"""
        QWidget().setLayout(self.layout())
        self.setLayout(self.frames_widget.layout())

    def on_make_info(self):
        """Make info file"""
        name = str(os.path.basename(self.gifinfo.name)).split('.')[0]
        if not os.path.exists(name + "info.txt"):
            with open(name + "info.txt", mode='w') as file:
                file.write(self.gifinfo.to_str())
        QMessageBox.about(self, "Make txt", "Finished")

    def closeEvent(self, event):
        """When window closed"""
        quit_msg = "Are you sure you want to close this program?"
        if self.close_with_dialog:
            reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)
        else:
            reply = QMessageBox.Yes
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def contextMenuEvent(self, event):
        """Handling context Menu"""
        menu = QMenu(self)
        open_act = menu.addAction("Open new")
        menu.addAction("Quit")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        self.close_with_dialog = False
        self.close()
        if action == open_act:
            main()

    def next_gif(self, direction):
        """Choose next gif in directory"""
        self.f_ip += direction
        self.f_ip += len(self.files)
        self.f_ip %= len(self.files)
        self.i_ip = 0
        self.filename = self.files[self.f_ip]
        if self.filename not in self.gifinfos:
            self.gifinfos[self.filename] = GifInfo(self.filename)
        self.gifinfo = self.gifinfos[self.filename]
        self.movie = QMovie(self.filename, QByteArray(), self)
        self.movie_screen.setMovie(self.movie)
        self.movie.start()

    def next_gif_b(self):
        """nxt_b event"""
        self.next_gif(1)

    def prev_gif_b(self):
        """prv_b event"""
        self.next_gif(-1)

    def keyPressEvent(self, event):
        """Key pressed event"""
        if event.key() == 44:
            self.next_gif(-1)
        elif event.key() == 46:
            self.next_gif(1)

    def on_pallete_b(self):
        """Make layout for pallete window"""
        lay = QGridLayout()
        wind = QWidget()
        wind_lay = QGridLayout()
        wind.setLayout(lay)
        self.pall_widget.setLayout(self.layout())
        for i, color in enumerate(self.gifinfo.colors):
            lab = QLabel()
            col = QColor(*color)
            lab.setStyleSheet("QFrame { background-color: %s }" % col.name())
            lay.addWidget(lab, i // 10, i % 10)
        back = QPushButton("Back")
        scroll = QScrollArea()
        scroll.setWidget(wind)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(200)
        wind_lay.addWidget(scroll)
        wind_lay.addWidget(back)
        self.setLayout(wind_lay)
        back.clicked.connect(self.on_back_pal)

    @staticmethod
    def make_frame_wid(frame):
        """Make specific widget for some gif's frame"""
        lay = QGridLayout()
        wid = QWidget()
        colors = QWidget()
        colors_lay = QGridLayout()
        colors.setLayout(colors_lay)
        data = []
        data += (frame.x, frame.y)
        data += (frame.width, frame.height)
        data.append(frame.delay)
        names = ["x", "y", "Width", "Heigth", "Delay"]
        for i in range(len(data)):
            lay.addWidget(QLabel(names[i]), i, 0)
            widget = QLineEdit(str(data[i]))
            widget.setReadOnly(True)
            lay.addWidget(widget, i, 1)
        for i, color in enumerate(frame.colors):
            lab = QLabel()
            col = QColor(*color)
            lab.setStyleSheet("QFrame { background-color: %s }" % col.name())
            colors_lay.addWidget(lab, 5 + i // 10, i % 10)
        scroll = QScrollArea()
        scroll.setWidget(colors)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(200)
        lay.addWidget(scroll, 4, 0, 2, 2)
        wid.setLayout(lay)
        return wid

    def change_frame_lay(self, lay):
        """Select info about selected frame in ComboBox"""
        self.lays[self.prev].setLayout(self.fr_wid.layout())
        self.prev = lay
        self.fr_wid.setLayout(self.lays[lay].layout())

    def on_frames_b(self):
        """Frames info event"""
        empty_lay = QGridLayout()
        self.frames_widget.setLayout(self.layout())
        self.lays = {}
        self.prev = '0'
        self.fr_wid = QWidget()
        lay = QGridLayout()
        for i, frame in enumerate(self.gifinfo.frames):
            self.lays[str(i)] = ImagePlayer.make_frame_wid(frame)
        combs = QComboBox()
        combs.addItems([str(i) for i in range(len(self.gifinfo.frames))])
        combs.activated[str].connect(self.change_frame_lay)
        lay.addWidget(combs)
        if self.lays:
            self.fr_wid.setLayout(self.lays['0'].layout())
        else:
            self.fr_wid.setLayout(empty_lay)
        lay.addWidget(self.fr_wid)
        back = QPushButton("Back")
        lay.addWidget(back)
        back.clicked.connect(self.on_back_frames)
        self.setLayout(lay)


def main():
    """Entry of application"""
    app = QApplication(sys.argv)
    window = ImagePlayer()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
