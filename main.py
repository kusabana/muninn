#!/usr/bin/python3
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import sys
import argparse

import pygame

from camera import Camera
from controls import InputController
from map import Map
from renderer import Renderer
from scene import Scene

TARGET_FPS = 60


class App:
    def __init__(self, world_map, title, display=(1600, 900)):
        self.display = display
        self.map = world_map

        self._init_window(title)
        self.renderer = Renderer(display)

        self.scene = Scene.from_map(self.map)
        print(f"face triangulation done ({self.scene.world.count} vertices)")

        self.camera = Camera((0.0, 0.0, 0.0))
        self.input = InputController(display)

    def _init_window(self, title):
        pygame.init()
        pygame.display.set_mode(self.display, pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption(f"muninn - {title}")
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        try:
            while running:
                dt = clock.tick(TARGET_FPS) / 1000.0
                state = self.input.poll()
                if state.quit:
                    running = False
                    continue
                self.camera.update(state, dt)
                self.renderer.draw(self.scene, self.camera)
        finally:
            pygame.quit()


def main():
    parser = argparse.ArgumentParser(description="muninn - Source Engine BSP Viewer")
    parser.add_argument("map", help="path to the .bsp map file")
    args = parser.parse_args()

    if not os.path.isfile(args.map):
        print(f"error: file not found: {args.map}", file=sys.stderr)
        sys.exit(1)

    try:
        world_map = Map(args.map)
    except Exception as e:
        print(f"error: failed to load BSP '{args.map}': {e}", file=sys.stderr)
        sys.exit(1)

    print(f"loaded {args.map}")
    App(world_map, args.map).run()


if __name__ == "__main__":
    main()
