from dataclasses import dataclass

import pygame
import sys


class Street:
    pass


class Pedestrian(pygame.Rect):
    def __init__(self, x: int, y: int) -> None:
        self.cnt = 0
        super().__init__(x, y, CELL_SIZE, CELL_SIZE)

    def move(self, x: int, y: int) -> None:
        self.cnt += 1
        if self.cnt == 8:
            super().move_ip(x, y)
            self.cnt = 0

    def check_pedestrian(self, x: int, y: int) -> bool:
        return super().colliderect()


class BlindPerson(pygame.Rect):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, CELL_SIZE, CELL_SIZE)

    def check_out_of_bounds(self, x: int, y: int) -> bool:
        return super().collidepoint(x, y)


@dataclass(frozen=True, slots=True)
class Display:
    x: int
    y: int


CELL_SIZE = 32


def main():
    pygame.init()
    DISPLAY = Display(640, 480)
    screen = pygame.display.set_mode((DISPLAY.x, DISPLAY.y))
    player = BlindPerson(512, 416)
    pedestrian = Pedestrian(256, 128)

    while True:  # event-loop
        print(player.x, player.y)

        pedestrian.move(0, CELL_SIZE)

        for event in pygame.event.get():


            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_w and player.y > 0:
                    player.move_ip(0, -CELL_SIZE)
                elif event.key == pygame.K_a and player.x > 0:
                    player.move_ip(-CELL_SIZE, 0)
                elif event.key == pygame.K_d and player.x <= DISPLAY.x - CELL_SIZE:
                    player.move_ip(CELL_SIZE, 0)
                elif event.key == pygame.K_s and player.y <= DISPLAY.y - CELL_SIZE:
                    player.move_ip(0, CELL_SIZE)

               # if player.check_pedestrian():

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 0, 0), player)
        pygame.draw.rect(screen, (0, 0, 255), pedestrian)
        pygame.display.flip()  # обновление экрана
        pygame.time.wait(66)


if __name__ == '__main__':
    main()