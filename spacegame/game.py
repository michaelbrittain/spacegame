import pygame
import random
import time
from models import Player, Enemy, Missile
from screen import InfoBoard
from colour import Colour
from models import GameObject
from utils import load_sprite, load_sound


class SpaceGame:
    def __init__(self, max_enemies: int = 3) -> None:
        self._init_pygame()
        self.max_enemies = max_enemies
        self.background = load_sprite("background", "jpg", False)
        self.player = Player(0, self.screen.get_height() // 2, fire_missile_callback=self._fire_missile)
        self.enemies = []
        self.missiles = []

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Game")
        self.screen = pygame.display.set_mode((800, 600))
        self.score_board = InfoBoard("Score", self.screen.get_width() - 175, self.screen.get_height() - 60)
        self.timer_board = InfoBoard("Countdown", self.screen.get_width() - 175, self.screen.get_height() - 30, value=1000)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.hit_sound = load_sound("hit")

    def play(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type not in [pygame.KEYDOWN, pygame.KEYUP]:
                continue
            self.player.register_event(event.type, pygame.key.get_pressed())

    def _process_game_logic(self):
        while len(self.enemies) < self.max_enemies:
            self._spawn_enemy()

        for game_object in self._game_objects:
            game_object.move(self.screen)

        for missile in self.missiles[:]:
            if not missile.is_in_bounds(self.screen):
                self.missiles.remove(missile)
                continue            
            for enemy in self.enemies[:]:
                if missile.is_collision(enemy):
                    self.hit_sound.play()
                    self.enemies.remove(enemy)
                    self.missiles.remove(missile)
                    self.score_board.value += 1                    
                    break

        self.timer_board.value -= 1
        if self.timer_board.value == 0:
            time.sleep(5)
            quit()

    def _draw(self):
        # self.screen.fill((Colour.BLACK))
        self.screen.blit(self.background, (0, 0))
        for game_object in self._game_objects:
            game_object.draw(self.screen)
        self.score_board.draw(self.screen)
        self.timer_board.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(30)

    @property
    def _game_objects(self):
        return [self.player, *self.enemies, *self.missiles]

    def _spawn_enemy(self):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        enemy_width = enemy_height = 50
        enemy_x = random.randint(screen_width // 2, screen_width - enemy_width)
        enemy_y = random.randint(0, screen_height - enemy_height)
        enemy_width = random.randint(enemy_width // 2, enemy_width)
        enemy_height = random.randint(enemy_height // 2, enemy_height)
        enemy_colour = random.choice((Colour.GREEN, Colour.PURPLE, Colour.CYAN, Colour.ORANGE, Colour.INDIGO))
        enemy = Enemy(enemy_x, enemy_y, enemy_width, enemy_height, enemy_colour)
        self.enemies.append(enemy)

    def _fire_missile(self, game_object: GameObject):
        if len(self.missiles) < 3:
            missile = Missile(game_object.x + game_object.width, game_object.y + game_object.height // 2)
            self.missiles.append(missile)

