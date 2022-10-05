import pygame
import random
import time
from player import Player, Enemy, Missile
from colour import Colour

from pygame.locals import (
    K_SPACE,
)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
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


def spawn_enemies():
    while len(ENEMIES) < MAX_ENEMIES:
        enemy_x = random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - ENEMY_WIDTH)
        enemy_y = random.randint(0, SCREEN_HEIGHT - ENEMY_HEIGHT)
        enemy_width = random.randint(ENEMY_WIDTH // 2, ENEMY_WIDTH)
        enemy_height = random.randint(ENEMY_HEIGHT // 2, ENEMY_HEIGHT)
        enemy_colour = random.choice((Colour.GREEN, Colour.PURPLE, Colour.CYAN, Colour.ORANGE, Colour.INDIGO))
        enemy = Enemy(enemy_x, enemy_y, enemy_width, enemy_height, enemy_colour)
        ENEMIES.append(enemy)

 
def update_enemies():
    for enemy in ENEMIES:
        if random.random() < 0.1:
            enemy.x += random.randint(-ENEMY_WIDTH, ENEMY_HEIGHT)
            enemy.y += random.randint(-ENEMY_WIDTH, ENEMY_HEIGHT)
            if -ENEMY_WIDTH < enemy.x < SCREEN_WIDTH and -ENEMY_HEIGHT < enemy.y < SCREEN_HEIGHT:
                continue
            ENEMIES.remove(enemy)


def play_game():
    pygame.init()
    running = True
    score = 0
    time_left = 1000
    missiles = []

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 25)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(0, SCREEN_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)

    while running:
        clock.tick(30)  # frames per sec
        spawn_enemies()
        update_enemies()
        player.update(screen)
        time_left -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type not in [pygame.KEYDOWN, pygame.KEYUP]:
                continue

            pressed_keys = pygame.key.get_pressed()
            player.register_event(event.type, pressed_keys)
            player.reset_if_out_of_bounds(screen)

            if event.type == pygame.KEYDOWN and pressed_keys[K_SPACE] and len(missiles) < 3:
                missile = Missile(player.x + player.width, player.y + player.height // 2 - MISSILE_HEIGHT, MISSILE_WIDTH, MISSILE_HEIGHT)
                missiles.append(missile)

        for missile in missiles:
            missile.x += MISSILE_SPEED
            if not missile.is_in_bounds(screen):
                missiles.remove(missile)
                continue
            for enemy in ENEMIES:
                if missile.is_collision(enemy):
                    ENEMIES.remove(enemy)
                    missiles.remove(missile)
                    score += 1

        screen.fill(Colour.BLACK)        
        player.draw(screen)
        for enemy in ENEMIES:
            enemy.draw(screen)
        for missile in missiles:         
            missile.draw(screen)

        score_label = font.render(f"Score: {score}", True, Colour.YELLOW)
        screen.blit(score_label, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 60))

        time_label = font.render(f"Time: {time_left}", True, Colour.YELLOW)
        screen.blit(time_label, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 30))

        pygame.display.update()

        if time_left < 0:
            running = False
         
    # pygame.time.wait(3000)


if __name__ == "__main__":
    play_game()