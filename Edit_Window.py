import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene,
    QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem,
    QGraphicsItem, QWidget, QPushButton, QVBoxLayout, QComboBox,
    QGraphicsTextItem, QMenu, QLineEdit, QLabel, QFormLayout
)
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPointF, QLineF

class EditWindow(QWidget):
    def __init__(self, component_item, is_smelter=False):
        super().__init__()
        self.component_item = component_item
        self.is_smelter = is_smelter
        self.setWindowTitle("Edit Production Rate")

        layout = QFormLayout()

        if is_smelter:
            self.input_rate_edit = QLineEdit(str(self.component_item.input_rate))
            self.output_rate_edit = QLineEdit(str(self.component_item.output_rate))
            layout.addRow(QLabel("Input Rate (items/min):"), self.input_rate_edit)
            layout.addRow(QLabel("Output Rate (items/min):"), self.output_rate_edit)
        else:
            self.output_rate_edit = QLineEdit(str(self.component_item.output_rate))
            layout.addRow(QLabel("Production Rate (items/min):"), self.output_rate_edit)

        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.apply_changes)
        layout.addWidget(apply_button)

        self.setLayout(layout)

    def apply_changes(self):
        try:
            if self.is_smelter:
                new_input_rate = float(self.input_rate_edit.text())
                new_output_rate = float(self.output_rate_edit.text())
                self.component_item.update_production_rates(new_input_rate, new_output_rate)
            else:
                new_output_rate = float(self.output_rate_edit.text())
                self.component_item.update_production_rate(new_output_rate)
            self.close()
        except ValueError:
            # Handle invalid input
            pass
