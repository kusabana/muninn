import pygame
from OpenGL.GL import (
    glEnable,
    glClear,
    glClearColor,
    glPushMatrix,
    glPopMatrix,
    glPointSize,
    glMatrixMode,
    glEnableClientState,
    glDisableClientState,
    GL_DEPTH_TEST,
    GL_POINT_SMOOTH,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_PROJECTION,
    GL_MODELVIEW,
    GL_VERTEX_ARRAY,
    GL_COLOR_ARRAY,
)
from OpenGL.GLU import gluPerspective


class Renderer:
    def __init__(self, display, fov=45.0, near=10.0, far=65000.0, point_size=5):
        glMatrixMode(GL_PROJECTION)
        gluPerspective(fov, display[0] / display[1], near, far)
        glMatrixMode(GL_MODELVIEW)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_POINT_SMOOTH)
        glPointSize(point_size)
        glClearColor(0.0, 0.0, 0.0, 1.0)

    def draw(self, scene, camera):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnableClientState(GL_VERTEX_ARRAY)

        glPushMatrix()
        camera.apply()
        scene.draw()
        glPopMatrix()

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        pygame.display.flip()
