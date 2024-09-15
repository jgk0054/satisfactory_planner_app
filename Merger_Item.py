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
        self.input_ports = [
            PortItem(-10, (i + 1) * (height / 4) - 5, 10, 10, 'input', self) 
            for i in range(2)
        ]

        # Create one output port in the middle of the right side
        self.output_port = PortItem(width, (height - 10) / 2, 10, 10, 'output', self)

        # No production rates; simply passes items through
        self.input_rate = None
        self.output_rate = None

    def calculate_throughput(self):
        # Sum the input rates from all connected inputs
        connected_inputs = [port for port in self.input_ports if len(port.connections) > 0]
        total_input_rate = sum(port.input_rate for port in connected_inputs if port.input_rate)

        # Set the output rate to the sum of input rates
        self.output_port.output_rate = total_input_rate if connected_inputs else 0