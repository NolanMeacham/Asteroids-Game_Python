"""
CS241 - Point Class
Written by Nolan Meacham

This class is used for the x and y values of the center of an object 
to be drawn in the arcade window.

"""


class Point:
    """
    Initialize the x and y to zero. Once an object "has a" point, 
    the x and y values can be changed.

    """
    def __init__(self):
        self.x = 0
        self.y = 0
