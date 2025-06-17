import random
import sys
import time
from typing import Final

from icecream import ic
import pygame

from classes.gameclasses import Color
from classes.gameclasses import BlindPerson, Car, Cars, Pedestrian, Pedestrians
from classes.gameclasses import PhysObjectCluster, TactileTile, TactileTiles, PhysicalObject
from classes.gameclasses import HospitalTile, HospitalTiles
from classes.abstracts import CELL_SIZE
from utils import  Display, NoOutOfBoundsChecker, PartialOutOfBoundsChecker
    

DISPLAY: Final[Display] = Display(640, 992, 30)
oob_checker = NoOutOfBoundsChecker(DISPLAY)
npc_oob_checker = PartialOutOfBoundsChecker(DISPLAY)


def main():
    def init_global_state() -> None:
        Pedestrian.set_fps(DISPLAY.fps)
        Car.set_fps(DISPLAY.fps)
        pygame.init()
        pygame.font.init()

    def render_frame() -> None:
        """Renders the frame."""
        screen.fill(Color.BLACK.value)
        
        for tactile in tactile_tiles:
            pygame.draw.rect(screen, Color.YELLOW.value, tactile)
        for ped in pedestrians:
            pygame.draw.rect(screen, Color.RED.value, ped)
        for car in cars:
            pygame.draw.rect(screen, Color.RED.value, car)
        for wall in walls:
            pygame.draw.rect(screen, Color.WHITE.value, wall)
        for hospital_tile in hospital:
            pygame.draw.rect(screen, Color.LIGHT_RED.value, hospital_tile)
            
        pygame.draw.rect(screen, Color.GREEN.value, player)
        # Screen updates
        pygame.display.flip()

    def move_player() -> None:
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

    def finish_game() -> None:
        clock.tick(DISPLAY.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.font.quit()
                sys.exit()
        
        screen.fill(Color.BLACK.value)
        game_over_text = arial_font.render('YOU WON!', 1, Color.LIGHT_RED.value)
        restart_text = arial_font.render('YOU CAN CLOSE GAME BY HITTING "X" BUTTON', 1, Color.LIGHT_RED.value)
        screen.blit(game_over_text, (CELL_SIZE, 5*CELL_SIZE))
        screen.blit(restart_text, (CELL_SIZE, 6*CELL_SIZE))
        pygame.display.flip()

    def render_text(text: str, x: int, y: int) -> None:
        text_to_render = arial_font.render(text, 1, Color.LIGHT_RED.value)
        screen.blit(text_to_render, (x, y))

    def restart_game() -> None:
        player.is_alive = True
        player.reset()
        pedestrians.reset()
        car.reset()


    init_global_state()

    font_path = pygame.font.match_font('arial')
    arial_font = pygame.font.Font(font_path, 25)
    
    screen = pygame.display.set_mode((DISPLAY.x, DISPLAY.y))
    clock = pygame.time.Clock()


    player = BlindPerson(512, DISPLAY.y - 2*CELL_SIZE)
    npc: list = []

    pedestrians = Pedestrians(
        [
            Pedestrian(576, 288, 0, 32), 
            Pedestrian(480, 256, 0, 32),
            *[Pedestrian(x, y, 0, 0) for x in range(384, 608+1, CELL_SIZE) for y in range(352, 480+1, CELL_SIZE)]
        ]
    )

    cars = Cars(
        (
            Car(224, 64), Car(320, 32)
        )
    )

    tactile_tiles = TactileTiles((
        *tuple(TactileTile(448, y) for y in range(352, 448, CELL_SIZE)),
        *tuple(TactileTile(x, 416) for x in range(480, 544, CELL_SIZE)),
        *tuple(TactileTile(512, y) for y in range(416, 513, CELL_SIZE))
    ))


    wall_coords: tuple[tuple[int, int], ...] = (
        # *tuple((0, y) for y in range(0, 640, CELL_SIZE)),
        *tuple((0, y) for y in range(0, DISPLAY.y, CELL_SIZE)),
        *tuple((192, y) for y in range(0, 256, CELL_SIZE)),
        *tuple((192, y) for y in range(320, DISPLAY.y, CELL_SIZE)),
        *tuple((352, y) for y in range(0, 224, CELL_SIZE)),
        *tuple((352, y) for y in range(320, DISPLAY.y, CELL_SIZE)),
        *tuple((x, DISPLAY.y-CELL_SIZE) for x in range(0, 640, CELL_SIZE)),
        *tuple((x, 224) for x in range(352, DISPLAY.x, CELL_SIZE))
    )
    walls = PhysObjectCluster(*wall_coords)

    hospital = HospitalTiles(
        tuple(
            HospitalTile(x, y) for x in range(32, 170, CELL_SIZE) for y in range(0, 32+1, CELL_SIZE)
        )
    )

    npc.extend(pedestrians.tolist())
    npc.extend(walls.tolist())

    is_start_game: bool = True
    while True:
        if is_start_game:
            ICON_X = CELL_SIZE
            TEXT_X = 3*CELL_SIZE

            screen.fill(Color.BLACK.value)

            ped = Pedestrian(ICON_X, 6*CELL_SIZE, 0, 0)
            player_ = BlindPerson(ICON_X, 7*CELL_SIZE)
            wall = PhysicalObject(ICON_X, 8*CELL_SIZE)
            car = Car(ICON_X, 9*CELL_SIZE)
            tactile = TactileTile(ICON_X, 11*CELL_SIZE)
            hospital_ = HospitalTile(ICON_X, 13*CELL_SIZE)


            render_text('BLIND WALKER (alpha)', 7*CELL_SIZE, 5*CELL_SIZE)
            pygame.draw.rect(screen, Color.RED.value, ped)
            render_text('Пешеход. Толкается.', TEXT_X, 6*CELL_SIZE)
            pygame.draw.rect(screen, Color.GREEN.value, player_)
            render_text('Главный герой - вы :)', TEXT_X, 7*CELL_SIZE)
            pygame.draw.rect(screen, Color.WHITE.value, wall)
            render_text('Физический объект. Через него нельзя пройти.', TEXT_X, 8*CELL_SIZE)
            pygame.draw.rect(screen, Color.RED.value, car)
            render_text('Автотранспорт. В исекай не отправляет :(', TEXT_X, 9.5*CELL_SIZE)
            pygame.draw.rect(screen, Color.YELLOW.value, tactile)
            render_text('Тактильное покрытие. Позволяет ориентироваться ', TEXT_X, 11*CELL_SIZE)
            render_text('на улице.', TEXT_X, 12*CELL_SIZE)
            pygame.draw.rect(screen, Color.LIGHT_RED.value, hospital_)
            render_text('Здание поликлиники - причина вашего выхода из дома!', TEXT_X, 13*CELL_SIZE)
            render_text('Управление:', 7*CELL_SIZE, 15*CELL_SIZE)
            render_text('W', ICON_X, 16*CELL_SIZE)
            render_text('Перемещение вверх', TEXT_X, 16*CELL_SIZE)
            render_text('A', ICON_X, 17*CELL_SIZE)
            render_text('Перемещение влево', TEXT_X, 17*CELL_SIZE)
            render_text('S', ICON_X, 18*CELL_SIZE)
            render_text('Перемещение вниз', TEXT_X, 18*CELL_SIZE)
            render_text('D', ICON_X, 19*CELL_SIZE)
            render_text('Перемещение вправо', TEXT_X, 19*CELL_SIZE)
            render_text('PRESS ANY BUTTON TO START', 5*CELL_SIZE, 22*CELL_SIZE)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    pygame.font.quit()
                    sys.exit()
                
                elif event.type == pygame.KEYDOWN:
                    is_start_game = False

        elif not player.is_won:
            print(player.x, player.y)  # DEBUG-ONLY
            clock.tick(DISPLAY.fps)
            
            # Bots' movement
            pedestrians.make_step(0, CELL_SIZE)
            cars.go(0, CELL_SIZE)
            
            no_oob_after_move = oob_checker.check_movement(player.x, player.y)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    pygame.font.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    move_player()

            for ped in pedestrians:
                if npc_oob_checker.check_movement(ped.x, ped.y).generally():
                    ped.reset()

            for car in cars:
                if npc_oob_checker.check_movement(car.x, car.y).generally():
                    car.reset()


            # Толчок прохожего при столкновении игрока с ним
            if player.hits_objectlist(pedestrians.tolist()):
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
            if player.hits_objectlist(cars.tolist()):
                # Kill the player
                player.is_alive = False

                # Render the 3 second timer before restart
                TICKS = 3
                for i in range(TICKS, 0, -1):
                    screen.fill(Color.BLACK.value)
                    render_text('GAME OVER', CELL_SIZE, 5*CELL_SIZE)
                    render_text('GAME WILL RESTART IN ', CELL_SIZE, 6*CELL_SIZE)
                    render_text(str(i), 9*CELL_SIZE, 6*CELL_SIZE)
                    pygame.display.flip()
                    pygame.time.wait(990)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            pygame.font.quit()
                            sys.exit()


                restart_game()

            if player.is_on_tactile == False and player.hits_objectlist(tactile_tiles.tolist()):
                player.is_on_tactile = True
                _coords = [(448, y) for y in range(11*CELL_SIZE, 14*CELL_SIZE, CELL_SIZE)] + \
                    [(x, 416) for x in range(15*CELL_SIZE, 17*CELL_SIZE, CELL_SIZE)] + \
                    [(512, y) for y in range(14*CELL_SIZE, 16*CELL_SIZE, CELL_SIZE)]
                for coord in _coords:
                    pedestrians.remove(*coord)


            if player.hits_objectlist(hospital.tolist()):
                # Kill the player
                player.is_won = True
                player.is_alive = False

            if player.is_alive: 
                render_frame()

        elif player.is_won:
            finish_game()

if __name__ == '__main__':
    main()
