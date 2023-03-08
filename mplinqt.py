from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigCan
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavToo
from matplotlib.figure import Figure
class MPLinQT(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.canvas = FigCan(Figure())
        
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)