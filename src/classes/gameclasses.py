from typing import Iterator, Sequence

import pygame

from classes.abstracts import Entity_1x1, EntityFreezed_1x1, Entity_1x2
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


class Pedestrians(Pedestrian):
    """Компоновщик экземпляров класса `Pedestrian`."""
    def __init__(self, pedestrians: list[Pedestrian]):
        self.pedestrians = sorted(pedestrians, key=lambda x: (x.x, x.y))
        print(self.pedestrians)
        self.cnt = -1
    
    def __iter__(self) -> Iterator[Pedestrian]:
        return self.pedestrians.__iter__()

    def _find_ped_by_coords(self, to_find: tuple[int, int]) -> int:
        src_array = self.pedestrians
        array_len = len(src_array)
        if array_len == 0:
            return -1
        
        # Linear Search
        for i in range(array_len):
            ped = src_array[i]
            if ped.x == to_find[0] and ped.y == to_find[1]:
                return i

    def make_step(self, x: int, y: int) -> None:
        """Wrapper for `ped.move()` method."""
        self.cnt += 1
        if self.cnt >= self.fps:
            for ped in self.pedestrians:
                ped.move_ip(ped.movement_x, ped.movement_y)
            self.cnt = -1
    
    def reset(self) -> None:
        for ped in self.pedestrians:
            ped.reset()
    
    def tolist(self) -> list[Pedestrian]:
        return self.pedestrians
    
    def remove(self, x: int, y: int) -> None:
        """Removes pedestrian with coordinates (x, y)."""
        print('FUCK!')
        ind = self._find_ped_by_coords((x, y))
        print(x, y, ind)
        self.pedestrians.pop(ind)

    def render(self) -> None:
        for ped in self.pedestrians:
            ped.render()


class Car(Entity_1x2):
    def __init__(self, x: int, y: int, movement_x: int, movement_y: int) -> None:
        self.cnt = -1
        super().__init__(x, y, movement_x, movement_y)

    @classmethod
    def set_fps(cls, fps: int) -> None:
        cls.fps = fps


class Cars(Car):
    def __init__(self, cars: Sequence[Car]):
        self.cars = cars
        self.cnt = -1

    def go(self) -> None:
        """Wrapper for `car.move()` method."""
        self.cnt += 5
        if self.cnt >= self.fps:
            for car in self.cars:
                car.move_ip(car.movement_x, car.movement_y)
            self.cnt = -1

    def __iter__(self) -> Iterator[Car]:
        return self.cars.__iter__()
    
    def tolist(self) -> list[Car]:
        return list(self.cars)
    
    def reset(self) -> None:
        for car in self.cars:
            car.reset()

    def render(self) -> None:
        for car in self.cars:
            car.render()


class PhysicalObject(EntityFreezed_1x1):
    """Класс, создающий объекты с коллизией."""
    pass


class TactileTile(PhysicalObject):
    """Класс, создающий тактильные поверхности."""
    pass


class TactileTiles(TactileTile):
    def __init__(self, tiles: Sequence[TactileTile]) -> None:
        self.tiles = tiles
        
    def tolist(self) -> list[TactileTile]:
        return list(self.tiles)
    
    def __iter__(self) -> Iterator[TactileTile]:
        return self.tiles.__iter__()
    
    def render(self) -> None:
        for tile in self.tiles:
            tile.render()


class HospitalTile(EntityFreezed_1x1):
    """Класс, создающий клетки больницы (цели игрока)."""
    pass


class HospitalTiles(HospitalTile):
    def __init__(self, tiles: Sequence[HospitalTile]) -> None:
        self.tiles = tiles
        
    def tolist(self) -> list[HospitalTile]:
        return list(self.tiles)
    
    def __iter__(self) -> Iterator[HospitalTile]:
        return self.tiles.__iter__()
    
    def render(self) -> None:
        for tile in self.tiles:
            tile.render()


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
    
    def render(self) -> None:
        for object_ in self.objects:
            object_.render()


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