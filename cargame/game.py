import pygame
from typing import Protocol, List
from colour import Colour
from utils import load_sprite
from models import Car


class Drawable(Protocol):
    def draw(self, surface: pygame.Surface):
        ...    


class CarGame:
    def __init__(self) -> None:
        self._init_pygame()
        self.player = Car()

    def _init_pygame(self) -> None:
        pygame.init()
        pygame.display.set_caption("Car Game")
        self.screen = pygame.display.set_mode((1200, 900))
        self.clock = pygame.time.Clock()

    @property
    def _drawable_objects(self) -> List[Drawable]:
        return [self.player]

    def play(self) -> None:
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        self.player.move(pygame.key.get_pressed())

    def _process_game_logic(self) -> None:
        pass

    def _draw(self) -> None:
        self.screen.fill((Colour.BLACK))
        for drawable_object in self._drawable_objects:
            drawable_object.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)
