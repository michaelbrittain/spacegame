import pygame
import random
from player import Player, Enemy, Missile, InfoBoard, Screen
from colour import Colour

from pygame.locals import (
    K_SPACE,
)

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50
MISSILE_WIDTH = 10
MISSILE_HEIGHT = 10
MISSILE_SPEED = 10
MAX_MISSILES = 3
MAX_ENEMIES = 3
ENEMIES = []


def spawn_enemies(screen: Screen):
    while len(ENEMIES) < MAX_ENEMIES:
        enemy_x = random.randint(screen.width // 2, screen.width - ENEMY_WIDTH)
        enemy_y = random.randint(0, screen.height - ENEMY_HEIGHT)
        enemy_width = random.randint(ENEMY_WIDTH // 2, ENEMY_WIDTH)
        enemy_height = random.randint(ENEMY_HEIGHT // 2, ENEMY_HEIGHT)
        enemy_colour = random.choice((Colour.GREEN, Colour.PURPLE, Colour.CYAN, Colour.ORANGE, Colour.INDIGO))
        enemy = Enemy(enemy_x, enemy_y, enemy_width, enemy_height, enemy_colour)
        ENEMIES.append(enemy)
        screen.add_object(enemy)

 
def update_enemies(screen: Screen):
    for enemy in ENEMIES:
        if random.random() < 0.1:
            enemy.x += random.randint(-ENEMY_WIDTH, ENEMY_HEIGHT)
            enemy.y += random.randint(-ENEMY_WIDTH, ENEMY_HEIGHT)
            if -ENEMY_WIDTH < enemy.x < screen.width and -ENEMY_HEIGHT < enemy.y < screen.height:
                continue
            ENEMIES.remove(enemy)
            screen.remove_object(enemy)


def play_game():
    pygame.init()
    running = True
    missiles = []

    screen = Screen()
    clock = pygame.time.Clock()
    player = Player(0, screen.height // 2, PLAYER_WIDTH, PLAYER_HEIGHT)
    score_board = InfoBoard("Score", screen.width - 175, screen.height - 60)
    timer_board = InfoBoard("Countdown", screen.width - 175, screen.height - 30, value=1000)
    screen.add_objects([player, score_board, timer_board])

    while running:
        clock.tick(30)  # frames per sec
        spawn_enemies(screen)
        update_enemies(screen)
        player.update(screen.surface)
        timer_board.value -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type not in [pygame.KEYDOWN, pygame.KEYUP]:
                continue

            pressed_keys = pygame.key.get_pressed()
            player.register_event(event.type, pressed_keys)
            player.reset_if_out_of_bounds(screen.surface)

            if event.type == pygame.KEYDOWN and pressed_keys[K_SPACE] and len(missiles) < 3:
                missile = Missile(player.x + player.width, player.y + player.height // 2 - MISSILE_HEIGHT, MISSILE_WIDTH, MISSILE_HEIGHT)
                missiles.append(missile)
                screen.add_object(missile)

        for missile in missiles:
            missile.x += MISSILE_SPEED
            if not missile.is_in_bounds(screen.surface):
                missiles.remove(missile)
                screen.remove_object(missile)
                continue
            for enemy in ENEMIES:
                if missile.is_collision(enemy):
                    ENEMIES.remove(enemy)
                    screen.remove_object(enemy)
                    missiles.remove(missile)
                    screen.remove_object(missile)
                    score_board.value += 1

        screen.draw()

        if timer_board.value < 0:
            running = False


if __name__ == "__main__":
    play_game()