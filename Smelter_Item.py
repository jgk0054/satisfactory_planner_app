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



class SmelterItem(ComponentItem):
    def __init__(self, width=100, height=50):
        super().__init__(width, height, "Smelter")
        self.setBrush(QBrush(QColor("orange")))

        # Default stats
        self.recipe = "Iron Ingot"
        self.input_rate = 30  # Items per minute
        self.output_rate = 30  # Items per minute
        self.power_consumption = 4  # MW

        # Create input and output ports
        self.input_port = PortItem(-10, (height - 10) / 2, 10, 10, 'input', self)
        self.output_port = PortItem(width, (height - 10) / 2, 10, 10, 'output', self)

        # Add a label to display current recipe and rates
        self.recipe_label = QGraphicsTextItem(self.get_label_text(), self)
        self.recipe_label.setPos(5, 5)

    def get_label_text(self):
        return f"{self.recipe}\n{self.input_rate}/{self.output_rate} items/min"

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.show_context_menu(event)
        else:
            super().mousePressEvent(event)

    def show_context_menu(self, event):
        menu = QMenu()
        recipe_action = menu.addAction("Select Recipe")
        edit_action = menu.addAction("Edit Production Rates")
        delete_action = menu.addAction("Delete Smelter")
        action = menu.exec_(event.screenPos())
        if action == recipe_action:
            self.show_recipe_selection()
        elif action == edit_action:
            self.show_edit_window()
        elif action == delete_action:
            self.scene().removeItem(self)

    def show_recipe_selection(self):
        self.recipe_selection_window = RecipeSelectionWindow(self, is_smelter=True)
        self.recipe_selection_window.show()

    def show_edit_window(self):
        self.edit_window = EditWindow(self, is_smelter=True)
        self.edit_window.show()

    def update_recipe(self, new_recipe):
        # Update the recipe and production stats
        self.recipe = new_recipe
        # Update rates based on recipe
        if self.recipe == "Iron Ingot":
            self.input_rate = 30
            self.output_rate = 30
        elif self.recipe == "Copper Ingot":
            self.input_rate = 30
            self.output_rate = 30
        # Update the label to display the new recipe and rates
        self.recipe_label.setPlainText(self.get_label_text())
        # Update connected connections' transfer rates
        for connection in self.input_port.connections + self.output_port.connections:
            connection.update_transfer_rate()

    def update_production_rates(self, new_input_rate, new_output_rate):
        self.input_rate = new_input_rate
        self.output_rate = new_output_rate
        self.recipe_label.setPlainText(self.get_label_text())
        # Update connected connections' transfer rates
        for connection in self.input_port.connections + self.output_port.connections:
            connection.update_transfer_rate()
