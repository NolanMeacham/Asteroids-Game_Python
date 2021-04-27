"""
CS241 - Flying Objects Class
Written by Nolan Meacham

This class is used as a base for all flying objects in the game. 
It is an abstract class, using the ABC inheritance. 
The advance function here is used for each of the flying objects. 
The draw method is declared abstract and is implemented in each of 
the specific objects instead of being implemented here.

"""

# Import statements
from abc import ABC
from abc import abstractmethod
from point_class import Point
from velocity_class import Velocity


class FlyingObjects(ABC):
    """
    Abstract class for all flying objects
    (ship, rocks, lasers)
    """
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.radius = 0.0
        self.angle = 0
        self.speed = 0
        self.alive = True

    def advance(self):
        """
        Advances all of the flying objects

        """
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    @abstractmethod
    def draw(self):
        """
        Abstract method, no implementation here.
        """
        pass

    """
    Define the properties (getters and setters) for angle and speed
    """
    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        self._angle = angle % 360

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        if speed > 8:
            self._speed = 8
        else:
            self._speed = speed

    def wrap_screen(self, screen_width, screen_height):
        """
        This function is called for every object in the game. 
        If the object passes beyond the window screen, its x or y position
        will be set to the opposite side of the screen as it continues to advance.
        I used the center.x and center.y plus or minus 20 in each statement so
        that the wrapping looked more smooth.
        """
        if self.center.x < ((0 - self.radius) - 20):
            self.center.x = (screen_width + self.radius + 20)

        if self.center.y < ((0 - self.radius) - 20):
            self.center.y = (screen_height + self.radius + 20)

        if self.center.x > ((screen_width + self.radius) + 20):
            self.center.x = (0 - self.radius - 20)

        if self.center.y > ((screen_height + self.radius) + 20):
            self.center.y = (0 - self.radius - 20)
