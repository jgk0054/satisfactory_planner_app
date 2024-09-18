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


class MergerItem(ComponentItem):
    def __init__(self, width=50, height=50):
        super().__init__(width, height, "Merger")
        self.setBrush(QBrush(QColor("purple")))

        # Create two evenly spaced input ports on the left side
        # self.input_ports = [
        #     PortItem(-10, (i + 1) * (height / 4) - 5, 10, 10, 'input', self) 
        #     for i in range(3)
        # ]

        self.input_ports = [
            PortItem(-10, (i + 1) * (height / 4) - 5, 10, 10, 'input', self) 
            for i in range(3)
        ]


        # Create one output port in the middle of the right side
        self.output_port = PortItem(width, (height - 10) / 2, 10, 10, 'output', self)

        # No production rates; simply passes items through
        self.input_rate = None
        self.output_rate = None

    def calculate_throughput(self):
        self.input_rate = 0
        self.output_rate = 0
        
        for port in self.input_ports:
            if len(port.connections) > 0:
                for connection in port.connections:
                    self.input_rate += connection.transfer_rate
        
        if len(self.output_port.connections) > 0:
            for connection in self.output_port.connections:
                if self.input_rate > connection.capacity:
                    connection.transfer_rate = connection.capacity
                else:
                    connection.transfer_rate = self.input_rate
                    connection.rate_label.setPlainText(connection.get_label_text())
                self.output_rate = self.input_rate