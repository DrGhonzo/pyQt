#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: 850 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from QLed import QLed
from gauge import AnalogGauge
from color_button import ColorButton

class indicator_graphics_object(QTabWidget):
    '''Indicator graphics object build the visual representation of the "analog" control.
    Config: at the time host, port of the hardware and the read register address. Write register is for control porpose.  '''
    # TODO: implement an alarm setup & it's popup system and logs.
    def __init__(self, parent=None, _type='Radial'):
        QTabWidget.__init__(self, parent=parent)
        self.setMaximumSize(320, 320)
        self._suffix = ' Bar'
        self._alias = ''
        self._type = _type
        self.init()

    def init(self):

        self.frame = QGroupBox()

        mainLayout = QVBoxLayout()
        mainHLayout = QHBoxLayout()

        if not self._type == 'Pens':
            if self._type == 'Bar':
                self.gauge = AnalogGauge(typeOf=self._type)
                gaugeLayOut = QHBoxLayout()
                gaugeLayOut.addWidget(self.gauge, Qt.AlignHCenter)
                mainLayout.addLayout(gaugeLayOut)
            elif self._type == 'Radial':
                self.gauge = AnalogGauge(typeOf=self._type)
                mainLayout.addWidget(self.gauge)


            self.penCombo = PenCombo(self)
            self.controlCombo = ControlCombo(self)
            #mainHLayout.addLayout(mainValueLayout)
            mainHLayout.addWidget(self.penCombo)
            mainHLayout.addWidget(self.controlCombo)
            mainLayout.addLayout(mainHLayout)
            mainLayout.setAlignment(Qt.AlignRight)
        if self._type == 'Pens':
            self.penCombo1 = PenCombo(self)
            self.penCombo2 = PenCombo(self)
            self.penCombo3 = PenCombo(self)
            mainLayout.addWidget(self.penCombo1)
            mainLayout.addWidget(self.penCombo2)
            mainLayout.addWidget(self.penCombo3)


        self.frame.setLayout(mainLayout)
        self.setTabPosition(QTabWidget.West)
        self.addTab(self.frame, '')
        self.config = Config()
        self.addTab(self.config, 'Config')
        self.control = Control()
        self.addTab(self.control, 'Control')
        self.comms = Comms()
        self.addTab(self.comms, 'Comms')
        self.setTabEnabled(2,False)
        self.setTabEnabled(3,False)

        self.show()


class Comms(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.init()

    def init(self):
        lay = QVBoxLayout()
        self.comms = QGroupBox()
        #self.comms.setTitle('Comms')
        form1 = QFormLayout()
        self.host = QLineEdit()
        hostLbl = QLabel('host')
        form1.addRow(hostLbl,self.host)
        self.port = QSpinBox()
        self.port.setMaximum(1023)
        portLbl = QLabel('port')
        form1.addRow(portLbl,self.port)

        self.reads = QGroupBox()
        self.reads.setTitle('Read')
        form2 = QFormLayout()

        self.addrRead = QSpinBox()
        addrRLbl = QLabel('addr')
        form2.addRow(addrRLbl,self.addrRead)

        self.regRead = QSpinBox()
        regRLbl = QLabel('reg')
        form2.addRow(regRLbl, self.regRead)

        self.writes = QGroupBox()
        self.writes.setTitle('Write')
        form3 = QFormLayout()

        self.addrWrite = QSpinBox()
        addrWLbl = QLabel('addr')
        form3.addRow(addrWLbl, self.addrWrite)

        self.regWrite = QSpinBox()
        regWLbl = QLabel('reg')
        form3.addRow(regWLbl,self.regWrite)

        self.comms.setLayout(form1)
        self.reads.setLayout(form2)
        self.writes.setLayout(form3)
        lay.addWidget(self.comms)
        lay.addWidget(self.reads)
        lay.addWidget(self.writes)
        self.setLayout(lay)


class Config(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.init()

    def init(self):
        lay = QVBoxLayout()
        self.vars = QGroupBox()
        #self.vars.setTitle('Variables')
        form1 = QFormLayout()

        self.alias = QLineEdit()
        self.alias.setMinimumHeight(22)
        aliasLbl = QLabel('alias')
        form1.addRow(aliasLbl,self.alias)

        self.zero = QDoubleSpinBox()
        self.zero.setMinimumHeight(22)
        self.zero.setMaximum(1000)
        self.zero.setMinimum(-1000)
        self.zero.setAlignment(Qt.AlignRight)
        zerolbl = QLabel('zero')
        form1.addRow(zerolbl,self.zero)

        self.span = QDoubleSpinBox()
        self.span.setMinimumHeight(22)
        self.span.setMaximum(1000)
        self.span.setMinimum(-1000)
        self.span.setAlignment(Qt.AlignRight)
        spanLbl = QLabel('span')
        form1.addRow(spanLbl,self.span)

        self.units = QLineEdit()
        self.units.setMinimumHeight(22)
        self.units.setAlignment(Qt.AlignRight)
        unitLbl = QLabel('units')
        form1.addRow(unitLbl,self.units)
        self.advanced = QPushButton('Avanzado...')
        form1.addWidget(self.advanced)

        self.vars.setLayout(form1)

        lay.addWidget(self.vars)

        self.setLayout(lay)


class Control(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.init()

    def init(self):
        lay = QVBoxLayout()
        self.control = QGroupBox()
        self.control.setTitle('Habilitar')
        self.control.setCheckable(True)
        form1 = QFormLayout()

        self.setPoint = QDoubleSpinBox()
        self.setPoint.setMinimumHeight(22)
        self.setPoint.setDecimals(1)
        self.setPoint.setMaximum(1000)
        self.setPoint.setAlignment(Qt.AlignRight)
        setPointLbl = QLabel('set point')
        form1.addRow(setPointLbl, self.setPoint)

        self.select = QComboBox()
        self.select.insertItem(0,'On/Off')
        self.select.insertItem(1,'PID')
        self.select.setMinimumHeight(22)
        selectLbl = QLabel('type')
        form1.addRow(selectLbl, self.select)

        self.control.setLayout(form1)

        form2 = QFormLayout()
        self.onOff = QGroupBox()
        self.onOff.setTitle('On/Off')
        self.histeresis = QDoubleSpinBox()
        self.histeresis.setMinimumHeight(22)
        self.histeresis.setDecimals(1)
        self.histeresis.setMaximum(100)
        self.histeresis.setPrefix('+/- ')
        self.histeresis.setSuffix(' %')
        self.histeresis.setAlignment(Qt.AlignRight)

        histeLbl = QLabel('hist')
        form2.addRow(histeLbl,self.histeresis)
        self.onOff.setLayout(form2)
        self.onOff.setEnabled(False)

        self.pid = QGroupBox()
        self.pid.setTitle('PID')
        form3 = QFormLayout()
        self.kP = QDoubleSpinBox()
        self.kP.setMinimumHeight(22)
        self.kP.setDecimals(1)
        self.kP.setAlignment(Qt.AlignRight)
        kpLbl = QLabel('kP')
        form3.addRow(kpLbl,self.kP)

        self.kI = QDoubleSpinBox()
        self.kI.setMinimumHeight(22)
        self.kI.setDecimals(1)
        self.kI.setAlignment(Qt.AlignRight)
        kiLbl = QLabel('kI')
        form3.addRow(kiLbl,self.kI)

        self.kD = QDoubleSpinBox()
        self.kD.setMinimumHeight(22)
        self.kD.setDecimals(1)
        self.kD.setAlignment(Qt.AlignRight)
        kdLbl = QLabel('kD')
        form3.addRow(kdLbl,self.kD)
        self.pid.setLayout(form3)
        self.pid.setEnabled(False)

        lay.addWidget(self.control)
        lay.addWidget(self.onOff)
        lay.addWidget(self.pid)

        self.setLayout(lay)


class PenCombo(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self._suffix = parent._suffix
        self.init()

    def init(self):
        self.value = QDoubleSpinBox()
        self.value.setDecimals(1)
        self.value.setSuffix(self._suffix)
        self.value.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.value.setReadOnly(True)
        self.value.setAlignment(Qt.AlignRight)

        self.colorPen = ColorButton()
        self.enablePen = QCheckBox()
        self.enablePen.setObjectName('enable')
        self.enablePen.setChecked(True)

        hValueLayout = QHBoxLayout()
        hValueLayout.addWidget(self.colorPen)
        hValueLayout.addSpacing(15)
        hValueLayout.addWidget(self.enablePen)
        hValueLayout.setAlignment(Qt.AlignJustify)

        mainValueLayout = QVBoxLayout()
        mainValueLayout.addWidget(self.value)
        mainValueLayout.addLayout(hValueLayout)

        self.setLayout(mainValueLayout)


class ControlCombo(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.init()

    def init(self):
        self.action = QPushButton('Abrir')
        self.action.setObjectName('action')
        self.action.setMinimumSize(70, 27)
        self.stateLed = QLed(self, onColour=QLed.Green, offColour=QLed.Red)
        self.stateLed.setMaximumSize(27, 27)

        vContLayout = QVBoxLayout()
        vContLayout.addWidget(self.action)
        vContLayout.addWidget(self.stateLed)
        vContLayout.setAlignment(Qt.AlignRight)

        self.setLayout(vContLayout)



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    indicator = indicator_graphics_object()
    indicator.show()
    sys.exit(app.exec_())
