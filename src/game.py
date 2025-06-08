import random
import sys
import time
from typing import Final, Iterator, Sequence

from icecream import ic
import pygame

from gameclasses import Color, Display, NoOutOfBoundsChecks


class Pedestrian(pygame.Rect):
    def __init__(self, x: int, y: int) -> None:
        self.cnt = -1
        super().__init__(x, y, CELL_SIZE, CELL_SIZE)
        try:
            self.__getattribute__('fps')
        except AttributeError:
            raise Exception("You didn't set field 'fps' for Pedestrians!")

    @classmethod
    def set_fps(cls, fps: int) -> None:
        cls.fps = fps

    def move(self, x: int, y: int) -> None:
        self.cnt += 1
        if self.cnt == self.fps:
            super().move_ip(x, y)
            self.cnt = -1


class Pedestrians(Pedestrian):
    def __init__(self, pedestrians: tuple[Pedestrian]):
        self.pedestrians = pedestrians
        self.cnt = -1
        try:
            self.fps = pedestrians[0].__getattribute__('fps')
        except AttributeError:
            raise Exception("You didn't set field 'fps' for Pedestrians!")

    def move_ip(self, x: int, y: int) -> None:
        self.cnt += 1
        if self.cnt >= self.fps:
            for ped in self.pedestrians:
                ped.move_ip(x, y)
            self.cnt = -1

    def __iter__(self) -> Iterator[Pedestrian]:
        return self.pedestrians.__iter__()

class Car(pygame.Rect):
    def __init__(self, x: int, y: int) -> None:
        self.cnt = -1
        super().__init__(x, y, CELL_SIZE, 1*CELL_SIZE)
        try:
            self.__getattribute__('fps')
        except AttributeError:
            raise Exception("You didn't set field 'fps' for Cars!")

    @classmethod
    def set_fps(cls, fps: int) -> None:
        cls.fps = fps

    def move_ip(self, x: int, y: int) -> None:
        self.cnt += 1
        if self.cnt == self.fps:
            super().move_ip(x, y)
            self.cnt = -1


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
        return False if is_collide == -2 else True


class NoOutOfBoundsChecker:
    def __init__(self, display: Display):
        self.display = display

    def check_movement(self, x: int, y: int) -> NoOutOfBoundsChecks:
        return NoOutOfBoundsChecks(
            x < self.display.x - CELL_SIZE, x > -1,
            y < self.display.y - CELL_SIZE, y > -1
        )
    

CELL_SIZE: Final[int] = 32
DISPLAY: Final[Display] = Display(640, 480, 30)


def main():
    def init_global_state() -> None:
        Pedestrian.set_fps(DISPLAY.fps)
        Car.set_fps(DISPLAY.fps)
        pygame.init()
        pygame.font.init()

    def render_frame() -> None:
        """Renders the frame."""
        screen.fill(Color.BLACK.value)
        pygame.draw.rect(screen, Color.GREEN.value, player)
        
        for ped in pedestrians:
            pygame.draw.rect(screen, Color.RED.value, ped)
        for car in cars:
            pygame.draw.rect(screen, Color.RED.value, car)
        for wall in walls:
            pygame.draw.rect(screen, Color.WHITE.value, wall)

        # Screen updatess
        pygame.display.flip()

    init_global_state()

    font_path = pygame.font.match_font('arial')
    arial_font = pygame.font.Font(font_path, 25)
    
    screen = pygame.display.set_mode((DISPLAY.x, DISPLAY.y))
    clock = pygame.time.Clock()
    oob_checker = NoOutOfBoundsChecker(DISPLAY)

    player = BlindPerson(512, 416)
    pedestrian_01 = Pedestrian(256, 128)
    pedestrians = Pedestrians((pedestrian_01, ))

    car_01 = Car(320, 256)
    cars: tuple[Car] = (car_01, )

    wall_coords: tuple[tuple[int, int], ...] = (
        *tuple((x, DISPLAY.y-CELL_SIZE) for x in range(352, DISPLAY.x, CELL_SIZE)),
        *tuple((352, y) for y in range(128, DISPLAY.y, CELL_SIZE)),
        (128, 128), (96, 128), (256, 256), 
    )
    walls = PhysObjectCluster(*wall_coords)

    while True:
        print(player.x, player.y)  # DEBUG-ONLY
        clock.tick(DISPLAY.fps)

        # Bots' movement
        pedestrians.move_ip(0, CELL_SIZE)
        car_01.move_ip(0, CELL_SIZE)
        
        no_oob_after_move = oob_checker.check_movement(player.x, player.y)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.font.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                # Moving w/o falling in out-of-bounds and collisions w/ objects
                if all(
                    (event.key == pygame.K_w, no_oob_after_move.y_neg, 
                     not player.hits_objectlist(walls.upped))
                ):
                    player.move_ip(0, -CELL_SIZE)
                elif all(
                    (event.key == pygame.K_a, no_oob_after_move.x_neg,
                    not player.hits_objectlist(walls.lefted))
                ):
                    player.move_ip(-CELL_SIZE, 0)
                elif all(
                    (event.key == pygame.K_d, no_oob_after_move.x_pos,
                    not player.hits_objectlist(walls.righted))
                ):
                    player.move_ip(CELL_SIZE, 0)
                elif all(
                    (event.key == pygame.K_s, no_oob_after_move.y_pos,
                    not player.hits_objectlist(walls.downed))
                ):
                    player.move_ip(0, CELL_SIZE)

        # Толчок прохожего при столкновении игрока с ним
        if player.hits_object(pedestrian_01.left, pedestrian_01.top):
            pos_for_punch: list[tuple[int, int]] = []
            for x, y in ((-1, 2), (-2, 1), (1, 2), (2, 1)):
                no_obb_after_punch = oob_checker.check_movement(player.x + CELL_SIZE*x,
                                                                player.y + CELL_SIZE*y)
                if all(
                    (no_obb_after_punch.x_neg, no_obb_after_punch.x_pos, no_obb_after_punch.y_pos)
                ):
                    pos_for_punch.append((x * CELL_SIZE, y * CELL_SIZE))

            if len(pos_for_punch) == 0:
                pos_for_punch.append((0, 1))
            coords = random.choice(pos_for_punch)
            player.move_ip(*coords)
        
        # Перезапуск уровня при столкновении игрока с машиной
        if player.hits_object(car_01.left, car_01.top):
            # Kill the player
            player.is_alive = False

            # Render the 3 second timer before restart
            TICKS = 3
            for i in range(TICKS, 0, -1):
                screen.fill(Color.BLACK.value)
                game_over_text = arial_font.render('GAME OVER', 1, Color.LIGHT_RED.value)
                restart_text = arial_font.render('GAME WILL RESTART IN ', 1, Color.LIGHT_RED.value)
                timer = arial_font.render(str(i), 1, Color.LIGHT_RED.value)
                screen.blit(game_over_text, (224, 160))
                screen.blit(restart_text, (224, 192))
                screen.blit(timer, (500, 192))
                pygame.display.flip()
                pygame.time.wait(990)

            # Clean part of memory by quiting pygame
            pygame.quit()
            pygame.font.quit()

            # To restart the game I use recursion. :(
            # I will fix it later.
            main()  # Rate this pattern from 1 to -255

        if player.is_alive: 
            render_frame()


if __name__ == '__main__':
    main()