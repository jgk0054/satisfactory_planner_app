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

        # Create one input port in the middle of the left side
        self.input_port = PortItem(-10, (height - 10) / 2, 10, 10, 'input', self)

        # Create three evenly spaced output ports on the right side
        self.output_ports = [
            PortItem(width, (i + 1) * (height / 4) - 5, 10, 10, 'output', self) 
            for i in range(3)
        ]

        # No production rates; simply passes items through
        self.input_rate = None
        self.output_rate = None

    def calculate_throughput(self):
        # Calculate throughput per output port based on the number of connections
        connected_outputs = [port for port in self.output_ports if len(port.connections) > 0]
        if self.input_rate and connected_outputs:
            rate_per_output = self.input_rate / len(connected_outputs)
            for port in connected_outputs:
                port.output_rate = rate_per_output
        else:
            for port in self.output_ports:
                port.output_rate = 0  # No output if no input or no connected outputs
