import pygame
from typing import List
from dataclasses import dataclass, field
from models import GameObject
from colour import Colour


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
