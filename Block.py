from ursina import *
from ursina.shaders import lit_with_shadows_shader

#Block class that creates instances of Block entities
class Block(Entity):
    def __init__(self,position,mesh, color):
        super().__init__(
            position = position,
            model = mesh,
            collider = "box",
            scale = 1,
            color = color,
            texture = "white_cube",
            shader = lit_with_shadows_shader
        )