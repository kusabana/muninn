#!/usr/bin/python3
import sys
import os
from OpenGL.GL import *
from OpenGL.arrays import vbo
import numpy as np


os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from pygame.locals import *

from camera import Camera
from map import Map

if len(sys.argv) <= 1:
    print("usage:\n\t./muninn.py <map.bsp>")

mp = Map(sys.argv[1])
print(f". loaded {mp.bsp}")
print(". performing face triangulation...")
vertices, colors = mp.triangulate_faces_flat()

print(
    f". face triangulation done ({sum(len(vert) for vert in mp.faces)} -> {len(vertices)})"
)

# initialize pygame
pygame.init()
display = (1600, 900)
pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
pygame.display.set_caption(f"muninn - {mp.bsp}")

entities = mp.get_entities_flat()
spawn = mp.get_spawns()[0]

# add a bit of height to spawn
spawn = (spawn[0], spawn[1], spawn[2] + 64)
camera = Camera(display, spawn)

# enable depth testing
glEnable(GL_DEPTH_TEST)

glEnable(GL_POINT_SMOOTH)
glPointSize(5)

# define buffers
vertex_vbo = vbo.VBO(np.array(vertices, dtype="float32"))
color_vbo = vbo.VBO(np.array(colors, dtype="float32"))
entities_vbo = vbo.VBO(np.array(entities, dtype="float32"))

while True:
    glPushMatrix()
    camera.update()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnableClientState(GL_VERTEX_ARRAY)

    # draw entitites
    entities_vbo.bind()
    glVertexPointer(3, GL_FLOAT, 0, None)
    glColor3f(1.0, 1.0, 1.0)
    glDrawArrays(GL_POINTS, 0, int(len(entities) / 3))

    # push vertex vbo
    vertex_vbo.bind()
    glVertexPointer(3, GL_FLOAT, 0, None)

    # line overlay
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glColor3f(1.0, 1.0, 1.0)
    glDrawArrays(GL_TRIANGLES, 0, int(len(vertices) / 3))

    # push color vbo
    color_vbo.bind()
    glEnableClientState(GL_COLOR_ARRAY)
    glColorPointer(3, GL_FLOAT, 0, None)

    # triangles
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glDrawArrays(GL_TRIANGLES, 0, int(len(vertices) / 3))

    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_COLOR_ARRAY)
    glPopMatrix()
    pygame.display.flip()
