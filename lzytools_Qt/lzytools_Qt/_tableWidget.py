from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHeaderView, QTableWidget, QTableWidgetItem


class TableWidgetHiddenOverLengthText(QTableWidget):
    """自动隐藏长文本的文本框控件，支持拉伸（abcd->a...）
    利用 tableWidget 的文本单元格自动隐藏长文本的特性
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.setColumnCount(1)
        self.insertRow(0)
        self.setFixedHeight(18)
        self.setRowHeight(0, 16)
        self.item_filename = QTableWidgetItem('')
        self.setItem(0, 0, self.item_filename)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setStyleSheet("""
            QTableWidget {
                border: 0px;
                background: transparent;
                gridline-color: transparent;
                selection-background-color: transparent;
            }

            QTableWidget::item {
                border: 0px;
                padding: 0px;
            }

            QHeaderView::section {
                border: 0px;
                background: transparent;
                padding: 0px;
            }
        """)

    def set_text(self, text: str):
        """设置文本"""
        self.item_filename.setText(text)

    def set_height(self, height: int):
        """设置控件高度
        :param height: int，高度"""
        self.setFixedHeight(height)
        self.setRowHeight(0, max(0, height - 2))
