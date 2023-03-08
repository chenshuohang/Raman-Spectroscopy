import numpy as np, matplotlib.pyplot as plt
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import sys
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import serial
from PyQt5.QtCore import *
import time
from serial.tools import list_ports
class MsgBox:
    def __init__(self, title, mesg, flag = 0):
        msg = QMessageBox()
        msg.setText(mesg)
        msg.setWindowTitle(title)
        if flag == 0:
            msg.setStandardButtons(QMessageBox.Ok)
        else:
            msg.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
        msg.exec_()
class Datacollect(QRunnable):
    def __init__(self, ser, canv):
        super(Datacollect, self).__init__()
        self.ser = ser
        self.canvas = canv
    @pyqtSlot()
    def run(self):
        self.ser.write(b'#IT:001ss%')
        self.ser.write(b'#Start%')
        while(1):
            try:
                self.ser.read_until(b'\x00\x00')
                x = self.ser.read(7388)
                self.dat0 = []
                for i in range(0,3694):
                    self.dat0.append(int.from_bytes(x[i*2:i*2+2], 'little'))
                print(self.dat0)
                self.canvas.axes.cla()
                self.canvas.axes.plot(self.dat0)
                self.canvas.draw()
                QThread.msleep(1000)
            except Exception as e:
                MsgBox('ERROR', '数据接受时出现错误：\n' + str(e))
                break


class MainWin(QtWidgets.QMainWindow):
    def CCDConnect(self):
        '''
        CCD Connection.
        '''
        try:
            self.ser = serial.Serial(str(self.lstports.currentText())[0:4], 9600, timeout=0.5)
            MsgBox('Success', '仪器连接成功')
            self.pushButton.setText('断开连接')
        except Exception as e:
            MsgBox('ERROR', '仪器连接出现错误：\n'+ str(e))
        if self.ser.is_open()==False:
            self.seri = Datacollect(self.ser, self.plotting.canvas)
        else:
            self.ser.close()
            self.pushButton.setText('连接仪器')

    def StartCollection(self, checked):
        if hasattr(self, 'seri'):
            if(checked):
                self.threadpools.start(self.seri)
            else:
                self.ser.write('#Stop%')
        else:
            MsgBox('ERROR', '仪器未连接')

    def Saving_datas(self):
        now = time.localtime()
        file_name = time.strftime('%a, %d %b %Y %H_%M_%S', now)
        if hasattr(self, 'datas'):
            with open(f'{file_name}.txt','w') as f:
                f.write(str(self.datas))
            MsgBox('Success', f'文件已经保存于{file_name}.txt')
        else:
            MsgBox('ERROR', '没有可供保存的数据！')

    def __init__(self):
        super(MainWin, self).__init__()
        self.threadpools = QThreadPool()
        uic.loadUi('MyUI.ui', self)
        self.setWindowTitle("拉曼光谱测定实验小助手")
        self.ports = list(list_ports.comports())
        self.lstports.addItems(map(str, self.ports))
        self.pushButton.clicked.connect(self.CCDConnect)
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.clicked.connect(self.StartCollection)
        self.Button_Save.clicked.connect(self.Saving_datas)
        self.toolbar = NavigationToolbar(self.plotting.canvas, self)
        self.addToolBar(self.toolbar)
        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    wind = MainWin()
    app.exec_()