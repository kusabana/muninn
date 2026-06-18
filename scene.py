from dataclasses import dataclass

from OpenGL.GL import GL_POINTS, GL_TRIANGLES

from map import Map
from mesh import Mesh

WHITE = (1.0, 1.0, 1.0)


@dataclass
class Scene:
    world: Mesh
    entities: Mesh

    @classmethod
    def from_map(cls, world_map: Map) -> "Scene":
        vertices, colors = world_map.triangulate_faces_flat()
        return cls(
            world=Mesh(vertices, colors),
            entities=Mesh(world_map.get_entities_flat()),
        )

    def draw(self):
        self.entities.draw(GL_POINTS, color=WHITE)
        self.world.draw(GL_TRIANGLES)
