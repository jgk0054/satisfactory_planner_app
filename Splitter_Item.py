import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene,
    QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem,
    QGraphicsItem, QWidget, QPushButton, QVBoxLayout, QComboBox,
    QGraphicsTextItem, QMenu, QLineEdit, QLabel, QFormLayout
)
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPointF, QLineF
from Component_Item import ComponentItem
from Port_Item import PortItem
from Connection_Line_Item import ConnectionLineItem
from Recipe_Selection_Window import RecipeSelectionWindow
from Edit_Window import EditWindow



class SplitterItem(ComponentItem):
    def __init__(self, width=50, height=50):
        super().__init__(width, height, "Splitter")
        self.setBrush(QBrush(QColor("lightblue")))
        self.input_rate = 0
        self.output_rate = 0

        # Create one input port in the middle of the left side
        self.input_port = PortItem(-10, (height - 10) / 2, 10, 10, 'input', self)

        # Create three evenly spaced output ports on the right side
        self.output_ports = [
            PortItem(width, (i + 1) * (height / 4) - 5, 10, 10, 'output', self) 
            for i in range(3)
        ]

    def calculate_throughput(self):
        # Calculate throughput per output port based on the number of connections
    #    print(self.input_port.connections)
        #calculate number out outgoing connections
        #update input rate
        self.input_rate = 0
        if len(self.input_port.connections) > 0:
            for connection in self.input_port.connections:
                print(connection.transfer_rate)
                self.input_rate += connection.transfer_rate
        
        connectionCounter = 0
        for port in self.output_ports:
            connectionCounter += len(port.connections)

        if len(self.input_port.connections) == 0:
            self.output_rate = 0
        elif connectionCounter > 0:
            self.output_rate = self.input_rate / connectionCounter
            for port in self.output_ports:
                for connection in port.connections:
                    connection.transfer_rate = self.output_rate
                    connection.rate_label.setPlainText(connection.get_label_text())

        else:
            self.output_rate = self.input_rate