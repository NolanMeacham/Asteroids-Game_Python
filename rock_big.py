"""
CS241
Written by Nolan Meacham

"""

# Import statements
import arcade
import random
from globals_asteroids import *
from rocks import Rock
from rock_medium import MedRock
from rock_small import SmallRock


class BigRock(Rock):
    """
    BigRock Class
    Inherits data from Rock using the super() command

    """
    def __init__(self, x, y):
        super().__init__()
        self.center.x = x
        self.center.y = y
        self.radius = BIG_ROCK_RADIUS
        self.angle = random.uniform(0, 360)
        self.velocity.calc_velocity(self.angle, BIG_ROCK_SPEED)
        self.rotate = 0
        self.rock_sound = arcade.load_sound("images/rock.wav")

    def draw(self):
        """
        Draw the large asteroid using the .png file
        """
        img = "images/meteorGrey_big1.png"
        texture = arcade.load_texture(img)

        width = texture.width
        height = texture.height

        x = self.center.x
        y = self.center.y
        rotate = self.rotate

        arcade.draw_texture_rectangle(x, y, width, height, texture, rotate)

    def advance(self):
        """
        overrides the advance function in the generic rock class
        adds the rotate to the asteroid so that it spins as it moves across the screen
        """
        super().advance()
        self.rotate += BIG_ROCK_SPIN

    def hit(self):
        """
        Used when a laser hits the asteroid.
        This function returns a list of new asteroids to create and a number
        used to keep track of the score.
        """
        self.alive = False
        arcade.play_sound(self.rock_sound)
        rocks = [MedRock(self.center.x, self.center.y, self.angle, 2),
                 MedRock(self.center.x, self.center.y, self.angle, -2),
                 SmallRock(self.center.x, self.center.y, self.angle, 0, 5)]

        return rocks, 1
