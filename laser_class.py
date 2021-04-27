"""
CS241 - Laser Class
Written by Nolan Meacham

"""

# Import statements.
import arcade
from globals_asteroids import *
from flying_objects import FlyingObjects


class Laser(FlyingObjects):
    """
    Inherits data from flying objects, using the super() command
    Defines the bullet radius using the global declaration

    """

    def __init__(self, x, y, angle, speed):
        """
        Declare and assign each member variable
        laser_sound is used to play the .wav sound file when the 
        fire command is used, self.color is used to determine which 
        color of laser to fire.
        """
        super().__init__()
        self.center.x = x
        self.center.y = y
        self.radius = LASER_RADIUS
        self.speed = speed
        self.duration = LASER_LIFE
        self.angle = angle
        self.laser_sound = arcade.load_sound("images/laser11.wav")
        self.color = 0

    def draw(self):
        """
        Draws each laser

        """
        # Two different images are used, blue for regular firing, 
        # red for rapid fire
        blue = "images/laser_blue.png"
        texture_blue = arcade.load_texture(blue)
        red = "images/laser_red.png"
        texture_red = arcade.load_texture(red)

        width = texture_blue.width
        height = texture_blue.height

        x = self.center.x
        y = self.center.y
        angle = self.angle

        # If statement used to determine which image/color laser to draw
        if self.color == 0:
            arcade.draw_texture_rectangle(x, y, width, height, texture_blue, angle)
        else:
            arcade.draw_texture_rectangle(x, y, width, height, texture_red, angle)

    def fire(self, sound):
        """
        The cos and sin math functions are used here for the bullet velocity. 
        It is dependent on the (x, y) of the mouse pointer when the bullet is 
        created which becomes the angel used from the parameter.
        The 'sound' parameter is used to determine whether the sound should be
        played or not. I did this so that when the user uses rapid fire, 
        it does not play the sound - it is annoying otherwise. 
        It is also used to change the color of laser being used in
        the draw function.
        """
        self.velocity.calc_velocity(self.angle, self.speed)
        if sound == True:
            self.color = 0
            arcade.play_sound(self.laser_sound)
        else:
            self.color = 1
