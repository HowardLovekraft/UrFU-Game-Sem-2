from dataclasses import dataclass

import pygame
import random
import sys


@dataclass(frozen=True, slots=True)
class Display:
    x: int
    y: int
    fps: int


@dataclass(frozen=True, slots=True)
class OutOfBoundsChecks:
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


class BlindPerson(pygame.Rect):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, CELL_SIZE, CELL_SIZE)

    def hits_pedestrian(self, x: int, y: int, x_size: int, y_size: int) -> bool:
        return super().colliderect(x, y, x_size, y_size)


def check_outofbounds(x: int, y: int, display) -> OutOfBoundsChecks:
    return OutOfBoundsChecks(
        x < display.x - CELL_SIZE,
        x > 0,
        y < display.y - CELL_SIZE,
        y > 0
    )


CELL_SIZE = 32


def main():
    pygame.init()
    DISPLAY = Display(640, 480, 30)
    screen = pygame.display.set_mode((DISPLAY.x, DISPLAY.y))
    clock = pygame.time.Clock()

    Pedestrian.set_fps(DISPLAY.fps)

    player = BlindPerson(512, 416)
    pedestrian = Pedestrian(256, 128)

    while True:
        print(player.x, player.y)  # DEBUG-ONLY

        clock.tick(DISPLAY.fps)

        pedestrian.move(0, CELL_SIZE)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                player_out_of_bounds = check_outofbounds(player.x, player.y, DISPLAY)

                # Moving w/o falling in out-of-bounds
                if event.key == pygame.K_w and player_out_of_bounds.y_neg:
                    player.move_ip(0, -CELL_SIZE)
                elif event.key == pygame.K_a and player_out_of_bounds.x_neg:
                    player.move_ip(-CELL_SIZE, 0)
                elif event.key == pygame.K_d and player_out_of_bounds.x_pos:
                    player.move_ip(CELL_SIZE, 0)
                elif event.key == pygame.K_s and player_out_of_bounds.y_pos:
                    player.move_ip(0, CELL_SIZE)

        
        if (
            player.hits_pedestrian(pedestrian.left, pedestrian.top,
                                   pedestrian.width, pedestrian.height) and
            1
        ):
            player.move_ip(-CELL_SIZE, CELL_SIZE*2)
        

        # Rendering
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 0), player)
        pygame.draw.rect(screen, (255, 0, 0), pedestrian)

        # Screen update
        pygame.display.flip()


if __name__ == '__main__':
    main()