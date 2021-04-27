"""
CS241 - Velocity class
Written by Nolan Meacham

This class will be used by the flying object class. 
It is used to determine how much to increase an object's x and y
values every frame refresh.

"""
import math


class Velocity:
    """
    Initializes the dx and dy to zero

    """
    def __init__(self):
        self.dx = 0.0
        self.dy = 0.0

    def calc_velocity(self, angle, speed):
        """
        Used to calculate the velocity of an object
        """
        self.dx = math.cos(math.radians(angle)) * speed
        self.dy = math.sin(math.radians(angle)) * speed
