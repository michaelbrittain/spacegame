import pygame
from pygame.math import Vector2
from utils import load_sprite

SPEED = 2
ROTATION_SPEED = 2


class Car:
    def __init__(self):
        self.sprite: pygame.surface = load_sprite("car")
        self.position: Vector2 = Vector2(200, 100)
        self.direction: Vector2 = Vector2(SPEED, 0)

    def move(self,  pressed_keys: dict):
        if pressed_keys[pygame.K_UP]:
            self.position += self.direction
        if pressed_keys[pygame.K_DOWN]:
            self.position -= self.direction
        if pressed_keys[pygame.K_LEFT]:
            self.direction.rotate_ip(-ROTATION_SPEED)
        if pressed_keys[pygame.K_RIGHT]:
            self.direction.rotate_ip(ROTATION_SPEED)

    def draw(self, surface: pygame.Surface):
        angle = self.direction.angle_to((1, 0))
        rotated_sprite = pygame.transform.rotate(self.sprite, angle)
        surface.blit(rotated_sprite, rotated_sprite.get_rect(center = (round(self.position.x), round(self.position.y))))
