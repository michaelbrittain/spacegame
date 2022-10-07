import pygame


def load_sprite(name, format="png", with_alpha=True) -> pygame.Surface:
    path = f"assets/sprites/{name}.{format}"
    loaded_sprite = pygame.image.load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


def load_sound(name, format="wav") -> pygame.mixer.Sound:
    path = f"assets/sounds/{name}.{format}"
    return pygame.mixer.Sound(path)