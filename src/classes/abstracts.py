from enum import Enum

import pygame

from config.cfg_reader import CELL_SIZE


class Color(Enum):  # Enum[tuple[int, int, int]]
    WHITE = (254, 255, 255)
    BLACK = (0, 0, 0)
    RED = (254, 0, 0)
    GREEN = (0, 255, 0)
    LIGHT_RED = (254, 100, 100)
    YELLOW = (255, 222, 33)


class EntityFreezed(pygame.Rect):
    """
    Базовый класс для статичных объектов.
    Требует заранее заданных значений аттрибутов `color` и `surface`.

    Args:
        x (int): Первая координата спавна объекта
        y (int): Вторая коодината спавна объекта
        size_x (int): Размер объекта по X
        size_y (int): Размер объекта по Y
    """
    def __init__(self, x: int, y: int, size_x: int, size_y: int) -> None:
        self.init_x = x
        self.init_y = y
        self.size_x = size_x
        self.size_y = size_y
        try:
            self.__getattribute__('color')
            self.__getattribute__('surface')
        except AttributeError:
            raise RuntimeError("Didn't set 'color' and/or 'surface' attributes!")
        super().__init__(x, y, size_x, size_y)

    @classmethod
    def set_color(cls, color: Color) -> None:
        cls.color = color

    @classmethod
    def set_surface(cls, surface: pygame.Surface) -> None:
        cls.surface = surface

    def render(self) -> None:
        """Отрисовывает объект на экран."""
        pygame.draw.rect(self.surface, self.color.value, self)


class Entity(EntityFreezed):
    def __init__(self, x: int, y: int, size_x: int, size_y: int, movement_x: int, movement_y: int) -> None:
        super().__init__(x, y, size_x, size_y)
        self.movement_x = movement_x
        self.movement_y = movement_y
        try:
            self.__getattribute__('fps')
        except AttributeError:
            raise RuntimeError("Didn't set 'fps' attribute!")
        
    @classmethod
    def set_fps(cls, fps: int) -> None:
        cls.fps = fps

    def reset(self) -> None:
        self.update(self.init_x, self.init_y, self.size_x, self.size_y)


class EntityFreezed_1x1(EntityFreezed):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, CELL_SIZE, CELL_SIZE)


class Entity_1x1(Entity):
    def __init__(self, x: int, y: int, movement_x: int, movement_y: int) -> None:
        super().__init__(x, y, CELL_SIZE, CELL_SIZE, movement_x, movement_y)
        self.movement_x = movement_x
        self.movement_y = movement_y


class Entity_1x2(Entity):
    def __init__(self, x: int, y: int, movement_x: int, movement_y: int) -> None:
        super().__init__(x, y, CELL_SIZE, 2*CELL_SIZE, movement_x, movement_y)