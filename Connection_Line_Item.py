from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene,
    QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem,
    QGraphicsItem, QWidget, QPushButton, QVBoxLayout, QComboBox,
    QGraphicsTextItem, QMenu, QLineEdit, QLabel, QFormLayout
)
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPointF, QLineF
from Converyor_Edit_Window import ConveyorEditWindow

class ConnectionLineItem(QGraphicsLineItem):
    def __init__(self, start_port, end_port, capacity=60):
        super().__init__()
        self.start_port = start_port
        self.end_port = end_port
        self.capacity = capacity  # Default capacity of the conveyor belt
        self.transfer_rate = 0  # Default transfer rate of the conveyor belt
        self.setPen(QPen(QColor("gray"), 2))
        # Calculate and display the transfer rate
        # Register this connection with the ports
        self.start_port.connections.append(self)
        self.end_port.connections.append(self)
        self.rate_label = QGraphicsTextItem(self.get_label_text(), parent=self)
        self.rate_label.setDefaultTextColor(QColor("black"))
        self.update_transfer_rate()
        self.update_position()


    def get_label_text(self):
        return f"{self.transfer_rate}/{self.capacity} items/min"

    def update_transfer_rate(self):
        from Merger_Item import MergerItem  # Deferred import
        from Splitter_Item import SplitterItem  # Deferred import

        start_parent = self.start_port.parentItem()
        end_parent = self.end_port.parentItem()

        # Logic for when the start parent is a Splitter or Merger
        if isinstance(start_parent, SplitterItem):
            # If the start is a splitter, divide the input rate across the outputs
            connected_outputs = len([conn for conn in start_parent.childItems() if isinstance(conn, ConnectionLineItem) and conn.start_port == self.start_port])
            if connected_outputs > 0:
                self.transfer_rate = start_parent.input_rate / connected_outputs if start_parent.input_rate else self.capacity
        elif isinstance(start_parent, MergerItem):
            # If the start is a merger, the output rate is the sum of the inputs
            self.transfer_rate = (
                sum(port.input_rate for port in [start_parent.input_port1, start_parent.input_port2] if port.input_rate)
                or self.capacity
            )
        else:
            # Default behavior for non-splitter/merger items
            self.transfer_rate = min(
                self.start_port.parentItem().output_rate if hasattr(self.start_port.parentItem(), 'output_rate') else self.capacity,
                self.capacity
            )

        # Logic for when the end parent is a Splitter or Merger
        if isinstance(end_parent, SplitterItem):
            # The end is a splitter, so it should take as much as its input rate allows
            if end_parent.input_rate:
                self.transfer_rate = min(self.transfer_rate, end_parent.input_rate)
        elif isinstance(end_parent, MergerItem):
            # The end is a merger, so the rate is based on its input capacity
            if end_parent.input_rate:
                self.transfer_rate = min(self.transfer_rate, end_parent.input_rate)
        else:
            # Default behavior for non-splitter/merger items
            self.transfer_rate = min(
                self.transfer_rate,
                self.end_port.parentItem().input_rate if hasattr(self.end_port.parentItem(), 'input_rate') else self.capacity,
                self.capacity
            )
        
        # Update the label displaying the transfer rate
        self.rate_label.setPlainText(self.get_label_text())

    def update_position(self):
        try:
            line = QLineF(
                self.start_port.scenePos() + self.start_port.boundingRect().center(),
                self.end_port.scenePos() + self.end_port.boundingRect().center()
            )
            self.setLine(line)
            self.update_label_position()
        except RuntimeError:
            self.remove()

    def update_label_position(self):
        mid_point = self.line().pointAt(0.5)
        self.rate_label.setPos(mid_point.x(), mid_point.y())

    def remove(self):
        # Remove this connection from ports
        if self in self.start_port.connections:
            self.start_port.connections.remove(self)
        if self in self.end_port.connections:
            self.end_port.connections.remove(self)
        # Remove from scene
        if self.scene():
            self.scene().removeItem(self.rate_label)
            self.scene().removeItem(self)

    def contextMenuEvent(self, event):
        menu = QMenu()
        edit_capacity_action = menu.addAction("Edit Capacity")
        delete_action = menu.addAction("Delete Conveyor")
        action = menu.exec_(event.screenPos())
        if action == edit_capacity_action:
            self.show_edit_window()
        elif action == delete_action:
            self.remove()

    def show_edit_window(self):
        self.edit_window = ConveyorEditWindow(self)
        self.edit_window.show()
