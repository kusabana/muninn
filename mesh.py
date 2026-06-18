import numpy as np
from OpenGL.GL import (
    glVertexPointer,
    glColorPointer,
    glDrawArrays,
    glEnableClientState,
    glDisableClientState,
    glColor3f,
    GL_FLOAT,
    GL_TRIANGLES,
    GL_COLOR_ARRAY,
)
from OpenGL.arrays import vbo


class Mesh:
    def __init__(self, vertices, colors=None):
        self.vbo = vbo.VBO(np.asarray(vertices, dtype="float32"))
        self.color_vbo = (
            vbo.VBO(np.asarray(colors, dtype="float32")) if colors is not None else None
        )
        self.count = len(vertices) // 3

    def draw(self, mode=GL_TRIANGLES, color=None):
        self.vbo.bind()
        glVertexPointer(3, GL_FLOAT, 0, None)

        if color is None and self.color_vbo is not None:
            self.color_vbo.bind()
            glEnableClientState(GL_COLOR_ARRAY)
            glColorPointer(3, GL_FLOAT, 0, None)
        else:
            glDisableClientState(GL_COLOR_ARRAY)
            if color is not None:
                glColor3f(*color)

        glDrawArrays(mode, 0, self.count)
