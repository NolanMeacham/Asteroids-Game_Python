"""
CS241 - Special Target class for Asteroids
Written by Nolan Meacham

"""

import arcade
from rocks import Rock
from globals_asteroids import*
import random


class Special(Rock):
    """
    Special Target Class
    Inherits data from Rock using the super() command

    """
    def __init__(self, x, y, angle, vert, horiz):
        """
        Assign member variables
        'vert' and 'horiz' are used to change the velocities of the target

        """
        super().__init__()
        self.center.x = x
        self.center.y = y
        self.radius = MEDIUM_ROCK_RADIUS
        self.angle = angle
        self.velocity.calc_velocity(self.angle, BIG_ROCK_SPEED)
        self.velocity.dx += horiz
        self.velocity.dy += vert
        self.rotate = 0

    def draw(self):
        """
        Draws the special target with .png image
        """
        img = "images/secret_target.png"
        texture = arcade.load_texture(img)

        width = texture.width
        height = texture.height

        x = self.center.x
        y = self.center.y
        rotate = self.rotate

        arcade.draw_texture_rectangle(x, y, width, height, texture, rotate)

    def advance(self):
        """
        Overrides the advance function
        Creates a random number every time this function is called,
        if the number is 1 or 15, multiply the x or y velocity by -1
        This results in the target moving across the screen unpredictably,
        instead of in a straight line like the asteroids.
        """
        super().advance()
        change_angle = random.randint(1, 30)
        if change_angle == 1:
            self.velocity.dx *= -1
        elif change_angle == 15:
            self.velocity.dy *= -1
        else:
            pass

    def hit(self):
        """
        Called if the special target is destroyed
        Returns an empty list and 2 points for score
        """
        self.alive = False
        return [], 2
