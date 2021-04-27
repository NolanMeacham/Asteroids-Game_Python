"""
CS241
Written by Nolan Meacham

"""

# Import statements
import arcade
import random
from globals_asteroids import *
from rocks import Rock
from special_asteroid import Special


class SmallRock(Rock):
    """
    BigRock Class
    Inherits data from Rock using the super() command

    """
    def __init__(self, x, y, angle, vert, horiz):
        """
        Assign member variables
        'vert' and 'horiz' parameters are used to change the asteroids vertical
        and horizontal velocity.

        self.special_target is a random number used to determine whether the
        small asteroid will create a new target or not when it is destroyed.
        """
        super().__init__()
        self.center.x = x
        self.center.y = y
        self.radius = SMALL_ROCK_RADIUS
        self.angle = angle
        self.velocity.calc_velocity(self.angle, BIG_ROCK_SPEED)
        self.velocity.dx += horiz
        self.velocity.dy += vert
        self.rotate = 0
        self.special_target = random.randint(1, 15)

    def draw(self):
        """
        Draw the small asteroid using the .png image
        """
        img = "images/meteorGrey_small1.png"
        texture = arcade.load_texture(img)

        width = texture.width
        height = texture.height

        x = self.center.x
        y = self.center.y
        rotate = self.rotate

        arcade.draw_texture_rectangle(x, y, width, height, texture, rotate)

    def advance(self):
        """
        Overrides the advance function and adds rotation
        """
        super().advance()
        self.rotate += SMALL_ROCK_SPIN

    def hit(self):
        """
        Called when a collision occurs
        if the special_target random number is 1, returns a special target to
        be added to the game list of asteroids and returns a number to keep score.
        If random number is not 1, returns an empty list and a number to keep score
        """
        self.alive = False
        if self.special_target == 1:
            special = [Special(self.center.x, self.center.y, self.angle, -5, 5)]
            return special, 1
        else:
            return [], 1
