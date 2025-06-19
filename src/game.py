import random
import sys
from typing import Final, NamedTuple

import pygame

from config.cfg_reader import CELL_SIZE
from classes.base_entities import Color
from classes.single_entities import BlindPerson, Car, Pedestrian, TactileTile, HospitalTile, Wall
from classes.group_entities import Cars, Pedestrians, HospitalTiles
from classes.group_entities import TactileTiles, WallCluster, StaticPedestrians, ObjectsRenderer
from utils import  Display, NoOutOfBoundsChecker, PartialOutOfBoundsChecker
    

class Resolution(NamedTuple):
    width: int
    height: int


class CollisionChecker:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface


WINDOW_SIZE = Resolution(20*CELL_SIZE, 21*CELL_SIZE)
LEVEL_SIZE = Resolution(20*CELL_SIZE, 31*CELL_SIZE)
DISPLAY: Final[Display] = Display(*LEVEL_SIZE, 30)
oob_checker = NoOutOfBoundsChecker(DISPLAY)
npc_oob_checker = PartialOutOfBoundsChecker(DISPLAY)


def main():
    def init_global_state(resolution: Resolution) -> pygame.Surface:
        field = pygame.Surface(resolution)

        Pedestrian.set_fps(DISPLAY.fps)
        Pedestrian.set_color(Color.RED)
        Pedestrian.set_surface(field)

        Car.set_fps(DISPLAY.fps)
        Car.set_color(Color.RED)
        Car.set_surface(field)

        Wall.set_color(Color.WHITE)
        Wall.set_surface(field)

        TactileTile.set_color(Color.YELLOW)
        TactileTile.set_surface(field)

        HospitalTile.set_color(Color.LIGHT_RED)
        HospitalTile.set_surface(field)

        BlindPerson.set_fps(DISPLAY.fps)
        BlindPerson.set_color(Color.GREEN)
        BlindPerson.set_surface(field)

        pygame.init()
        pygame.font.init()

        return field


    def render_frame() -> None:
        """Renders the frame."""
        screen.fill(Color.BLACK.value)
        field.fill(Color.BLACK.value)
        
        object_renderer.render(player)
        # Screen updates
        screen.blit(field, (-320+(LEVEL_SIZE[0]-player.x), -720 +(LEVEL_SIZE[1]-player.y)))
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
        
        field.fill(Color.BLACK.value)
        game_over_text = arial_font.render('YOU WON!', 1, Color.LIGHT_RED.value)
        restart_text = arial_font.render('YOU CAN CLOSE GAME BY HITTING "X" BUTTON', 1, Color.LIGHT_RED.value)
        field.blit(game_over_text, (CELL_SIZE, 5*CELL_SIZE))
        field.blit(restart_text, (CELL_SIZE, 6*CELL_SIZE))
        screen.blit(field, (0, 0))
        pygame.display.flip()


    def render_text(text: str, x: int, y: int) -> None:
        text_to_render = arial_font.render(text, 1, Color.LIGHT_RED.value)
        field.blit(text_to_render, (x, y))


    def restart_game() -> None:
        player.is_alive = True
        player.reset()
        pedestrians.reset()
        car.reset()


    def lose_game() -> None:
        # Kill the player
        player.is_alive = False

        # Render the 3 second timer before restart
        TICKS = 3
        for i in range(TICKS, 0, -1):
            screen.fill(Color.BLACK.value)
            field.fill(Color.BLACK.value)
            render_text('GAME OVER :(', CELL_SIZE, 4*CELL_SIZE)
            render_text('GAME WILL RESTART IN ', CELL_SIZE, 6*CELL_SIZE)
            render_text(str(i), 9*CELL_SIZE, 6*CELL_SIZE)
            screen.blit(field, (0, 0))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    pygame.font.quit()
                    sys.exit()

            pygame.time.wait(990)


    field = init_global_state(LEVEL_SIZE)

    font_path = pygame.font.match_font('arial')
    arial_font = pygame.font.Font(font_path, 25)
    
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    player = BlindPerson(16*CELL_SIZE, 31*CELL_SIZE - 2*CELL_SIZE)

    pedestrians = Pedestrians(
        [
            Pedestrian(18*CELL_SIZE, 9*CELL_SIZE, 0, CELL_SIZE), 
            Pedestrian(480, 256, 0, CELL_SIZE),
            Pedestrian(384, 512, 0, CELL_SIZE),
            Pedestrian(512, 480, 0, CELL_SIZE),
            Pedestrian(576, 512, 0, CELL_SIZE),
            Pedestrian(160, 64, 0, CELL_SIZE),
            Pedestrian(96, 32, 0, CELL_SIZE)
        ]
    )

    static_pedestrians = StaticPedestrians(
        [(x, y) for x in range(384, 608+1, CELL_SIZE) for y in range(352, 480+1, CELL_SIZE)]
    )

    cars = Cars(
        (
            Car(224, 64, 0, CELL_SIZE), Car(288, 32, 0, CELL_SIZE),
            Car(256, 896, 0, -CELL_SIZE), Car(320, 896, 0, -2*CELL_SIZE)
        )
    )

    tactile_tiles = TactileTiles((
        *tuple(TactileTile(448, y) for y in range(352, 448, CELL_SIZE)),
        *tuple(TactileTile(x, 416) for x in range(480, 544, CELL_SIZE)),
        *tuple(TactileTile(512, y) for y in range(416, 513, CELL_SIZE))
    ))


    wall_coords: tuple[tuple[int, int], ...] = (
        *tuple((0, y) for y in range(0, 31*CELL_SIZE, CELL_SIZE)),
        *tuple((192, y) for y in range(0, 256, CELL_SIZE)),
        *tuple((192, y) for y in range(320, 31*CELL_SIZE, CELL_SIZE)),
        *tuple((352, y) for y in range(0, 224, CELL_SIZE)),
        *tuple((352, y) for y in range(320, 31*CELL_SIZE, CELL_SIZE)),
        *tuple((608, y) for y in range(0, LEVEL_SIZE[1], CELL_SIZE)),
        *tuple((x, 0) for x in range(0, 640, CELL_SIZE)),
        *tuple((x, 30*CELL_SIZE) for x in range(0, 640, CELL_SIZE)),
        *tuple((x, 224) for x in range(352, DISPLAY.x, CELL_SIZE))
    )
    walls = WallCluster(*wall_coords)

    hospital = HospitalTiles(
        tuple(
            HospitalTile(x, y) for x in range(32, 170, CELL_SIZE) for y in range(0, 32+1, CELL_SIZE)
        )
    )
    
    object_renderer = ObjectsRenderer()
    object_renderer.add_entity(player)
    for ped in pedestrians:
        object_renderer.add_entity(ped)
    for ped in static_pedestrians:
        object_renderer.add_entity(ped)
    for car in cars:
        object_renderer.add_entity(car)
    for tile in tactile_tiles:
        object_renderer.add_entity(tile)
    for wall in walls:
        object_renderer.add_entity(wall)
    for tile in hospital:
        object_renderer.add_entity(tile)


    is_start_game: bool = True
    while True:
        if is_start_game:
            ICON_X = CELL_SIZE
            TEXT_X = 3*CELL_SIZE

            screen.fill(Color.BLACK.value)
            field.fill(Color.BLACK.value)

            ped = Pedestrian(ICON_X, 3*CELL_SIZE, 0, 0)
            player_ = BlindPerson(ICON_X, 4*CELL_SIZE)
            wall = Wall(ICON_X, 5*CELL_SIZE)
            car = Car(ICON_X, 6*CELL_SIZE, 0, 0)
            tactile = TactileTile(ICON_X, 8.5*CELL_SIZE)
            hospital_ = HospitalTile(ICON_X, 10*CELL_SIZE)

            render_text('BLIND WALKER (alpha)', 7*CELL_SIZE, 2*CELL_SIZE)
            pygame.draw.rect(field, Color.RED.value, ped)
            render_text('Пешеход. Толкается.', TEXT_X, 3*CELL_SIZE)
            pygame.draw.rect(field, Color.GREEN.value, player_)
            render_text('Главный герой - вы :)', TEXT_X, 4*CELL_SIZE)
            pygame.draw.rect(field, Color.WHITE.value, wall)
            render_text('Физический объект. Через него нельзя пройти.', TEXT_X, 5*CELL_SIZE)
            pygame.draw.rect(field, Color.RED.value, car)
            render_text('Автотранспорт. Сбивает насмерть :(', TEXT_X, 6.5*CELL_SIZE)
            pygame.draw.rect(field, Color.YELLOW.value, tactile)
            render_text('Тактильное покрытие. Позволяет ориентироваться ', TEXT_X, 8*CELL_SIZE)
            render_text('на улице.', TEXT_X, 9*CELL_SIZE)
            pygame.draw.rect(field, Color.LIGHT_RED.value, hospital_)
            render_text('Здание поликлиники - причина вашего выхода из дома!', TEXT_X, 10*CELL_SIZE)
            render_text('Управление:', 7*CELL_SIZE, 12*CELL_SIZE)
            render_text('W', ICON_X, 13*CELL_SIZE)
            render_text('Перемещение вверх', TEXT_X, 13*CELL_SIZE)
            render_text('A', ICON_X, 14*CELL_SIZE)
            render_text('Перемещение влево', TEXT_X, 14*CELL_SIZE)
            render_text('S', ICON_X, 15*CELL_SIZE)
            render_text('Перемещение вниз', TEXT_X, 15*CELL_SIZE)
            render_text('D', ICON_X, 16*CELL_SIZE)
            render_text('Перемещение вправо', TEXT_X, 16*CELL_SIZE)
            render_text('PRESS ANY BUTTON TO START', 5*CELL_SIZE, 18*CELL_SIZE)
            screen.blit(field, (0, 0))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    pygame.font.quit()
                    sys.exit()
                
                elif event.type == pygame.KEYDOWN:
                    is_start_game = False

        elif not player.is_won:
            print('Player coords:', player.x, player.y)
            clock.tick(DISPLAY.fps)
            
            # Bots' movement
            pedestrians.make_move()
            cars.make_move()
            
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
            if player.hits_objectlist(pedestrians.tolist() + static_pedestrians.tolist()):
                pos_for_punch: list[tuple[int, int]] = []
                for x, y in ((-1, 2), (-2, 1), (1, 2), (2, 1)):
                    new_x = player.x + 32*x
                    new_y = player.y + 32*y
                    no_obb_after_punch = oob_checker.check_movement(new_x, new_y)
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
                lose_game()
                restart_game()

            if player.is_on_tactile == False and player.hits_objectlist(tactile_tiles.tolist()):
                player.is_on_tactile = True
                _coords = [(448, y) for y in range(11*CELL_SIZE, 14*CELL_SIZE, CELL_SIZE)] + \
                    [(x, 416) for x in range(15*CELL_SIZE, 17*CELL_SIZE, CELL_SIZE)] + \
                    [(512, y) for y in range(14*CELL_SIZE, 16*CELL_SIZE, CELL_SIZE)]
                for coord in _coords:
                    static_pedestrians.remove(*coord)


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
