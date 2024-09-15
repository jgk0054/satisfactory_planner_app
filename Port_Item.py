import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene,
    QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem,
    QGraphicsItem, QWidget, QPushButton, QVBoxLayout, QComboBox,
    QGraphicsTextItem, QMenu, QLineEdit, QLabel, QFormLayout
)
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPointF, QLineF


class PortItem(QGraphicsEllipseItem):
    def __init__(self, x, y, width, height, port_type='output', parent=None):
        super().__init__(x, y, width, height)
        self.port_type = port_type  # 'input' or 'output'
        self.setBrush(QBrush(QColor("blue") if self.port_type == 'input' else QColor("green")))
        self.connections = []
        self.setAcceptHoverEvents(True)
        self.hovered = False
        self.parent = parent
        
        if isinstance(parent, QGraphicsItem):
            self.setParentItem(parent)
            # Do not allow independent movement if it's attached to a parent
            self.setFlags(
                QGraphicsItem.ItemIsSelectable |
                QGraphicsItem.ItemSendsGeometryChanges
            )
        else:
            # Allow movement if it's not attached to a parent
            self.setFlags(
                QGraphicsItem.ItemIsMovable |
                QGraphicsItem.ItemIsSelectable |
                QGraphicsItem.ItemSendsGeometryChanges
            )

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSceneChange and value is None:
            # PortItem is being removed from the scene
            # Remove all its connections
            for connection in list(self.connections):
                connection.remove()
        elif change == QGraphicsItem.ItemPositionChange:
            for connection in self.connections:
                connection.update_position()
        return super().itemChange(change, value)

    def hoverEnterEvent(self, event):
        self.hovered = True
        self.update()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.hovered = False
        self.update()
        super().hoverLeaveEvent(event)

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        if self.hovered:
            pen = QPen(QColor("red"), 2)
            painter.setPen(pen)
            painter.drawEllipse(self.rect())

    def contextMenuEvent(self, event):
        menu = QMenu()
        delete_action = menu.addAction("Delete Connections")
        action = menu.exec_(event.screenPos())
        if action == delete_action:
            for connection in list(self.connections):
                connection.remove()
