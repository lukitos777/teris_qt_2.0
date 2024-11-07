from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLabel, QMessageBox
)

from PyQt6.QtCore import QSize, Qt, QTimer, QUrl
from PyQt6.QtGui import QFont
from pygame import mixer

from sys import argv
from random import choice
from copy import deepcopy

from settings.settings import *
from constants.constants import *
from classes.cell import Cell
from classes.shape import Shape
from decorators.decorators import *


class Tetris(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.init_UI()
        self.generate_shape()

    def init_UI(self) -> None:
        self.setWindowTitle('Tetris QT')
        self.alpha : int = 1 # coeficient to calculate game speed
        self.removed_levels_counter: int = 0 # to calculate game speed

        # Here we save the cells of the grid and change it's state in game process
        self.board = [[Cell() for i in range(width)] for j in range(height)]

        central_widget = QWidget()
        main_layout = QVBoxLayout()

        grid = QGridLayout()
        grid_widget = QWidget()

        for i in range(height):
            for j in range(width):
                grid.addWidget(self.board[i][j], i, j)
        
        grid.setSpacing(1)
        grid.setContentsMargins(5, 5, 5, 5)

        grid_widget.setLayout(grid)

        self.counter = QLabel()
        self.counter.setText('0')

        self.counter.setFixedSize(QSize(449, 22))
        self.counter.setFont(QFont('Consolas', 12))
        self.counter.setContentsMargins(5, 2, 0, 0)
        self.counter.setStyleSheet('color: #000000;')
        self.counter.setAlignment(Qt.AlignmentFlag.AlignRight)

        main_layout.addWidget(self.counter)
        main_layout.addWidget(grid_widget)

        central_widget.setLayout(main_layout)

        central_widget.setAutoFillBackground(True)
        central_widget.setStyleSheet(f'background-color: {Colors.W.value};')

        self.setCentralWidget(central_widget)

        self.play_music()

        self.player = QTimer(self)
        self.player.setInterval(83011)

        self.player.timeout.connect(self.play_music)

        self.player.start()

        self.timer = QTimer(self)
        self.timer.setInterval(fall_speed(self.alpha))

        self.timer.timeout.connect(self.shift_shape_below)
        
        self.timer.start()

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_S:
            self.shift_shape_below()
        elif event.key() == Qt.Key.Key_A:
            self.shift_shape_left()
        elif event.key() == Qt.Key.Key_D:
            self.shift_shape_right()
        elif event.key() == Qt.Key.Key_W:
            self.rotate_shape()

    def generate_shape(self) -> None:
        key = choice(list(shape_types.keys()))

        vectors, color = shape_types[key]

        points = ( # moving spawn point using vectors
            (start_point[0] + vectors[0][0], start_point[1] + vectors[0][1]),
            (start_point[0] + vectors[1][0], start_point[1] + vectors[1][1]),
            (start_point[0] + vectors[2][0], start_point[1] + vectors[2][1]),
            (start_point[0] + vectors[3][0], start_point[1] + vectors[3][1])
        )

        for point in points:
            if self.board[point[0]][point[1]].is_filled:
                self.show_game_over_dialog()
                return
            
        self.current_shape = Shape(color, points)

        self.draw_shape(self.current_shape, points)

    # we get old points and new points of the shape, which we just moved
    # we look for points which belong to the set => old_points \ new_points
    # and then colorize empty cells by default color
    # finally colorize new points with moved shape's color
    def draw_shape(self, shape: Shape, old_points: list[tuple[int, int]]) -> None:
        for point in old_points:
            if point not in shape.points:
                self.board[point[0]][point[1]].is_filled = False
                self.board[point[0]][point[1]].fill()

        for point in shape.points:
            self.board[point[0]][point[1]].is_filled = True
            self.board[point[0]][point[1]].fill(shape.color)

    @movement_decorator(S)
    def shift_shape_below(self) -> None: ...

    @movement_decorator(W)
    def shift_shape_left(self) -> None: ...

    @movement_decorator(E)
    def shift_shape_right(self) -> None: ...
        
    def rotate_shape(self) -> None:
        if self.current_shape.color == Colors.O.value:
            return
        else:
            points = deepcopy(self.current_shape.points)

            if self.current_shape.color == Colors.I.value:
                for point in points:
                    if point[0] - 1 <= 0:
                        return

            for point in points:
                if point[1] == 0 or point[1] == width - 1: return

            pivot = points[0]

            rotated_points = [pivot] + [(
                int((point[0] - pivot[0]) * cos_90 - (point[1] - pivot[1]) * sin_90 + pivot[0]),
                int((point[0] - pivot[0]) * sin_90 + (point[1] + pivot[1]) * cos_90 + pivot[1])) \
                for point in points[1:]
            ]

            for point in rotated_points:
                if point in points: continue
                if self.board[point[0]][point[1]].is_filled: return

            self.current_shape.points = rotated_points
            self.draw_shape(self.current_shape, points)

    # here we are calling the checker functions to check collisions in different directions
    def collision_checker(self, vect: tuple[int, int], old_points: tuple[tuple[int, int]], new_points: tuple[tuple[int, int]]) -> bool:
        return collision_checker_functions[vect](old_points, new_points, self.board)
                
    def show_game_over_dialog(self) -> None:
        msg = QMessageBox()

        msg.setText('Would you like to try again ?')
        msg.setWindowTitle('Game Over')

        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        response = msg.exec()

        if response == QMessageBox.StandardButton.Yes:
            self.restart_game()
        else:
            QApplication.quit()

    def restart_game(self) -> None:
        self.init_UI()
        self.generate_shape()

    # we getting all i-s of the current shape and then 
    # check if all cell are filled on the i-th row
    # finnaly we calling remove levels
    def level_checker(self) -> None:
        levels = [point[0] for point in self.current_shape.points]
        filtered_levels = list(set(filter(lambda x: all([self.board[x][i].is_filled for i in range(width)]), levels)))
        self.remove_levels(filtered_levels)

    # here we just change the atribute is_filled of each cell 
    # of the row, which was filled in the grid
    # finnaly we colorze each cell with default color
    def remove_levels(self, levels: list[int]) -> None:
        if not levels: return
        for level in levels:
            for ind in range(width):
                self.board[level][ind].is_filled = False
                self.board[level][ind].fill()
            self.removed_levels_counter += 1
        self.increment_score(len(levels))
        self.shift_levels(len(levels), min(levels) - 1)

    # we starting from the level_from-th row to the end of the grid and
    # shift each cell which is filled by number of the combos below
    def shift_levels(self, combo: int, level_from: int) -> None:
        for i in range(level_from, -1, -1):
            for j in range(width):
                if self.board[i][j].is_filled:
                    color = self.board[i][j].color

                    self.board[i][j].is_filled = False
                    self.board[i][j].fill()

                    self.board[i + combo][j].is_filled = True
                    self.board[i + combo][j].fill(color)

    def increment_score(self, combo: int) -> None:
        new_score = int(self.counter.text()) + riser(combo)

        if 0 <= new_score < 100: self.alpha = 1
        elif 100 <= new_score < 150: self.alpha = 2
        elif 150 <= new_score < 200: self.alpha = 3
        elif 200 <= new_score < 255: self.alpha = 4
        elif 255 <= new_score < 300: self.alpha = 5
        elif 300 <= new_score < 355: self.alpha = 6
        elif 355 <= new_score < 405: self.alpha = 7
        elif 405 <= new_score < 1577: self.alpha = 8
        else: self.alpha = 9 # super speed

        self.timer.setInterval(fall_speed(self.alpha))
        self.counter.setText(str(new_score))

    def play_music(self) -> None:
        mixer.init()
        mixer.music.load(file_name)
        mixer.music.play()


def main(*args, **kwargs) -> None:
    app = QApplication(argv)
    tetris = Tetris()
    tetris.show()
    app.exec()

if __name__ == '__main__':
     main()
