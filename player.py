import pygame
from typing import Protocol, List
from dataclasses import dataclass, field
from colour import Colour

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)


class GameObject(Protocol):
    def draw(self, screen: pygame.Surface) -> None:
        ...


@dataclass
class Missile:
    x: int
    y: int
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
    x: int
    y: int
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
    x: int
    y: int
    width: int = 50
    height: int = 50
    colour: tuple = Colour.RED

    def update(self, pressed_keys: dict = None) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))


@dataclass
class InfoBoard:
    label: str
    x: int
    y: int
    value: int = 0
    font_family: str = "monospace"
    font_size: int = 20
    colour: tuple = Colour.YELLOW
    _font: pygame.font.SysFont = field(init=False, default=None) 

    def __post_init__(self):
        self._font = pygame.font.SysFont(self.font_family, self.font_size)        

    def draw(self, screen: pygame.Surface) -> None:
        label = self._font.render(f"{self.label}: {self.value}", True, self.colour)
        screen.blit(label, (self.x, self.y))


@dataclass
class Screen:
    width: int = 800
    height: int = 600
    game_objects: List[GameObject] = field(default_factory=list)
    surface: pygame.Surface = field(init=False, default=None)

    def __post_init__(self):
        self.surface = pygame.display.set_mode((self.width, self.height))

    def add_objects(self, game_objects: List[GameObject]):
        self.game_objects.extend(game_objects)

    def add_object(self, game_object: GameObject):
        self.game_objects.append(game_object)

    def remove_object(self, game_object: GameObject):
        self.game_objects.remove(game_object)

    def draw(self) -> None:
        self.surface.fill(Colour.BLACK)        
        for game_object in self.game_objects:
            game_object.draw(self.surface)
        pygame.display.update()
