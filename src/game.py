from dataclasses import dataclass

import pygame
import sys


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


@dataclass(frozen=True, slots=True)
class Display:
    x: int
    y: int
    fps: int


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
                
                # перемещение без выхода в out-of-bounds
                if event.key == pygame.K_w and player.y > 0:
                    player.move_ip(0, -CELL_SIZE)
                elif event.key == pygame.K_a and player.x > 0:
                    player.move_ip(-CELL_SIZE, 0)
                elif event.key == pygame.K_d and player.x < DISPLAY.x - CELL_SIZE:
                    player.move_ip(CELL_SIZE, 0)
                elif event.key == pygame.K_s and player.y < DISPLAY.y - CELL_SIZE:
                    player.move_ip(0, CELL_SIZE)

        if player.hits_pedestrian(pedestrian.left, pedestrian.top,
                                  pedestrian.width, pedestrian.height):
            player.move_ip(-CELL_SIZE, CELL_SIZE*2)
        

        # Рендеринг
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 0), player)
        pygame.draw.rect(screen, (255, 0, 0), pedestrian)

        # Обновление экрана
        pygame.display.flip()


if __name__ == '__main__':
    main()