from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize

from settings.settings import stylesheet_for_cell
from constants.constants import Colors

# this class is the cell of the grid, where will be placed shapes
class Cell(QPushButton):
    def __init__(self) -> None:
        super().__init__()
        self.setFixedSize(QSize(44, 44))
        self.setDisabled(True)
        self.is_filled = False
        self.fill()

    def fill(self, color: str = '') -> None:
        fill_ = color if self.is_filled else Colors.D.value
        self.color = fill_
        self.setStyleSheet(stylesheet_for_cell.replace('_____', fill_))