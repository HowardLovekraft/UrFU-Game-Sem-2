import pygame

from config.cfg_reader import CELL_SIZE


class EntityFreezed_1x1(pygame.Rect):
    def __init__(self, x: int, y: int) -> None:
        self.init_x = x
        self.init_y = y
        super().__init__(x, y, CELL_SIZE, CELL_SIZE)


class Entity_1x1(EntityFreezed_1x1):
    def __init__(self, x: int, y: int, movement_x: int, movement_y: int) -> None:
        super().__init__(x, y)
        self.movement_x = movement_x
        self.movement_y = movement_y

    def reset(self) -> None:
        self.update(self.init_x, self.init_y, CELL_SIZE, CELL_SIZE)


class Entity_1x2(pygame.Rect):
    def __init__(self, x: int, y: int) -> None:
        self.init_x = x
        self.init_y = y
        super().__init__(x, y, CELL_SIZE, 2*CELL_SIZE)

    def reset(self) -> None:
        self.update(self.init_x, self.init_y, CELL_SIZE, 2*CELL_SIZE)