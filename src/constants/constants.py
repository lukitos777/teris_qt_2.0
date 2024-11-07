from enum import Enum
from math import sin, cos, radians
from typing import TypeVar

Cell = TypeVar('Cell')

class Colors(Enum):
    T: str = '#00cc99' # cayan
    S: str = '#ffc000' # yellow
    Z: str = '#92d050' # green
    J: str = '#7030a0' # purple
    L: str = '#ff66cc' # pink
    I: str = '#00b0f0' # blue
    O: str = '#ff0066' # red
    D: str = '#bdeeff' # default color for empty cell
    W: str = '#ffffff' # for background color

# dictionary with vectors and it's colors
# vectors be like => ( delta_i : delta_j )
# i -- index of row in the board & j -- index of column
shape_types = {
    'T': (((0, 0), (0, -1), (0, 1), (-1, 0)), Colors.T.value),
    'S': (((0, 0), (0, -1), (-1, 0), (-1, 1)), Colors.S.value),
    'Z': (((0, 0), (0, 1), (-1, 0), (-1, -1)), Colors.Z.value),
    'J': (((0, 0), (-1, 0), (1, 0), (1, -1)), Colors.J.value),
    'L': (((0, 0), (-1, 0), (1, 0), (1, 1)), Colors.L.value),
    'I': (((0, 0), (0, -1), (0, 1), (0, 2)), Colors.I.value),
    'O': (((0, 0), (0, 1), (-1, 0), (-1, 1)), Colors.O.value)
}

sin_90, cos_90 = sin(radians(90)), cos(radians(90))

# vectors to move shapes
# W, E, S are west, east, south vectors respectively 
W, E, S = (0, -1), (0, 1), (1, 0)


# here are functions to check collision from different sides
# we save them into a dictionary do avoid lots of 'if' statements
def check_collision_from_left(old_points: list[tuple[int, int]], new_points: list[tuple[int, int]], board: list[list[Cell]]) -> bool:
    for point in new_points:
        if point[1] < 0: return True
        if point in old_points: continue
        if board[point[0]][point[1]].is_filled: return True
    else: return False

def check_collision_from_right(old_points: list[tuple[int, int]], new_points: list[tuple[int, int]], board: list[list[Cell]]) -> bool:
    for point in new_points:
        if point[1] >= 10: return True
        if point in old_points: continue
        if board[point[0]][point[1]].is_filled: return True
    else: return False

def check_collision_below(old_points: list[tuple[int, int]], new_points: list[tuple[int, int]], board: list[list[Cell]]) -> bool:
    for point in new_points:
        if point[0] >= 20 or point[0] < 0: return True
        if point in old_points: continue
        if board[point[0]][point[1]].is_filled: return True
    else: return False
    

collision_checker_functions = {
    W: check_collision_from_left,
    E: check_collision_from_right,
    S: check_collision_below,
}

# tetris theme music path
file_name = './music/tetris_theme.mp3'