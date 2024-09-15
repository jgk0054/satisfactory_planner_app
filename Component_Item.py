from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene,
    QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem,
    QGraphicsItem, QWidget, QPushButton, QVBoxLayout, QComboBox,
    QGraphicsTextItem, QMenu, QLineEdit, QLabel, QFormLayout
)
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPointF, QLineF
from Port_Item import PortItem

class ComponentItem(QGraphicsRectItem):
    def __init__(self, width, height, name):
        super().__init__(0, 0, width, height)
        self.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemSendsGeometryChanges
        )
        self.setBrush(QBrush(QColor("lightgray")))
        self.name = name

        # Add a label to display the component's name
        self.name_label = QGraphicsTextItem(self.name, self)
        self.name_label.setDefaultTextColor(QColor("black"))
        self.name_label.setPos(width / 2 - self.name_label.boundingRect().width() / 2, -20)  # Centered above the item

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSceneChange and value is None:
            # ComponentItem is being removed from the scene
            # Remove connections of all child ports
            for child in self.childItems():
                if isinstance(child, PortItem):
                    for connection in list(child.connections):
                        connection.remove()
        elif change == QGraphicsItem.ItemPositionChange:
            # Update positions of connected lines
            for child in self.childItems():
                if isinstance(child, PortItem):
                    for connection in child.connections:
                        connection.update_position()
        return super().itemChange(change, value)

    def contextMenuEvent(self, event):
        menu = QMenu()
        delete_action = menu.addAction(f"Delete {self.name}")
        action = menu.exec_(event.screenPos())
        if action == delete_action:
            # Remove from scene (this will trigger itemChange with ItemSceneChange)
            self.scene().removeItem(self)
