from dataclasses import dataclass
from enum import Enum
import random
import sys
from typing import Final

from icecream import ic
import pygame


@dataclass(frozen=True, slots=True)
class Display:
    x: int
    y: int
    fps: int


@dataclass(frozen=True, slots=True)
class NoOutOfBoundsChecks:
    """
    Container for results of out-of-bounds checks.
    """
    x_pos: bool
    x_neg: bool
    y_pos: bool
    y_neg: bool

    def generally(self) -> bool:
        return self.x_pos and self.x_neg and self.y_pos and self.y_neg


class Pedestrian(pygame.Rect):
    def __init__(self, x: int, y: int) -> None:
        self.cnt = 0
        super().__init__(x, y, CELL_SIZE, CELL_SIZE)
        try:
            self.__getattribute__('fps')
        except AttributeError:
            raise Exception("You didn't set field 'fps' for class!")

    @classmethod
    def set_fps(cls, fps: int):
        cls.fps = fps

    def move(self, x: int, y: int) -> None:
        self.cnt += 1
        if self.cnt == self.fps:
            super().move_ip(x, y)
            self.cnt = 0


class PhysicalObject(pygame.Rect):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, CELL_SIZE, CELL_SIZE)


class BlindPerson(pygame.Rect):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, CELL_SIZE, CELL_SIZE)

    def hits_object(self, x: int, y: int) -> bool:
        return super().colliderect(x, y, CELL_SIZE, CELL_SIZE)
    
    def hits_objectlist(self, walls: list[pygame.Rect]) -> bool:
        is_collide = super().collidelist(walls)
        return False if is_collide == -1 else True


class NoOutOfBoundsChecker:
    def __init__(self, display: pygame.display):
        self.display = display

    def check_movement(self, x: int, y: int) -> NoOutOfBoundsChecks:
        return NoOutOfBoundsChecks(
            x < self.display.x - CELL_SIZE, x > 0,
            y < self.display.y - CELL_SIZE, y > 0
        )
    

class Color(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)


CELL_SIZE: Final[int] = 32


def main():
    pygame.init()
    DISPLAY = Display(640, 480, 30)
    screen = pygame.display.set_mode((DISPLAY.x, DISPLAY.y))
    clock = pygame.time.Clock()
    oob_checker = NoOutOfBoundsChecker(DISPLAY)

    Pedestrian.set_fps(DISPLAY.fps)

    player = BlindPerson(512, 416)
    pedestrian_01 = Pedestrian(256, 128)
    pedestrians: tuple[Pedestrian] = (pedestrian_01, )

    wall_coords: tuple[tuple[int, int], ...] = (
        (128, 128), (96, 128), (256, 256)
    )
    walls: tuple[PhysicalObject, ...] = tuple(PhysicalObject(x, y) for (x, y) in wall_coords)
    walls_upped = tuple(PhysicalObject(x, y+CELL_SIZE) for (x, y) in wall_coords)
    walls_lefted = tuple(PhysicalObject(x+CELL_SIZE, y) for (x, y) in wall_coords)
    walls_righted = tuple(PhysicalObject(x-CELL_SIZE, y) for (x, y) in wall_coords)
    walls_downed = tuple(PhysicalObject(x, y-CELL_SIZE) for (x, y) in wall_coords)

    while True:
        print(player.x, player.y)  # DEBUG-ONLY

        clock.tick(DISPLAY.fps)
        pedestrian_01.move(0, CELL_SIZE)
        
        no_oob_after_move = oob_checker.check_movement(player.x, player.y)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                # Moving w/o falling in out-of-bounds and collisions w/ objects
                if all(
                    (event.key == pygame.K_w, no_oob_after_move.y_neg, 
                     not player.hits_objectlist(walls_upped))
                ):
                    player.move_ip(0, -CELL_SIZE)
                elif all(
                    (event.key == pygame.K_a, no_oob_after_move.x_neg,
                    not player.hits_objectlist(walls_lefted))
                ):
                    player.move_ip(-CELL_SIZE, 0)
                elif all(
                    (event.key == pygame.K_d, no_oob_after_move.x_pos,
                    not player.hits_objectlist(walls_righted))
                ):
                    player.move_ip(CELL_SIZE, 0)
                elif all(
                    (event.key == pygame.K_s, no_oob_after_move.y_pos,
                    not player.hits_objectlist(walls_downed))
                ):
                    player.move_ip(0, CELL_SIZE)

        # Толчок прохожего при столкновении игрока с ним
        if player.hits_object(pedestrian_01.left, pedestrian_01.top):
            pos_for_punch: list[tuple[int, int]] = []
            for x, y in ((-1, 2), (-2, 1), (1, 2), (2, 1)):
                no_obb_after_punch = oob_checker.check_movement(player.x + CELL_SIZE * x,
                                                                player.y + CELL_SIZE * y)
                if all(
                    (no_obb_after_punch.x_neg, no_obb_after_punch.x_pos, no_obb_after_punch.y_pos)
                ):
                    pos_for_punch.append((x * CELL_SIZE, y * CELL_SIZE))

            if len(pos_for_punch) == 0:
                pos_for_punch.append((0, 1))
            coords = random.choice(pos_for_punch)
            player.move_ip(*coords)

        # Rendering
        screen.fill(Color.BLACK.value)
        pygame.draw.rect(screen, Color.GREEN.value, player)
        
        for pedestrian in pedestrians:
            pygame.draw.rect(screen, Color.RED.value, pedestrian)
        
        for wall in walls:
            pygame.draw.rect(screen, Color.WHITE.value, wall)

        # Screen update
        pygame.display.flip()


if __name__ == '__main__':
    main()