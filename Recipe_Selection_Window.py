
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene,
    QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem,
    QGraphicsItem, QWidget, QPushButton, QVBoxLayout, QComboBox,
    QGraphicsTextItem, QMenu, QLineEdit, QLabel, QFormLayout
)
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPointF, QLineF


class RecipeSelectionWindow(QWidget):
    def __init__(self, component_item, is_smelter=False):
        super().__init__()
        self.component_item = component_item
        self.setWindowTitle("Select Recipe")

        # Set up the layout
        layout = QVBoxLayout()
        self.combo_box = QComboBox()
        if is_smelter:
            self.combo_box.addItems(["Iron Ingot", "Copper Ingot"])
        else:
            self.combo_box.addItems(["Iron Ore", "Copper Ore", "Coal"])
        # Set the current index to the component's current recipe
        index = self.combo_box.findText(self.component_item.recipe)
        if index >= 0:
            self.combo_box.setCurrentIndex(index)
        layout.addWidget(self.combo_box)

        # Add a button to apply the selection
        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.apply_selection)
        layout.addWidget(apply_button)

        self.setLayout(layout)

    def apply_selection(self):
        selected_recipe = self.combo_box.currentText()
        self.component_item.update_recipe(selected_recipe)
        self.close()
