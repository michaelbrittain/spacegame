import pygame


def load_sprite(name, with_alpha=True) -> pygame.Surface:
    path = f"assets/sprites/{name}.png"
    loaded_sprite = pygame.image.load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


def load_sound(name) -> pygame.mixer.Sound:
    path = f"assets/sounds/{name}.wav"
    return pygame.mixer.Sound(path)