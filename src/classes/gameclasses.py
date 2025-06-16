from enum import Enum
from typing import Iterator, Sequence

import pygame

from classes.abstracts import Entity_1x1, EntityFreezed_1x1, Entity_1x2
from config.cfg_reader import CELL_SIZE

    
class Color(Enum):  # Enum[tuple[int, int, int]]
    WHITE = (254, 255, 255)
    BLACK = (0, 0, 0)
    RED = (254, 0, 0)
    GREEN = (0, 255, 0)
    LIGHT_RED = (254, 100, 100)
    YELLOW = (255, 222, 33)


class Pedestrian(Entity_1x1):
    def __init__(self, x: int, y: int, movement_x: int, movement_y: int) -> None:
        self.cnt = -1
        super().__init__(x, y, movement_x, movement_y)
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
    def __init__(self, pedestrians: list[Pedestrian]):
        self.pedestrians = sorted(pedestrians, key=lambda x: (x.x, x.y))
        print(self.pedestrians)
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
                ped.move_ip(ped.movement_x, ped.movement_y)
            self.cnt = -1

    def __iter__(self) -> Iterator[Pedestrian]:
        return self.pedestrians.__iter__()
    
    def tolist(self) -> list[Pedestrian]:
        return self.pedestrians
    
    def _find_ped_by_coords(self, to_find: tuple[int, int]) -> int:
        src_array = self.pedestrians
        array_len = len(src_array)
        if array_len == 0:
            return -1
        
        for i in range(array_len):
            ped = src_array[i]
            if ped.x == to_find[0] and ped.y == to_find[1]:
                return i
    
    
    def remove(self, x: int, y: int) -> None:
        """Removes pedestrian with coordinates (x, y)."""
        print('FUCK!')
        ind = self._find_ped_by_coords((x, y))
        print(x, y, ind)
        self.pedestrians.pop(ind)

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
        self.cnt += 5
        if self.cnt >= self.fps:
            for car in self.cars:
                car.move_ip(x, y)
            self.cnt = -1

    def __iter__(self) -> Iterator[Car]:
        return self.cars.__iter__()
    
    def tolist(self) -> list[Car]:
        return list(self.cars)


class PhysicalObject(EntityFreezed_1x1):
    pass


class TactileTile(PhysicalObject):
    pass

class TactileTiles(TactileTile):
    def __init__(self, tiles: Sequence[TactileTile]) -> None:
        self.tiles = tiles
        
    def tolist(self) -> list[TactileTile]:
        return list(self.tiles)
    
    def __iter__(self) -> Iterator[TactileTile]:
        return self.tiles.__iter__()


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

    def tolist(self) -> list[PhysicalObject]:
        return list(self.objects)

    def __iter__(self) -> Iterator[PhysicalObject]:
        return self.objects.__iter__()


class BlindPerson(Entity_1x1):
    def __init__(self, x: int, y: int) -> None:
        self.is_alive: bool = True
        self.is_on_tactile: bool = False
        super().__init__(x, y, CELL_SIZE, CELL_SIZE)

    def hits_object(self, x: int, y: int) -> bool:
        return super().colliderect(x, y, CELL_SIZE, CELL_SIZE)
    
    def hits_objectlist(self, walls: Sequence[pygame.Rect]) -> bool:
        is_collide = super().collidelist(walls)
        return False if is_collide == -1 else True
