from math import sin, cos, radians

from OpenGL.GL import glLoadIdentity, glRotatef, glTranslatef
from pygame.locals import K_w, K_s, K_a, K_d, K_SPACE, K_LCTRL


class Camera:
    def __init__(self, origin, move_speed=90.0, rotate_speed=0.15):
        self.position = list(origin)
        self.rotation = [-90.0, 180.0]
        self.move_speed = move_speed
        self.rotate_speed = rotate_speed

    def update(self, state, dt):
        step = self.move_speed * dt
        pitch = radians(self.rotation[0])
        yaw = radians(self.rotation[1])

        move_vectors = {
            K_w: [
                -step * sin(yaw) * sin(pitch),
                -step * cos(yaw) * sin(pitch),
                -step * cos(pitch),
            ],
            K_s: [
                step * sin(yaw) * sin(pitch),
                step * cos(yaw) * sin(pitch),
                step * cos(pitch),
            ],
            K_a: [-step * cos(yaw), step * sin(yaw), 0],
            K_d: [step * cos(yaw), -step * sin(yaw), 0],
            K_SPACE: [0, 0, step],
            K_LCTRL: [0, 0, -step],
        }

        for key, vector in move_vectors.items():
            if state.keys[key]:
                self.position = [sum(c) for c in zip(self.position, vector)]

        self.rotation[0] += state.mouse_delta[1] * self.rotate_speed
        self.rotation[1] += state.mouse_delta[0] * self.rotate_speed

    def apply(self):
        glLoadIdentity()
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 0, 1)
        glTranslatef(-self.position[0], -self.position[1], -self.position[2])
