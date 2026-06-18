from dataclasses import dataclass
from typing import Tuple

import pygame


@dataclass
class InputState:
    quit: bool
    keys: object
    mouse_delta: Tuple[int, int]


class InputController:
    def __init__(self, display):
        self.center = (display[0] // 2, display[1] // 2)

    def poll(self) -> InputState:
        should_quit = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_quit = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                should_quit = True

        keys = pygame.key.get_pressed()
        pygame.mouse.set_pos(self.center)
        mouse_delta = pygame.mouse.get_rel()
        return InputState(should_quit, keys, mouse_delta)
