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
from Miner_Item import MinerItem
from Smelter_Item import SmelterItem
from Splitter_Item import SplitterItem
from Merger_Item import MergerItem





class GraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setRenderHints(self.renderHints())
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.zoom_factor = 1.15
        self.setAcceptDrops(True)
        self.temp_line = None
        self.drawing_line = False
        self.start_port = None

    def wheelEvent(self, event):
        zoom_in_factor = self.zoom_factor
        zoom_out_factor = 1 / self.zoom_factor

        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor

        self.scale(zoom_factor, zoom_factor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            item = self.itemAt(event.pos())
            if isinstance(item, PortItem):
                self.start_port = item
                self.drawing_line = True
                self.temp_line = QGraphicsLineItem()
                self.temp_line.setPen(QPen(QColor("gray"), 2, Qt.DashLine))
                start_pos = self.start_port.scenePos() + self.start_port.boundingRect().center()
                self.temp_line.setLine(QLineF(start_pos, start_pos))
                self.scene().addItem(self.temp_line)
            else:
                super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.drawing_line and self.temp_line:
            start_pos = self.start_port.scenePos() + self.start_port.boundingRect().center()
            current_pos = self.mapToScene(event.pos())
            self.temp_line.setLine(QLineF(start_pos, current_pos))
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.drawing_line and event.button() == Qt.LeftButton:
            item = self.itemAt(event.pos())
            if isinstance(item, PortItem) and self.start_port:
                end_port = item
                connection = ConnectionLineItem(self.start_port, end_port)
                self.scene().addItem(connection)
            elif self.temp_line:
                self.scene().removeItem(self.temp_line)
                self.temp_line = None
            self.drawing_line = False
        super().mouseReleaseEvent(event)

    def is_valid_connection(self, start_port, end_port):
        # Ensure that we are connecting from an output to an input
        if start_port.port_type == 'output' and end_port.port_type == 'input':
            return True
        return False

    def contextMenuEvent(self, event):
        item = self.itemAt(event.pos())
        if item is None:
            # Right-clicked on empty space
            menu = QMenu()
            add_miner_action = menu.addAction("Add Miner")
            add_smelter_action = menu.addAction("Add Smelter")
            add_splitter_action = menu.addAction("Add Splitter")
            add_merger_action = menu.addAction("Add Merger")
            action = menu.exec_(event.globalPos())
            position = self.mapToScene(event.pos())
            if action == add_miner_action:
                miner = MinerItem()
                self.scene().addItem(miner)
                miner.setPos(position)
            elif action == add_smelter_action:
                smelter = SmelterItem()
                self.scene().addItem(smelter)
                smelter.setPos(position)
            elif action == add_splitter_action:
                splitter = SplitterItem()
                self.scene().addItem(splitter)
                splitter.setPos(position)
            elif action == add_merger_action:
                merger = MergerItem()
                self.scene().addItem(merger)
                merger.setPos(position)
        else:
            super().contextMenuEvent(event)

    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setRenderHints(self.renderHints())
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.zoom_factor = 1.15
        self.setAcceptDrops(True)
        self.temp_line = None
        self.drawing_line = False
        self.start_port = None

    def wheelEvent(self, event):
        zoom_in_factor = self.zoom_factor
        zoom_out_factor = 1 / self.zoom_factor

        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor

        self.scale(zoom_factor, zoom_factor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            item = self.itemAt(event.pos())
            if isinstance(item, PortItem):
                self.start_port = item
                self.drawing_line = True
                self.temp_line = QGraphicsLineItem()
                self.temp_line.setPen(QPen(QColor("gray"), 2, Qt.DashLine))
                start_pos = self.start_port.scenePos() + self.start_port.boundingRect().center()
                self.temp_line.setLine(QLineF(start_pos, start_pos))
                self.scene().addItem(self.temp_line)
            else:
                super().mousePressEvent(event)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.drawing_line and self.temp_line:
            start_pos = self.start_port.scenePos() + self.start_port.boundingRect().center()
            current_pos = self.mapToScene(event.pos())
            self.temp_line.setLine(QLineF(start_pos, current_pos))
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.drawing_line:
            items_under_mouse = self.items(event.pos())
            end_port = None
            for item in items_under_mouse:
                if isinstance(item, PortItem):
                    end_port = item
                    break

            if isinstance(end_port, PortItem) and self.is_valid_connection(self.start_port, end_port):
                connection = ConnectionLineItem(self.start_port, end_port)
                self.scene().addItem(connection)
            self.scene().removeItem(self.temp_line)
            self.temp_line = None
            self.drawing_line = False
            self.start_port = None
        else:
            super().mouseReleaseEvent(event)

    def is_valid_connection(self, start_port, end_port):
        # Ensure that we are connecting from an output to an input
        if start_port.port_type == 'output' and end_port.port_type == 'input':
            return True
        return False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Satisfactory Planner")
        self.setGeometry(100, 100, 800, 600)

        self.scene = QGraphicsScene()
        self.view = GraphicsView(self.scene)
        self.setCentralWidget(self.view)

        # # Create a miner item
        # miner = MinerItem(100, 50)
        # self.scene.addItem(miner)
        # miner.setPos(0, 0)

        # # Create a smelter item
        # smelter = SmelterItem(100, 50)
        # self.scene.addItem(smelter)
        # smelter.setPos(200, 0)

        # # Create example connection
        # connection1 = ConnectionLineItem(miner.output_port, smelter.input_port)
        # self.scene.addItem(connection1)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            # Delete selected items
            for item in self.scene.selectedItems():
                if isinstance(item, ComponentItem):
                    self.scene.removeItem(item)
                elif isinstance(item, ConnectionLineItem):
                    item.remove()
        else:
            super().keyPressEvent(event)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            # Delete selected items
            for item in self.scene.selectedItems():
                if isinstance(item, ComponentItem):
                    self.scene.removeItem(item)
                elif isinstance(item, ConnectionLineItem):
                    item.remove()
        else:
            super().keyPressEvent(event)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
