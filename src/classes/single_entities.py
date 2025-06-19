from typing import Sequence

import pygame

from classes.base_entities import Entity_1x1, EntityFreezed_1x1, Entity_1x2
from config.cfg_reader import CELL_SIZE


class Pedestrian(Entity_1x1):
    """
    Противник игрока. При столкновении с ним отталкивает.

    Args:
        x (int): Первая координата спавна
        y (int): Вторая коодината спавна
        movement_x (int): Координата перемещения по X
        movement_y (int): Координата перемещения по Y
    """
    def __init__(self, x: int, y: int, movement_x: int, movement_y: int) -> None:
        self.cnt = -1
        super().__init__(x, y, movement_x, movement_y,)


class StaticPedestrian(Pedestrian):
    def __init__(self, x: int, y: int) -> None:
        self.cnt = -1
        super().__init__(x, y, 0, 0)


class Car(Entity_1x2):
    def __init__(self, x: int, y: int, movement_x: int, movement_y: int) -> None:
        self.cnt = -1
        super().__init__(x, y, movement_x, movement_y)

    @classmethod
    def set_fps(cls, fps: int) -> None:
        cls.fps = fps


class Wall(EntityFreezed_1x1):
    """Класс, создающий объекты с коллизией."""
    pass


class TactileTile(EntityFreezed_1x1):
    """Класс, создающий тактильные поверхности."""
    pass


class HospitalTile(EntityFreezed_1x1):
    """Класс, создающий клетки больницы (цели игрока)."""
    pass


class BlindPerson(Entity_1x1):
    def __init__(self, x: int, y: int) -> None:
        self.is_alive: bool = True
        self.is_on_tactile: bool = False
        self.is_won: bool = False
        super().__init__(x, y, CELL_SIZE, CELL_SIZE)

    def hits_object(self, x: int, y: int) -> bool:
        return super().colliderect(x, y, CELL_SIZE, CELL_SIZE)
    
    def hits_objectlist(self, walls: Sequence[pygame.Rect]) -> bool:
        is_collide = super().collidelist(walls)
        return False if is_collide == -1 else True
