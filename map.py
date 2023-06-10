import bsp_tool
from bsp_tool.branches import vector
import math


class Map:
    def __init__(self, file: str):
        self.bsp = bsp_tool.load_bsp(file)
        self.faces = [
            [
                ((vert[0].x, vert[0].y, vert[0].z), vert[2])
                for vert in self.vertices_of_face(x)
            ]
            for x in range(len(self.bsp.FACES))
        ]

    # we reconstruct the bsp_tool function as
    # there are several flaws with it.
    def vertices_of_face(self, face_index: int):
        face = self.bsp.FACES[face_index]
        first_edge = face.first_edge
        positions = []
        for surfedge in self.bsp.SURFEDGES[first_edge : (first_edge + face.num_edges)]:
            if surfedge >= 0:
                positions.append(self.bsp.VERTICES[self.bsp.EDGES[surfedge][0]])
            else:
                positions.append(self.bsp.VERTICES[self.bsp.EDGES[-surfedge][1]])
        texture_info = self.bsp.TEXTURE_INFO[face.texture_info]
        texture_data = self.bsp.TEXTURE_DATA[texture_info.texture_data]

        normal = [self.bsp.PLANES[face.plane].normal] * len(positions)
        colour = [texture_data.reflectivity] * len(positions)
        return list(zip(positions, normal, colour))

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
