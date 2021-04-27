"""
CS241 - Asteroids Game
Written by Nolan Meacham

File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others
This program implements the asteroids game.
"""

# Import statements
import arcade
import random
from globals_asteroids import *
from rock_big import BigRock
from starship_class import Ship
from laser_class import Laser


class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction.
    This class will then call the appropriate functions of
    each of the above classes.

    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game.
        Creates all the variables needed for the game and begins the game
        by creating 5 large asteroids.
        Loads a .png file for the background to be drawn.

        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        self.held_keys = set()

        self.ship = Ship()

        self.lasers = []

        self.rocks = []
        # I begin with 5 big rocks as the description states
        for i in range(5):
            self.rocks.append(BigRock(random.uniform(0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT)))

        self.score = 0
        self.play_game = True

        self.background = arcade.load_texture("images/star_background.png")

    def create_target(self):
        """
        This function is used to create large asteroids. 
        The parameters determine where the large asteroid will spawn at; 
        They will spawn at a random y value along the left side of the screen.
        """
        self.rocks.append(BigRock(0, random.uniform(0, SCREEN_HEIGHT)))

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()
        # Draw the star background image
        arcade.draw_texture_rectangle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, SCREEN_WIDTH,
                                      SCREEN_HEIGHT, self.background)
        # Draw the ship
        self.ship.draw()

        # loop for lasers
        for laser in self.lasers:
            laser.draw()

        # draw the rocks
        for rock in self.rocks:
            rock.draw()

        # This text is used to display the number of asteroids destroyed in
        # the bottom left of screen
        text1 = "Asteroids Destroyed: {}" .format(self.score)
        arcade.draw_text(text1, 20, 20, arcade.color.GREEN_YELLOW, font_size=18)

        # When score is 10 or above, display instructions for rapid fire
        if self.score >= 10:
            text = "Press 'S' for rapid fire"
            arcade.draw_text(text, SCREEN_WIDTH//2 - 100, 30, arcade.color.GREEN_YELLOW, font_size=24)

        # If you crash, display game over and restart instructions
        if not self.play_game:
            text1 = "GAME OVER"
            arcade.draw_text(text1, ((SCREEN_WIDTH//2) - 120), (SCREEN_HEIGHT//2),
                             arcade.color.GREEN_YELLOW, font_size=30)
            text2 = "Press 'R' to restart"
            arcade.draw_text(text2, ((SCREEN_WIDTH//2) - 110), (SCREEN_HEIGHT//2) - 30,
                             arcade.color.GHOST_WHITE, font_size=20)

    def update(self, delta_time):
        """
        Update each object in the game. Begins by checking keys,
        collisions and checking if any objects are off screen.
        If the game is being played, a random number generator is used to 
        create new large asteroids.
        If the user destroys all the asteroids, create 3 new large asteroids.

        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()
        self.check_collisions()
        self.check_off_screen()

        for rock in self.rocks:
            rock.advance()

        for laser in self.lasers:
            laser.duration -= 1
            if laser.duration > 0:
                laser.advance()
            else:
                laser.alive = False

        # Random number generator to periodically create new large asteroid
        if self.play_game:
            if random.randint(0, 200) == 1:
                self.create_target()
            # Only update the ship if the play_game bool is true
            self.ship.advance()

            # Create 3 new asteroids if the list of asteroids is ever zero
            if len(self.rocks) == 0:
                for i in range(3):
                    self.create_target()

    def check_collisions(self):
        """
        This function will check to see if the asteroid has collided with the
        ship or bullets and will call the clean_up_dead function to remove any
        objects that collided.
        """
        # Declare list of additional rocks and hit bool
        add_rocks = []
        hit = False

        # Check for collisions with lasers and asteroids. 
        # If an asteroid is destroyed, the hit function will return a list of 
        # asteroids to be added to the game, and returns a score which is 
        # added to the game score
        for laser in self.lasers:
            for rock in self.rocks:

                # Make sure they are both alive before checking for a collision
                if laser.alive and rock.alive:
                    too_close = laser.radius + rock.radius
                    if (abs(laser.center.x - rock.center.x) < too_close and
                            abs(laser.center.y - rock.center.y) < too_close):
                        # its a hit!
                        laser.alive = False
                        hit = True
                        add_rocks, add_score = rock.hit()
                        self.score += add_score

        # Check for collision with the asteroids and the ship
        for rock in self.rocks:
            if rock.alive and self.ship.alive:
                crash = self.ship.radius + rock.radius

                if (abs(self.ship.center.x - rock.center.x) < crash and
                        abs(self.ship.center.y - rock.center.y) < crash):
                    self.ship.crash()
                    hit = True
                    add_rocks, add_score = rock.hit()
                    self.score -= add_score
                    self.play_game = False

        # If an asteroid is destroyed, hit becomes true and the returned list
        # of new asteroids is added to the game
        if hit:
            self.rocks.extend(add_rocks)
        # Use clean_up_dead function to remove all dead objects
        self.clean_up_dead()

    def clean_up_dead(self):
        """
        If an objects alive boolean is false,
        this function will remove it from the game
        """
        for laser in self.lasers:
            if not laser.alive:
                self.lasers.remove(laser)

        for rock in self.rocks:
            if not rock.alive:
                self.rocks.remove(rock)

    def check_off_screen(self):
        """
        This function is used to wrap the objects around the game screen,
        and calls the wrap_screen for each object
        """
        for rock in self.rocks:
            rock.wrap_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.ship.wrap_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

        for laser in self.lasers:
            laser.wrap_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.rotate_left()

        if arcade.key.RIGHT in self.held_keys:
            self.ship.rotate_right()

        if arcade.key.UP in self.held_keys:
            self.ship.apply_thrust(SHIP_THRUST_AMOUNT)

        if arcade.key.DOWN in self.held_keys:
            if self.ship.speed > 0:
                self.ship.reduce_thrust(self.ship.speed * .05)
            else:
                pass

        # Machine gun mode... Uses the 'S' key after score is greater than 10
        #    I used 10 and 20 as score thresholds to show the feature without 
        #    needing to play long
        if self.score >= 10:
            if arcade.key.S in self.held_keys:
                # if the score is above 20, the ship fires two lasers at once
                #    from the ship wing tips
                if self.score > 20:
                    laser1 = Laser(self.ship.center.x-30, self.ship.center.y, self.ship.angle,
                                   (self.ship.speed + LASER_SPEED))
                    laser2 = Laser(self.ship.center.x+30, self.ship.center.y, self.ship.angle,
                                   (self.ship.speed + LASER_SPEED))
                    laser1.fire(False)
                    laser2.fire(False)
                    laser1.velocity.dx += self.ship.velocity.dx
                    laser1.velocity.dy += self.ship.velocity.dy
                    laser2.velocity.dx += self.ship.velocity.dx
                    laser2.velocity.dy += self.ship.velocity.dy
                    self.lasers.append(laser1)
                    self.lasers.append(laser2)
                # If score is less than 20, fire one laser from the center of the ship
                else:
                    laser = Laser(self.ship.center.x, self.ship.center.y, self.ship.angle,
                                  (self.ship.speed + LASER_SPEED))
                    laser.fire(False)
                    laser.velocity.dx += self.ship.velocity.dx
                    laser.velocity.dy += self.ship.velocity.dy
                    self.lasers.append(laser)

    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        I used the score of 10 to show the feature without needing to play
        very long, I would normally have a larger score needed for the 
        increased firing capacity.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # If the score is above 10, 
                # the ship fires two lasers from the wing tips
                if self.score > 10:
                    laser1 = Laser(self.ship.center.x-30, self.ship.center.y, self.ship.angle,
                                   (self.ship.speed + LASER_SPEED))
                    laser2 = Laser(self.ship.center.x+30, self.ship.center.y, self.ship.angle,
                                   (self.ship.speed + LASER_SPEED))
                    laser1.fire(True)
                    laser2.fire(True)
                    laser1.velocity.dx += self.ship.velocity.dx
                    laser1.velocity.dy += self.ship.velocity.dy
                    laser2.velocity.dx += self.ship.velocity.dx
                    laser2.velocity.dy += self.ship.velocity.dy
                    self.lasers.append(laser1)
                    self.lasers.append(laser2)

                # If score is less than 10, 
                # fire one laser from the center of ship
                else:
                    laser1 = Laser(self.ship.center.x, self.ship.center.y, self.ship.angle,
                                   (self.ship.speed + LASER_SPEED))
                    laser1.fire(True)
                    laser1.velocity.dx += self.ship.velocity.dx
                    self.lasers.append(laser1)

        # If the ship is crashed, the 'R' key is used to restart the game
        if not self.play_game:
            if key == arcade.key.R:
                self.restart()

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)

    def restart(self):
        """
        This function is used to restart the game after the user crashes. 
        It re-initializes the game with the same settings
        in the __init__ function.

        """
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        self.held_keys = set()

        self.ship = Ship()

        self.lasers = []

        self.rocks = []
        # I begin with 5 big rocks as the description states
        for i in range(5):
            self.rocks.append(BigRock(random.uniform(0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT)))

        self.score = 0
        self.play_game = True


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()
