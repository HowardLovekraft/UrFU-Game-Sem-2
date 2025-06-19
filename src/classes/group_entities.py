from typing import Iterator, Sequence

import pygame

from classes.base_entities import EntityCluster, EntityFreezed
from classes.single_entities import Car, HospitalTile, Pedestrian, Wall
from classes.single_entities import TactileTile, StaticPedestrian, BlindPerson
from config.cfg_reader import CELL_SIZE


class Pedestrians(Pedestrian):
    """Компоновщик экземпляров класса `Pedestrian`."""
    def __init__(self, pedestrians: list[Pedestrian]):
        self.pedestrians = sorted(pedestrians, key=lambda x: (x.x, x.y))
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

    def make_move(self) -> None:
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
        ind = self._find_ped_by_coords((x, y))
        self.pedestrians.pop(ind)

    def render(self) -> None:
        for ped in self.pedestrians:
            ped.render()


class StaticPedestrians(StaticPedestrian):
    def __init__(self, parameters: list[tuple[int, int]]):
        pedestrians = [StaticPedestrian(*param) for param in parameters]
        self.pedestrians = sorted(pedestrians, key=lambda x: (x.x, x.y))
        self.cnt = -1
    
    def __iter__(self) -> Iterator[StaticPedestrian]:
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
    
    def tolist(self) -> list[StaticPedestrian]:
        return self.pedestrians
    
    def remove(self, x: int, y: int) -> None:
        """Removes pedestrian with coordinates (x, y)."""
        ind = self._find_ped_by_coords((x, y))
        self.pedestrians.pop(ind)

    def render(self) -> None:
        for ped in self.pedestrians:
            ped.render()


class Cars(Car):
    def __init__(self, cars: Sequence[Car]):
        self.cars = cars
        self.cnt = -1

    def make_move(self) -> None:
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


class WallCluster(Wall):
    def __init__(self, *coords: tuple[int, int]):
        self.objects: tuple[Wall, ...] = tuple(
            Wall(x, y) for (x, y) in coords
        )
        self.upped: tuple[Wall, ...] = tuple(
            Wall(x, y+CELL_SIZE) for (x, y) in coords
        )
        self.lefted: tuple[Wall, ...] = tuple(
            Wall(x+CELL_SIZE, y) for (x, y) in coords
        )
        self.righted: tuple[Wall, ...] = tuple(
            Wall(x-CELL_SIZE, y) for (x, y) in coords
        )
        self.downed: tuple[Wall, ...] = tuple(
            Wall(x, y-CELL_SIZE) for (x, y) in coords
        )

    def __iter__(self) -> Iterator[Wall]:
        return self.objects.__iter__()

    def tolist(self) -> list[Wall]:
        return list(self.objects)
    
    def render(self) -> None:
        for object_ in self.objects:
            object_.render()


class ObjectsRenderer(EntityCluster):
    def __init__(self, entities: Sequence[EntityFreezed] = []):
        super().__init__(entities)
    
    def render(self, player: BlindPerson) -> None:
        coords_to_render = tuple(
            (player.x+x*CELL_SIZE, player.y+y*CELL_SIZE) 
            for x in (-3, -2, -1, 0, 1, 2, 3) for y in (-3, -2, -1, 0, 1, 2, 3)
        )
        entities_to_render = [
            entity for entity in self.entities if (entity.x, entity.y) in coords_to_render
        ]
        for entity in entities_to_render:
            entity.render()
        player.render()