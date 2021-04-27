"""
CS241 - Rock Class for Asteroids
Written by Nolan Meacham

"""

# Import statements
from abc import ABC
from abc import abstractmethod
from flying_objects import FlyingObjects


class Rock(FlyingObjects, ABC):
    """
    Rock Class
    Inherits data from flying objects using the super() command
    Abstract class (ABC)
    """
    def __init__(self):
        super().__init__()

    @abstractmethod
    def draw(self):
        """
        Abstract method, no implementation here.

        """
        pass

    @abstractmethod
    def hit(self):
        """
        Abstract method, no implementation here.

        """
        pass
