"""
CS241
Written by Nolan Meacham

"""

# Import statements
import arcade
from globals_asteroids import *
from rocks import Rock
from rock_small import SmallRock


class MedRock(Rock):
    """
    MedRock Class
    Inherits data from Rock using the super() command

    """
    def __init__(self, x, y, angle, vert):
        """
        Assign member variables
        'vert' parameter is used to increase the vertical velocity of the asteroid
        """
        super().__init__()
        self.center.x = x
        self.center.y = y
        self.radius = MEDIUM_ROCK_RADIUS
        self.angle = angle
        self.velocity.calc_velocity(self.angle, BIG_ROCK_SPEED)
        self.velocity.dy += vert
        self.rotate = 0

    def draw(self):
        """
        Draws the medium asteroid using the .png image
        """
        img = "images/meteorGrey_med1.png"
        texture = arcade.load_texture(img)

        width = texture.width
        height = texture.height

        x = self.center.x
        y = self.center.y
        rotate = self.rotate

        arcade.draw_texture_rectangle(x, y, width, height, texture, rotate)

    def advance(self):
        """
        overrides the advance function and adds rotation to the asteroid
        """
        super().advance()
        self.rotate += MEDIUM_ROCK_SPIN

    def hit(self):
        """
        Called when a collision occurs
        Returns a list of new asteroids to create and a number to be used to keep score

        """
        self.alive = False
        rocks = [SmallRock(self.center.x, self.center.y, self.angle, 1.5, 1.5),
                 SmallRock(self.center.x, self.center.y, self.angle, -2.5, -1.5)]
        return rocks, 1
