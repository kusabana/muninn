from pygame.locals import *
from OpenGL.GL import (
    glMatrixMode,
    glLoadIdentity,
    glRotatef,
    glTranslatef,
    GL_PROJECTION,
    GL_MODELVIEW,
)
from OpenGL.GLU import gluPerspective
from math import sin, cos, radians
import pygame


class Camera:
    def __init__(self, display, origin):
        self.position = list(origin)
        self.rotation = [0, 0]
        self.move_speed = 1.5
        self.rotate_speed = 0.15

        # setup perspective
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (display[0] / display[1]), 10.0, 35000.0)
        glMatrixMode(GL_MODELVIEW)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_rel()
        pygame.mouse.set_pos(500, 500)  # TODO: set to display center

        strafe_sin = self.move_speed * sin(radians(self.rotation[1]))
        strafe_cos = self.move_speed * cos(radians(self.rotation[1]))
        move_vectors = {
            K_w: [
                strafe_sin,
                strafe_cos,
                -self.move_speed * sin(radians(self.rotation[0])),
                # TODO: something is wrong with this with |angle| >45 , but it works for now
            ],
            K_s: [
                -strafe_sin,
                -strafe_cos,
                self.move_speed * sin(radians(self.rotation[0])),
                # TODO: something is wrong with this with |angle| >45, but it works for now
            ],
            K_a: [
                -strafe_cos,
                strafe_sin,
                0,
            ],
            K_d: [
                strafe_cos,
                -strafe_sin,
                0,
            ],
            K_SPACE: [0, 0, self.move_speed],
            K_LCTRL: [0, 0, -self.move_speed],
        }

        for key, vector in move_vectors.items():
            if keys[key]:
                self.position = [sum(x) for x in zip(self.position, vector)]

        # clamp rotational values
        self.rotation[0] = max(-90, min(self.rotation[0] - (mouse[1] * self.rotate_speed), 90))
        self.rotation[1] = max(-180, min(self.rotation[1] - (mouse[0] * self.rotate_speed), 180))

        glLoadIdentity()
        
        # somewhat of a stupid solution... (but it works!)
        glRotatef(-90 + self.rotation[0], 1, 0, 0)
        glRotatef(180 + self.rotation[1], 0, 0, 1)

        glTranslatef(-self.position[0], -self.position[1], -self.position[2])
