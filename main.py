import os
import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from karta import Ui_MainWindow


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.searchThing()
        self.search.setFocus()
        self.search.clicked.connect(self.searchThing)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.zoom.value() < 18:
                self.zoom.setValue(self.zoom.value() + 1)
        if event.key() == Qt.Key_PageDown:
            if self.zoom.value() > 1:
                self.zoom.setValue(self.zoom.value() - 1)

    def searchThing(self):
        api_server = "http://static-maps.yandex.ru/1.x/"
        lat = str(self.width_1.value())
        lon = str(self.long_2.value())
        map_type = ["map", 'sat']
        z = int(self.zoom.value()) - 1
        params = {
            "ll": ",".join([lon, lat]),
            "l": map_type[0],
            'z': z,
        }
        response = requests.get(api_server, params=params)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        self.map.setPixmap(QPixmap("map.png").scaled(300, 300))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
