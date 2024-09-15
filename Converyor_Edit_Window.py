
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene,
    QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem,
    QGraphicsItem, QWidget, QPushButton, QVBoxLayout, QComboBox,
    QGraphicsTextItem, QMenu, QLineEdit, QLabel, QFormLayout
)
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPointF, QLineF


class ConveyorEditWindow(QWidget):
    def __init__(self, connection_item):
        super().__init__()
        self.connection_item = connection_item
        self.setWindowTitle("Edit Conveyor Capacity")

        layout = QFormLayout()
        self.capacity_edit = QLineEdit(str(self.connection_item.capacity))
        layout.addRow(QLabel("Capacity (items/min):"), self.capacity_edit)

        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.apply_changes)
        layout.addWidget(apply_button)

        self.setLayout(layout)

    def apply_changes(self):
        try:
            new_capacity = float(self.capacity_edit.text())
            self.connection_item.capacity = new_capacity
            self.connection_item.update_transfer_rate()
            self.close()
        except ValueError:
            # Handle invalid input
            pass
