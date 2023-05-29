#!/usr/bin/python3
import sys
import os
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective
from OpenGL.arrays import vbo
import numpy as np

try:  # local copy, temporary until author fixes their library...
    import bsp_tool.bsp_tool as bsp_tool
except:
    import bsp_tool

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame


class Camera:
    def __init__(self, display):
        self.tx = 0
        self.ty = 0
        self.tz = 0

        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (display[0] / display[1]), 0.1, 75000.0)

        self.view = np.matrix(np.identity(4), copy=False, dtype="float32")
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glGetFloatv(GL_MODELVIEW_MATRIX, self.view)
        glLoadIdentity()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_a:
                    self.tx = 0.1
                elif event.key == pygame.K_d:
                    self.tx = -0.1
                elif event.key == pygame.K_w:
                    self.tz = 0.1
                elif event.key == pygame.K_s:
                    self.tz = -0.1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a and self.tx > 0:
                    self.tx = 0
                elif event.key == pygame.K_d and self.tx < 0:
                    self.tx = 0
                elif event.key == pygame.K_w and self.tz > 0:
                    self.tz = 0
                elif event.key == pygame.K_s and self.tz < 0:
                    self.tz = 0

        glLoadIdentity()
        glTranslatef(self.tx * 20, self.ty * 20, self.tz * 20)
        mouseMove = pygame.mouse.get_rel()
        glRotatef(mouseMove[0] * 0.15, 0.0, 1.0, 0.0)
        glRotatef(mouseMove[1] * 0.15, 1.0, 0.0, 0)
        glMultMatrixf(self.view)
        glGetFloatv(GL_MODELVIEW_MATRIX, self.view)


if len(sys.argv) <= 1:
    print("usage:\n\t./muninn.py <map.bsp>")

map_file = sys.argv[1]
bsp = bsp_tool.load_bsp(map_file)

print(f". loaded {bsp}")
print(". performing face triangulation...")

polygons = [
    [((vert[0].x, vert[0].y, vert[0].z), vert[4]) for vert in bsp.vertices_of_face(x)]
    for x in range(len(bsp.FACES))
]
vertices, colors = zip(
    *[
        (v, c)
        for p in polygons
        for tri in [(p[0], b, c) for b, c in zip(p[1:], p[2:])]
        for vertex, color in tri
        for v, c in zip(vertex, color)
    ]
)

print(
    f". face triangulation done ({sum(len(poly) for poly in polygons)} -> {len(vertices)})"
)

pygame.init()
display = (1600, 900)
pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
pygame.display.set_caption(f"muninn - {bsp}")

camera = Camera(display)

glClearDepth(1.0)
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LEQUAL)
glShadeModel(GL_SMOOTH)

# define buffers
vertex_vbo = vbo.VBO(np.array(vertices, dtype="float32"))
color_vbo = vbo.VBO(np.array(colors, dtype="float32"))

while True:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    camera.update()

    vertex_vbo.bind()
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, None)

    # lines
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glColor3f(1.0, 1.0, 1.0)
    glDrawArrays(GL_TRIANGLES, 0, int(len(vertices) / 3))

    color_vbo.bind()
    glEnableClientState(GL_COLOR_ARRAY)
    glColorPointer(3, GL_FLOAT, 0, None)

    # tris
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glDrawArrays(GL_TRIANGLES, 0, int(len(vertices) / 3))

    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_COLOR_ARRAY)
    glPopMatrix()

    pygame.display.flip()
