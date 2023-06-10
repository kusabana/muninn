#!/usr/bin/python3
import sys
import os
from OpenGL.GL import *
from OpenGL.arrays import vbo
import numpy as np

try:  # local copy, temporary until author fixes their library...
    import bsp_tool.bsp_tool as bsp_tool
except:
    import bsp_tool

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from pygame.locals import *
from camera import Camera

if len(sys.argv) <= 1:
    print("usage:\n\t./muninn.py <map.bsp>")

map_file = sys.argv[1]
bsp = bsp_tool.load_bsp(map_file)

print(f". loaded {bsp}")
print(". performing face triangulation...")
faces = [
    [((vert[0].x, vert[0].y, vert[0].z), vert[4]) for vert in bsp.vertices_of_face(x)]
    for x in range(len(bsp.FACES))
]
vertices, colors = zip(
    *[
        (v, c)
        for face in faces
        for tri in [(face[0], b, c) for b, c in zip(face[1:], face[2:])]
        for vertex, color in tri
        for v, c in zip(vertex, color)
    ]
)

print(
    f". face triangulation done ({sum(len(vert) for vert in faces)} -> {len(vertices)})"
)

# initialize pygame
pygame.init()
display = (1600, 900)
pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
pygame.display.set_caption(f"muninn - {bsp}")

entities = [
    coord
    for entity in bsp.ENTITIES
    if "origin" in entity
    for coord in list(map(float, entity["origin"].split(" ")))
]

spawns = [
    entity for entity in bsp.ENTITIES if entity["classname"].startswith("info_player_")
]
spawn = tuple(map(float, spawns[0]["origin"].split(" ")))

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
