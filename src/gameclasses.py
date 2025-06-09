from enum import Enum
from typing import Iterator, Sequence

import pygame

from config_reader import CELL_SIZE


class Entity_1x1(pygame.Rect):
    def __init__(self, x: int, y: int) -> None:
        self.init_x = x
        self.init_y = y
        super().__init__(x, y, CELL_SIZE, CELL_SIZE)

    def reset(self) -> None:
        self.update(self.init_x, self.init_y, CELL_SIZE, CELL_SIZE)


class Entity_1x2(pygame.Rect):
    def __init__(self, x: int, y: int) -> None:
        self.init_x = x
        self.init_y = y
        super().__init__(x, y, CELL_SIZE, 2*CELL_SIZE)

    def reset(self) -> None:
        self.update(self.init_x, self.init_y, CELL_SIZE, 2*CELL_SIZE)


class Pedestrian(Entity_1x1):
    def __init__(self, x: int, y: int) -> None:
        self.cnt = -1
        super().__init__(x, y)
        try:
            self.__getattribute__('fps')
        except AttributeError:
            raise Exception("You didn't set field 'fps' for Pedestrians!")

    @classmethod
    def set_fps(cls, fps: int) -> None:
        cls.fps = fps

    def reset(self) -> None:
        self.update(self.init_x, self.init_y, CELL_SIZE, CELL_SIZE)


class Pedestrians(Pedestrian):
    def __init__(self, pedestrians: Sequence[Pedestrian]):
        self.pedestrians = pedestrians
        self.cnt = -1
        try:
            self.fps = pedestrians[0].__getattribute__('fps')
        except AttributeError:
            raise Exception("You didn't set field 'fps' for Pedestrians!")

    def make_step(self, x: int, y: int) -> None:
        """Wrapper for `ped.move()` method."""
        self.cnt += 1
        if self.cnt >= self.fps:
            for ped in self.pedestrians:
                ped.move_ip(x, y)
            self.cnt = -1

    def __iter__(self) -> Iterator[Pedestrian]:
        return self.pedestrians.__iter__()
    
    def tolist(self) -> list[Pedestrian]:
        return list(self.pedestrians)


class Car(Entity_1x2):
    def __init__(self, x: int, y: int) -> None:
        self.cnt = -1
        super().__init__(x, y)
        try:
            self.__getattribute__('fps')
        except AttributeError:
            raise Exception("You didn't set field 'fps' for Cars!")

    @classmethod
    def set_fps(cls, fps: int) -> None:
        cls.fps = fps


class Cars(Car):
    def __init__(self, cars: Sequence[Car]):
        self.cars = cars
        self.cnt = -1
        try:
            self.fps = cars[0].__getattribute__('fps')
        except AttributeError:
            raise Exception("You didn't set field 'fps' for Cars!")

    def go(self, x: int, y: int) -> None:
        """Wrapper for `car.move()` method."""
        self.cnt += 4
        if self.cnt >= self.fps:
            for car in self.cars:
                car.move_ip(x, y)
            self.cnt = -1

    def __iter__(self) -> Iterator[Car]:
        return self.cars.__iter__()
    
    def tolist(self) -> list[Car]:
        return list(self.cars)



class PhysicalObject(pygame.Rect):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, CELL_SIZE, CELL_SIZE)


class PhysObjectCluster(PhysicalObject):
    def __init__(self, *coords: tuple[int, int]):
        self.objects: tuple[PhysicalObject, ...] = tuple(
            PhysicalObject(x, y) for (x, y) in coords
        )
        self.upped: tuple[PhysicalObject, ...] = tuple(
            PhysicalObject(x, y+CELL_SIZE) for (x, y) in coords
        )
        self.lefted: tuple[PhysicalObject, ...] = tuple(
            PhysicalObject(x+CELL_SIZE, y) for (x, y) in coords
        )
        self.righted: tuple[PhysicalObject, ...] = tuple(
            PhysicalObject(x-CELL_SIZE, y) for (x, y) in coords
        )
        self.downed: tuple[PhysicalObject, ...] = tuple(
            PhysicalObject(x, y-CELL_SIZE) for (x, y) in coords
        )

    def __iter__(self) -> Iterator[PhysicalObject]:
        return self.objects.__iter__()


class BlindPerson(pygame.Rect):
    def __init__(self, x: int, y: int) -> None:
        self.is_alive = True
        super().__init__(x, y, CELL_SIZE, CELL_SIZE)

    def hits_object(self, x: int, y: int) -> bool:
        return super().colliderect(x, y, CELL_SIZE, CELL_SIZE)
    
    def hits_objectlist(self, walls: Sequence[pygame.Rect]) -> bool:
        is_collide = super().collidelist(walls)
        return False if is_collide == -1 else True
    

class Color(Enum):  # Enum[tuple[int, int, int]]
    WHITE = (254, 255, 255)
    BLACK = (0, 0, 0)
    RED = (254, 0, 0)
    GREEN = (0, 255, 0)
    LIGHT_RED = (254, 100, 100)