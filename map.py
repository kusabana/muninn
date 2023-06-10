import bsp_tool
from bsp_tool.branches import vector
import math


class Map:
    def __init__(self, file: str):
        self.bsp = bsp_tool.load_bsp(file)
        self.faces = [
            [
                ((vert[0].x, vert[0].y, vert[0].z), vert[1])
                for vert in self.vertices_of_face(x)
            ]
            for x in range(len(self.bsp.FACES))
        ]

    # we reconstruct the bsp_tool function as
    # there are several flaws with it.
    def vertices_of_face(self, face_index: int):
        face = self.bsp.FACES[face_index]
        vertices = self.bsp.VERTICES
        edges = self.bsp.EDGES
        surfedges = self.bsp.SURFEDGES[
            face.first_edge : face.first_edge + face.num_edges
        ]

        positions = [
            vertices[edges[surfedge][0]]
            if surfedge >= 0
            else vertices[edges[-surfedge][1]]
            for surfedge in surfedges
        ]

        texture_info = self.bsp.TEXTURE_INFO[face.texture_info]
        texture_data = self.bsp.TEXTURE_DATA[texture_info.texture_data]
        colour = [texture_data.reflectivity] * len(positions)

        return list(zip(positions, colour))

    def triangulate_faces(
        self,
    ) -> list[tuple[float, float, float], tuple[float, float, float]]:
        return zip(
            *[
                (vertex, color)
                for face in self.faces
                for tri in [(face[0], b, c) for b, c in zip(face[1:], face[2:])]
                for vertex, color in tri
            ]
        )

    def triangulate_faces_flat(self) -> tuple[list[float], list[float]]:
        return zip(
            *[
                (v, c)
                for vertex, color in zip(*self.triangulate_faces())
                for v, c in zip(vertex, color)
            ]
        )

    def get_entities(self) -> list[tuple[float, float, float]]:
        return [
            self.convert_coord(entity["origin"])
            for entity in self.bsp.ENTITIES
            if "origin" in entity
        ]

    def get_entities_flat(self) -> list[float]:
        return [coord for entity in self.get_entities() for coord in entity]

    def get_spawns(self) -> list[tuple[float, float, float]]:
        return [
            self.convert_coord(entity["origin"])
            for entity in self.bsp.ENTITIES
            if entity["classname"].startswith("info_player_")
        ]

    # converts "75 2 81" to tuple(75, 2, 81)
    def convert_coord(self, str) -> tuple[float, float, float]:
        return tuple(map(float, str.split(" ")))
