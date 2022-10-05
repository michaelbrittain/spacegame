import pygame
from dataclasses import dataclass, field
from colour import Colour
from typing import List

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    KEYUP,
    KEYDOWN
)


@dataclass
class Missile:
    x: int = 0
    y: int = 0
    width: int = 10
    height: int = 10
    colour: tuple = Colour.YELLOW

    def update(self, pressed_keys: dict = None) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))

    def is_collision(self, other: "Enemy"):
        enter_left = other.x + other.width >= self.x
        not_exit_right = self.x + self.width >= other.x
        
        enter_top = other.y + other.height >= self.y
        not_exit_bottom = self.y + self.height >= other.y

        return enter_left and not_exit_right and enter_top and not_exit_bottom

    def is_in_bounds(self, screen: pygame.Surface):
        return -self.width < self.x < screen.get_width() and -self.height < self.y < screen.get_height()     


@dataclass
class Player:
    x: int = 0
    y: int = 0
    width: int = 50
    height: int = 50
    colour: tuple = Colour.BLUE
    move_x: int = 0
    move_y: int = 0
    move_speed: int = 10

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
                
    def update(self, screen: pygame.Surface) -> None:
        self.x += self.move_x * self.move_speed
        self.y += self.move_y * self.move_speed
        self.reset_if_out_of_bounds(screen)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))

    def reset_if_out_of_bounds(self, screen: pygame.Surface):
        x_bound = screen.get_width() - self.width
        y_bound = screen.get_height() - self.height

        if self.x < 0:
            self.x = 0
        elif self.x > x_bound:
            self.x = x_bound

        if self.y < 0:
            self.y = 0
        elif self.y > y_bound:
            self.y = y_bound        


@dataclass
class Enemy:
    x: int = 0
    y: int = 0
    width: int = 50
    height: int = 50
    colour: tuple = Colour.RED

    def update(self, pressed_keys: dict = None) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
