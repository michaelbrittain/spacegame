import pygame
import random
from typing import Callable
from dataclasses import dataclass
from colour import Colour
from utils import load_sprite, load_sound

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
)


@dataclass
class GameObject:
    x: int = 0
    y: int = 0
    width: int = 10
    height: int = 10
    colour: tuple = Colour.YELLOW
    move_x: int = 0
    move_y: int = 0
    move_speed: int = 0
    sprite: pygame.Surface = None

    def draw(self, surface: pygame.Surface) -> None:
        if self.sprite:
            surface.blit(self.sprite, (self.x, self.y))
            sprite_rect = self.sprite.get_rect()
            self.width = sprite_rect.width
            self.height = sprite_rect.height
        else:
            pygame.draw.rect(surface, self.colour, (self.x, self.y, self.width, self.height))

    def move(self, surface: pygame.Surface):
        self.x += self.move_x * self.move_speed
        self.y += self.move_y * self.move_speed
        self.reset_if_out_of_bounds(surface)

    def reset_if_out_of_bounds(self, surface: pygame.Surface):
        x_bound = surface.get_width() - self.width
        y_bound = surface.get_height() - self.height

        if self.x < 0:
            self.x = 0
        elif self.x > x_bound:
            self.x = x_bound

        if self.y < 0:
            self.y = 0
        elif self.y > y_bound:
            self.y = y_bound          

    def is_collision(self, other: "GameObject"):
        enter_left = other.x + other.width >= self.x
        not_exit_right = self.x + self.width >= other.x
        
        enter_top = other.y + other.height >= self.y
        not_exit_bottom = self.y + self.height >= other.y

        return enter_left and not_exit_right and enter_top and not_exit_bottom

    def is_in_bounds(self, screen: pygame.Surface):
        return -self.width < self.x < screen.get_width() and -self.height < self.y < screen.get_height()     


@dataclass
class Player(GameObject):
    width: int = 50
    height: int = 50
    colour: tuple = Colour.BLUE
    move_speed: int = 10
    fire_missile_callback: Callable = None
    missile_sound: pygame.mixer.Sound = None

    def __post_init__(self):
        self.sprite = load_sprite("goat")
        self.missile_sound = load_sound("laser")        

    def register_event(self, event_type: int = 0, pressed_keys: dict = None) -> None:
        if event_type == pygame.KEYUP:
            if not pressed_keys[K_LEFT] and not pressed_keys[K_RIGHT]:
                self.move_x = 0
            if not pressed_keys[K_UP] and not pressed_keys[K_DOWN]:
                self.move_y = 0
        elif event_type == pygame.KEYDOWN:
            self.move_x = 0
            self.move_y = 0
            if pressed_keys[K_UP]:
                self.move_y = -1
            if pressed_keys[K_DOWN]:
                self.move_y = 1
            if pressed_keys[K_LEFT]:
                self.move_x = -1
            if pressed_keys[K_RIGHT]:
                self.move_x = 1
            if pressed_keys[K_SPACE]:
                self.fire_missile_callback(self)
                self.missile_sound.play()


@dataclass
class Enemy(GameObject):
    width: int = 50
    height: int = 50
    colour: tuple = Colour.RED

    def __post_init__(self):
        self.sprite = load_sprite("alien")
        # self.x = random.randint(self.screen.width // 2, self.screen.width - self.width)
        # self.y = random.randint(0, self.screen.height - self.height)
        # self.width = random.randint(self.width // 2, self.width)
        # self.height = random.randint(self.height // 2, self.height)
        # self.colour = random.choice((Colour.GREEN, Colour.PURPLE, Colour.CYAN, Colour.ORANGE, Colour.INDIGO))

    def move(self, surface: pygame.Surface):
        if random.random() < 0.1:
            self.move_x = random.randint(-1, 1)
            self.move_y = random.randint(-1, 1)
            self.move_speed = random.randint(0, 10)
        super().move(surface)

@dataclass
class Missile(GameObject):
    width: int = 10
    height: int = 10
    colour: tuple = Colour.YELLOW
    move_x: int = 1
    move_speed: int = 10      

    def move(self, surface: pygame.Surface):
        self.x += self.move_x * self.move_speed
