# PyQt GUI for EchoMind AutoLoop
# Handles conversation display, controls, and update logs
from PyQt5 import QtWidgets, QtCore
import sys

class EchoLoopUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('EchoMind AutoLoop')
        self.resize(900, 600)

        self.log_area = QtWidgets.QTextEdit(self)
        self.log_area.setReadOnly(True)

        self.start_btn = QtWidgets.QPushButton('Start')
        self.stop_btn = QtWidgets.QPushButton('Stop')
        self.pause_btn = QtWidgets.QPushButton('Pause')

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.log_area)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.pause_btn)
        layout.addWidget(self.stop_btn)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = EchoLoopUI()
    win.show()
    sys.exit(app.exec_())
