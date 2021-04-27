"""
CS241 - Ship class for Asteroids
Written by Nolan Meacham

"""

from globals_asteroids import *
import arcade
from flying_objects import FlyingObjects


class Ship(FlyingObjects):
    """
    Ship class IS A flying object and inherits member data
    from the abstract class.
    """
    def __init__(self):
        """
        Assign member variables
        crash_sound is used to play a sound when ship crashes
        """
        super().__init__()
        self.center.x = (SCREEN_WIDTH // 2)
        self.center.y = (SCREEN_HEIGHT // 2)
        self.radius = SHIP_RADIUS
        self.angle = 90
        self.velocity.calc_velocity(self.angle, 0)
        self.speed = 0
        self.crash_sound = arcade.load_sound("images/crash.wav")

    def draw(self):
        """
        Draw the ship using the .png image
        If the alive bool is True, draw the actual ship
        if  the ship crashes (alive is False) - draw an explosion/fire image
        """
        if self.alive:
            img = "images/X_Wing_Game_Fighter.png"
            texture = arcade.load_texture(img)

            width = texture.width
            height = texture.height

            x = self.center.x
            y = self.center.y
            angle = (self.angle - 90)

            arcade.draw_texture_rectangle(x, y, width, height, texture, angle)

        if not self.alive:
            fire = "images/crash_fire.png"
            texture = arcade.load_texture(fire)

            width = texture.width
            height = texture.height
            x = self.center.x
            y = self.center.y
            angle = 0
            arcade.draw_texture_rectangle(x, y, width, height, texture, angle)

    def apply_thrust(self, thrust):
        """
        Called by the game class
        Increases speed  with 'thrust' parameter and re-calculates velocity
        """
        self.speed += thrust
        self.velocity.calc_velocity(self.angle, self.speed)

    def reduce_thrust(self, thrust):
        """
        Called by the game class
        Decreases speed with 'thrust' parameter and re-calculates velocity
        """
        self.speed -= thrust
        self.velocity.calc_velocity(self.angle, self.speed)

    def rotate_left(self):
        """
        Rotate the ship, but does not calculate velocity
        """
        self.angle += SHIP_TURN_AMOUNT

    def rotate_right(self):
        """
        Rotate the ship, but does not calculate velocity
        """
        self.angle -= SHIP_TURN_AMOUNT

    def crash(self):
        """
        Used to set the ship alive bool to False and trigger the crash sound
        """
        self.alive = False
        arcade.play_sound(self.crash_sound)
