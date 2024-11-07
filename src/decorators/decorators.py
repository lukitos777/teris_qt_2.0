from functools import wraps
from typing import TypeVar
from copy import deepcopy

Function = TypeVar('Function')


def movement_decorator(vect: tuple[int, int]):
    def wrapper(func: Function):
        @wraps(func)
        def inner(self):
            old_points = deepcopy(self.current_shape.points)

            new_points = [(vect[0] + point[0], vect[1] + point[1]) for point in old_points]

            if (res := self.collision_checker(vect, old_points, new_points)) and (vect == (1, 0)): 
                self.level_checker()
                self.generate_shape() 
                return
            if res: return

            self.current_shape.points = new_points
            self.draw_shape(self.current_shape, old_points)

            return func(self)
        return inner
    return wrapper