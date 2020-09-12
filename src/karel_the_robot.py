"""

##Importing##
>When karel_the_robot.py is in the same path as your code

>>
    from karel_the_robot import World, Robot

>When karel_the_robot.py is a in a subdirectory

>>
    from subdir.karel_the_robot import World, Robot


##Creating Custom Methods##
>To create custom methods, follow this format:

>>
    @Robot.add_method(Robot)
    def method_name(Robot):
        # Custom code goes here

>Everything shown above (except for the comment) must be present for the custom method to work.

>Within this new method, "Robot" can be used to call methods on the Robot using this method, as seen in the example below:

>>
    @Robot.add_method(Robot)
    def move_twice(Robot):
        Robot.move()
        Robot.move()

>Multiple methods can be created by giving each one a full header, as seen in the example below:

>>
    @Robot.add_method(Robot)
    def move_twice(Robot):
        Robot.move()
        Robot.move()
>>
    @Robot.add_method(Robot)
    def move_thrice(Robot):
        Robot.move()
        Robot.move()
        Robot.move()

>Parameters can be added after the required "Robot" parameter, as seen in the example below:

>>
    @Robot.add_method(Robot)
    def move_if_true(Robot, true_or_false):
        if true_or_false == True:
            Robot.move()

>If the resulting method is called on a Robot, the "Robot" parameter will be automatically filled, as seen in the example below:

>>
    karel = Robot(0, 0, 0, 0)
    karel.move_if_true(True)
>>
    # Result: karel moves once.

>Methods are added to all members of the Robot class, as seen in the example below:

>>
    @Robot.add_method(Robot)
    def move_twice(Robot):
        Robot.move()
        Robot.move()
>>
    karel = Robot(0, 0, 0, 0)
    warel = Robot(1, 1, 0, 0)
>>
    karel.move_twice()
    warel.move_twice()
>>
    # Result: karel and warel both move twice.

>**IMPORTANT:** ```Robot.add_method()``` is itself a method. This means that custom methods can only be used after their creation.

>To put it simply, this code **works**:

>>
    @Robot.add_method(Robot)
    def move_twice(Robot):
        Robot.move()
        Robot.move()
>>
    karel = Robot(0, 0, 0, 0)
    karel.move_twice()

>And this code **doesn't work**:

>>
    karel = Robot(0, 0, 0, 0)
    karel.move_twice()
>>
    @Robot.add_method(Robot)
    def move_twice(Robot):
        Robot.move()
        Robot.move()

##Using Worlds within Code##
>There are multiple ways to create a World, as documented [here](#karel_the_robot.World).

>To add Robots to a World, use [```World.add_robots()```](#karel_the_robot.World.add_robots)

>Once all Robots are added, call [```World.start()```](#karel_the_robot.World.start)

>All code to be executed while the World is running should be placed below this line, as seen in the example below:

>>
    world = World.from_file("example_world.txt")
    karel = Robot(1, 1, 0, 0)
    world.add_robots(karel)
    world.start()
>>
    karel.move()
    karel.turn_left()

>Worlds automatically stop when:

>* all Robots have turned off

>* no methods have been called on any Robot for 1 second

>In the event that a World stops too quickly and you are unable to see the end state, look for a file named "final_world_status.jpg". This is a screenshot of the world right before it ended.

##Setting up World Files##
>World files should be located in the same directory as your code.
>A World file consists of parameters and values.
>General formatting is as follows:

>>
    parameter1: value
    parameter2: value
    ...

>**IMPORTANT:** Strings and chars should **NOT** be quoted!

>The following is a list of parameters and their specific formatting:

>>###Required Parameters:###
* **size** the width and height in tiles of the World
    * Formatting: ```size: (w h)```
    * **w (int)** the width in tiles of the World
        * ```0 < w```
    * **h (int)** the height in tiles of the World
        * ```0 < h```

>>###Optional Parameters:###
* **beepers** the positions of Beepers in the World
    * Formatting: ```beepers: (x y n) (x y n) (x y n)...```
    * **x (int)** the x position of the Beeper cluster
        * ```0 <= x < World.width```
    * **y (int)** the y position of the Beeper cluster
        * ```0 <= y < World.height```
    * **n (int)** the number of Beepers in the Beeper cluster
        * ```0 < n```
* **walls** the positions of Walls in the World
    * Formatting: ```walls: (o sx sy ev) (o sx sy ev) (o sx sy ev)...```
    * **o (char)** ```h``` if the Wall is horizontal, ```v``` if the Wall is vertical
        * ```o == {h, v}```
    * **sx (int)** the starting x position of the Wall
        * ```0 <= sx < World.width```
    * **sy (int)** the starting y position of the Wall
        * ```0 <= sy < World.height```
    * **sy (int)** the ending x position of the Wall if ```o == h```, the ending y position of the Wall if ```o == v```
* **name** the window name of the World
    * Formatting: ```name: n```
    * **n (str)** the window name of the World
    * Default: ```Karel J Robot```
* **fps** the FPS of the World
    * Formatting: ```fps: fps```
    * **fps (int)** the FPS of the World
    * Default: ```4```

>The following is an example World file:

>>
    name: Example World
    fps: 5
    size: (10 9)
    beepers: (5 3 1) (2 6 8)
    walls: (h 1.5 2.5 8.5) (v 4.5 3.5 7.5)

>This file will produce the following World:

>>![Example World Screenshot](https://cjbell630.github.io/example-world.jpg)

##Future Plans##
* Add all possible error messages (most are present, but not all)
* Figure out a clean way to show Robot movements in the console (such as "[Green Robot] Moved once")
* Add a legacy mode for Java Karel world files
* Get the zoom feature working
* Get the global movement variable working
* Add more objects for Robots to interact with (ex rotating gears)


---

"""

import numpy
import threading
import time
import traceback
import os
from functools import wraps
from itertools import count

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

import sentry_sdk

sentry_sdk.init(
    "https://5ccc0b1af0ce423abb24c4a306a238f6@o446990.ingest.sentry.io/5426981",
    traces_sample_rate=1.0
)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
TILE_WIDTH = 10
# TODO: maybe make has moved this frame a global
FPS = 4

BEEPERS = pygame.sprite.Group()
WALLS = []

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
L_GREY = (158, 158, 158)
D_GREY = (56, 56, 56)
GREEN = (91, 153, 0)
RED = (240, 0, 0)
L_BLUE = (0, 124, 150)
D_BLUE = (34, 25, 117)
YELLOW = (255, 236, 0)
CLR = (1, 1, 1)
ORANGE = (255, 165, 0)
PINK = (255, 165, 245)
TEAL = (0, 160, 180)
PURPLE = (200, 0, 255)

SLEEVE_COLORS = [
    ("Green", GREEN), ("Orange", ORANGE), ("Pink", PINK), ("Blue", TEAL), ("Purple", PURPLE)
]

DIRECTIONS = {
    "North": 90,
    "South": 270,
    "East": 0,
    "West": 180
}

KAREL_ON = numpy.array([
    [CLR, CLR, CLR, CLR, CLR, CLR, BLACK, BLACK, BLACK, BLACK, CLR, CLR, CLR, BLACK, BLACK, BLACK, BLACK, CLR, CLR, CLR,
     CLR, CLR, CLR],
    [CLR, CLR, CLR, CLR, CLR, BLACK, RED, RED, RED, BLACK, CLR, CLR, CLR, BLACK, RED, RED, RED, BLACK, CLR, CLR, CLR,
     CLR, CLR],
    [CLR, CLR, CLR, CLR, CLR, BLACK, RED, RED, RED, RED, BLACK, D_BLUE, BLACK, RED, RED, RED, RED, BLACK, CLR, CLR, CLR,
     CLR, CLR],
    [CLR, CLR, CLR, CLR, CLR, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK,
     CLR, CLR, CLR, CLR, CLR],
    [CLR, CLR, CLR, BLACK, BLACK, BLACK, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW,
     YELLOW, BLACK, BLACK, BLACK, CLR, CLR, CLR],
    [CLR, CLR, CLR, BLACK, D_GREY, BLACK, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW,
     YELLOW, YELLOW, BLACK, D_GREY, BLACK, CLR, CLR, CLR],
    [CLR, CLR, CLR, BLACK, D_GREY, BLACK, YELLOW, YELLOW, YELLOW, BLACK, YELLOW, YELLOW, YELLOW, BLACK, YELLOW, YELLOW,
     YELLOW, BLACK, D_GREY, BLACK, CLR, CLR, CLR],
    [CLR, CLR, CLR, BLACK, GREEN, BLACK, YELLOW, YELLOW, YELLOW, BLACK, YELLOW, YELLOW, BLACK, YELLOW, YELLOW, YELLOW,
     YELLOW, BLACK, GREEN, BLACK, CLR, CLR, CLR],
    [CLR, CLR, CLR, BLACK, GREEN, BLACK, YELLOW, YELLOW, YELLOW, BLACK, YELLOW, BLACK, YELLOW, YELLOW, YELLOW, YELLOW,
     YELLOW, BLACK, GREEN, BLACK, CLR, CLR, CLR],
    [CLR, CLR, CLR, BLACK, GREEN, BLACK, YELLOW, YELLOW, YELLOW, BLACK, BLACK, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW,
     YELLOW, BLACK, GREEN, BLACK, CLR, CLR, CLR],
    [CLR, CLR, CLR, BLACK, GREEN, BLACK, YELLOW, YELLOW, YELLOW, BLACK, YELLOW, BLACK, YELLOW, YELLOW, YELLOW, YELLOW,
     YELLOW, BLACK, GREEN, BLACK, CLR, CLR, CLR],
    [CLR, CLR, CLR, BLACK, GREEN, BLACK, YELLOW, YELLOW, YELLOW, BLACK, YELLOW, YELLOW, BLACK, YELLOW, YELLOW, YELLOW,
     YELLOW, BLACK, GREEN, BLACK, CLR, CLR, CLR],
    [CLR, CLR, CLR, BLACK, GREEN, BLACK, YELLOW, YELLOW, YELLOW, BLACK, YELLOW, YELLOW, YELLOW, BLACK, YELLOW, YELLOW,
     YELLOW, BLACK, GREEN, BLACK, CLR, CLR, CLR],
    [CLR, CLR, CLR, CLR, BLACK, BLACK, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW,
     YELLOW, BLACK, BLACK, CLR, CLR, CLR, CLR],
    [CLR, CLR, CLR, CLR, CLR, BLACK, BLACK, YELLOW, YELLOW, YELLOW, BLACK, BLACK, BLACK, YELLOW, YELLOW, YELLOW, BLACK,
     BLACK, CLR, CLR, CLR, CLR, CLR],
    [CLR, CLR, CLR, CLR, CLR, CLR, BLACK, BLACK, BLACK, BLACK, L_GREY, L_GREY, L_GREY, BLACK, BLACK, BLACK, BLACK, CLR,
     CLR, CLR, CLR, CLR, CLR],
    [CLR, CLR, CLR, CLR, CLR, BLACK, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, BLACK, L_GREY, L_GREY, L_GREY, L_GREY,
     L_GREY, BLACK, CLR, CLR, CLR, CLR, CLR],
    [CLR, CLR, CLR, CLR, CLR, BLACK, L_GREY, L_GREY, D_GREY, D_GREY, L_GREY, L_GREY, L_GREY, D_GREY, D_GREY, L_GREY,
     L_GREY, BLACK, CLR, CLR, CLR, CLR, CLR],
    [CLR, CLR, CLR, CLR, CLR, BLACK, L_GREY, D_GREY, BLACK, BLACK, D_GREY, L_GREY, D_GREY, BLACK, BLACK, D_GREY, L_GREY,
     BLACK, CLR, CLR, CLR, CLR, CLR],
    [CLR, CLR, CLR, CLR, CLR, BLACK, L_GREY, D_GREY, L_BLUE, BLACK, D_GREY, L_GREY, D_GREY, L_BLUE, BLACK, D_GREY,
     L_GREY, BLACK, CLR, CLR, CLR, CLR, CLR],
    [CLR, CLR, CLR, CLR, CLR, BLACK, L_GREY, L_GREY, D_GREY, D_GREY, L_GREY, L_GREY, L_GREY, D_GREY, D_GREY, L_GREY,
     L_GREY, BLACK, CLR, CLR, CLR, CLR, CLR],
    [CLR, CLR, CLR, CLR, CLR, CLR, BLACK, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, BLACK,
     CLR, CLR, CLR, CLR, CLR, CLR],
    [CLR, CLR, CLR, CLR, CLR, CLR, CLR, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, CLR, CLR, CLR,
     CLR, CLR, CLR, CLR]
])

BEEPER = [
    [CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR],
    [CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, CLR, CLR, CLR, CLR, CLR,
     CLR, CLR, CLR],
    [CLR, CLR, CLR, CLR, CLR, CLR, BLACK, BLACK, D_GREY, D_GREY, D_GREY, D_GREY, D_GREY, D_GREY, D_GREY, BLACK, BLACK,
     CLR, CLR, CLR, CLR, CLR, CLR],
    [CLR, CLR, CLR, CLR, CLR, BLACK, D_GREY, D_GREY, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, D_GREY, D_GREY,
     BLACK, CLR, CLR, CLR, CLR, CLR],
    [CLR, CLR, CLR, CLR, BLACK, D_GREY, BLACK, BLACK, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, BLACK,
     BLACK, D_GREY, BLACK, CLR, CLR, CLR, CLR],
    [CLR, CLR, CLR, BLACK, D_GREY, D_GREY, BLACK, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY,
     L_GREY, BLACK, D_GREY, D_GREY, BLACK, CLR, CLR, CLR],
    [CLR, CLR, BLACK, D_GREY, BLACK, BLACK, BLACK, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY,
     L_GREY, BLACK, BLACK, BLACK, D_GREY, BLACK, CLR, CLR],
    [CLR, CLR, BLACK, D_GREY, BLACK, L_GREY, L_GREY, BLACK, L_GREY, L_GREY, BLACK, BLACK, BLACK, L_GREY, L_GREY, BLACK,
     L_GREY, L_GREY, BLACK, D_GREY, BLACK, CLR, CLR],
    [CLR, BLACK, D_GREY, BLACK, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, BLACK, RED, RED, RED, BLACK, L_GREY, L_GREY,
     L_GREY, L_GREY, L_GREY, BLACK, D_GREY, BLACK, CLR],
    [CLR, BLACK, D_GREY, BLACK, L_GREY, L_GREY, L_GREY, L_GREY, BLACK, RED, RED, RED, RED, RED, BLACK, L_GREY, L_GREY,
     L_GREY, L_GREY, BLACK, D_GREY, BLACK, CLR],
    [CLR, BLACK, D_GREY, BLACK, L_GREY, L_GREY, L_GREY, BLACK, RED, RED, RED, RED, RED, RED, RED, BLACK, L_GREY, L_GREY,
     L_GREY, BLACK, D_GREY, BLACK, CLR],
    [CLR, BLACK, D_GREY, BLACK, L_GREY, L_GREY, L_GREY, BLACK, RED, RED, RED, RED, RED, RED, RED, BLACK, L_GREY, L_GREY,
     L_GREY, BLACK, D_GREY, BLACK, CLR],
    [CLR, BLACK, D_GREY, BLACK, L_GREY, L_GREY, L_GREY, BLACK, RED, RED, RED, RED, RED, RED, RED, BLACK, L_GREY, L_GREY,
     L_GREY, BLACK, D_GREY, BLACK, CLR],
    [CLR, BLACK, D_GREY, BLACK, L_GREY, L_GREY, L_GREY, L_GREY, BLACK, RED, RED, RED, RED, RED, BLACK, L_GREY, L_GREY,
     L_GREY, L_GREY, BLACK, D_GREY, BLACK, CLR],
    [CLR, BLACK, D_GREY, BLACK, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, BLACK, RED, RED, RED, BLACK, L_GREY, L_GREY,
     L_GREY, L_GREY, L_GREY, BLACK, D_GREY, BLACK, CLR],
    [CLR, CLR, BLACK, D_GREY, BLACK, L_GREY, L_GREY, BLACK, L_GREY, L_GREY, BLACK, BLACK, BLACK, L_GREY, L_GREY, BLACK,
     L_GREY, L_GREY, BLACK, D_GREY, BLACK, CLR, CLR],
    [CLR, CLR, BLACK, D_GREY, BLACK, BLACK, BLACK, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY,
     L_GREY, BLACK, BLACK, BLACK, D_GREY, BLACK, CLR, CLR],
    [CLR, CLR, CLR, BLACK, D_GREY, D_GREY, BLACK, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY,
     L_GREY, BLACK, D_GREY, D_GREY, BLACK, CLR, CLR, CLR],
    [CLR, CLR, CLR, CLR, BLACK, D_GREY, BLACK, BLACK, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, L_GREY, BLACK,
     BLACK, D_GREY, BLACK, CLR, CLR, CLR, CLR],
    [CLR, CLR, CLR, CLR, CLR, BLACK, D_GREY, D_GREY, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, D_GREY, D_GREY,
     BLACK, CLR, CLR, CLR, CLR, CLR],
    [CLR, CLR, CLR, CLR, CLR, CLR, BLACK, BLACK, D_GREY, D_GREY, D_GREY, D_GREY, D_GREY, D_GREY, D_GREY, BLACK, BLACK,
     CLR, CLR, CLR, CLR, CLR, CLR],
    [CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, CLR, CLR, CLR, CLR, CLR,
     CLR, CLR, CLR],
    [CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR, CLR],
]

BEEPER_SURF = 0

HORIZ_TILES = 0
VERT_TILES = 0


def _continued_exception(text):
    try:
        raise Exception(text)
    except Exception as exc:
        print("\n")
        traceback.print_stack(limit=-1)
        traceback.print_exception(Exception, exc, None, limit=-1)


def _replace_2d(array, value, replacement):
    array = array.copy()
    for x in range(0, len(array)):
        for y in range(0, len(array[x])):
            if all(array[x][y] == value):
                array[x][y] = replacement
    return array


def _readable_pixarray_to_surface(array):
    # array = array.swapaxes(0, 1)
    surf = pygame.Surface(array.shape[0:2], pygame.SRCALPHA).convert()
    pygame.surfarray.blit_array(surf, array)
    surf.set_colorkey(CLR)
    return surf


def _tile_to_point(tile):
    global TILE_WIDTH
    return (tile + 0.5) * TILE_WIDTH


def _point_to_tile(point):
    global TILE_WIDTH
    return (point / TILE_WIDTH) - 0.5


def _wall_at(tile_x, tile_y):
    global WALLS, HORIZ_TILES, VERT_TILES
    if tile_x == -0.5 or tile_y == -0.5 or tile_x == HORIZ_TILES + 0.5 or tile_y == VERT_TILES + 0.5:
        return True
    for w in WALLS:
        if w[0] == tile_x and w[1] == tile_y:
            return True
    return False


def _extract_vals_inside_parenthesis(string, open_parenthesis_index):
    p = []
    temp = ""
    count = open_parenthesis_index + 1
    while count < len(string):
        if string[count] == ' ':
            p.append(temp)
            temp = ""
        elif string[count] == ')':
            p.append(temp)
            return p
        else:
            temp += string[count]
        count += 1
    return p


class Robot(pygame.sprite.Sprite):
    """Creates a new Robot and stores information about it.
##Required Parameters:##
* **x (int)** the starting x position of the Robot
    * ```0 <= x < World.width```
* **y (int)** the starting y position of the Robot
    * ```0 <= y < World.height```
* **direction (str)** the starting direction of the Robot
    * ```direction == {"North", "South", "East", "West"}```
* **num_of_beepers (int)** the starting number of beepers of the Robot
    * ```0 <= num_of_beepers```
##Optional Parameters:##
* **color (int)** the sleeve color of the Robot
    * ```0 < color < 4```
    * Current colors: ```[Green, Orange, Pink, Teal, Purple]```
    * Colors are automatically assigned based on the order Robots are added to the World.
"""
    __ids = count(0)

    def __init__(self, x, y, direction, num_of_beepers, color=-1):
        # color is an int, maybe add string colors eventually
        super().__init__()
        self.id = next(self.__ids)
        self.__color = SLEEVE_COLORS[(self.id if color == -1 else color) % len(SLEEVE_COLORS)]
        self.__tile_x = x
        self.__tile_y = y
        self.__direction = DIRECTIONS[direction]
        self.__beepers = num_of_beepers
        self.has_moved_this_frame = True
        self.__image = 0
        self.__rect = 0
        self.is_alive = True
        self.__prev_fps = 4
        self.__zoom_fps = 20
        self.__array = _replace_2d(KAREL_ON, GREEN, self.__color[1])

        print("[" + self.__color[0] + " Robot] Initializing...")

    def _scale_image(self, width):
        self.__image = pygame.transform.rotate(
            pygame.transform.scale(_readable_pixarray_to_surface(self.__array), (width, width)),
            self.__direction)
        self.__rect = self.__image.get_rect()
        self.__rect.x = _tile_to_point(self.__tile_x - 0.5)
        self.__rect.y = _tile_to_point(self.__tile_y - 0.5)

    def get_sleeve_color(self):
        """Returns the sleeve color of the Robot.\n
        **return type:** ```str```
        """
        return self.__color[0]

    def turn_left(self):
        """Rotates the Robot left 90 degrees."""
        if self.is_alive:
            self.wait()
            self.__image = pygame.transform.rotate(self.__image, 90)
            self.__direction = (self.__direction + 90) % 360
            self.has_moved_this_frame = True

    def move(self):
        """Moves the Robot forward one space.\n
        Will not move into Walls or the border of the stage.
        """
        if self.is_alive:
            self.wait()
            if self.front_is_clear():
                if self.__direction == 0:
                    self.__rect.x += TILE_WIDTH
                    self.__tile_x += 1
                elif self.__direction == 180:
                    self.__rect.x -= TILE_WIDTH
                    self.__tile_x -= 1
                elif self.__direction == 270:
                    self.__rect.y += TILE_WIDTH
                    self.__tile_y += 1
                elif self.__direction == 90:
                    self.__rect.y -= TILE_WIDTH
                    self.__tile_y -= 1
            else:
                _continued_exception("[" + self.__color[0] + " Robot] I ran into a wall! ")
                self.turn_off()
            self.has_moved_this_frame = True

    def pick_beeper(self):
        """Makes the Robot pick up a single Beeper if it is standing on one.\n
        If it is not standing on any Beepers, it will cause an error and turn off.
        """
        global BEEPERS
        if self.is_alive:
            self.wait()
            beepers_at_pos = [b for b in BEEPERS if b.tile_x == self.__tile_x and b.tile_y == self.__tile_y]
            if len(beepers_at_pos) > 0:
                beepers_at_pos[0]._dec()
                self.__beepers += 1
            self.has_moved_this_frame = True

    def put_beeper(self):
        """Makes the Robot put down up a single Beeper in the space it is standing on.\n
        If it does not have any Beepers, it will cause an error and turn off.
        """
        global BEEPERS
        if self.is_alive:
            self.wait()
            if self.has_any_beepers():
                beepers_at_pos = [b for b in BEEPERS if b.tile_x == self.__tile_x and b.tile_y == self.__tile_y]
                self.__beepers -= 1
                if len(beepers_at_pos) > 0:
                    beepers_at_pos[0]._inc()
                else:
                    BEEPERS.add(_Beeper(self.__tile_x, self.__tile_y, 1))
            else:
                # raise Exception("[" + self.__color[0] + " Robot] I don't have any beepers! ")
                _continued_exception("[" + self.__color[0] + " Robot] I don't have any beepers! ")
                self.turn_off()
            self.has_moved_this_frame = True

    def has_any_beepers(self):
        """Returns True if the Robot has at least 1 Beeper, and False if not.\n
        **return type:** ```bool```
        """
        return self.__beepers > 0

    def front_is_clear(self):  # TODO: maybe invert
        """Returns True if there are no walls directly in front of the Robot, and False if there are.\n
        **return type:** ```bool```
        """
        if self.__direction == 0:
            return not _wall_at(self.__tile_x + 0.5, self.__tile_y)
        elif self.__direction == 180:
            return not _wall_at(self.__tile_x - 0.5, self.__tile_y)
        elif self.__direction == 270:
            return not _wall_at(self.__tile_x, self.__tile_y + 0.5)
        elif self.__direction == 90:
            return not _wall_at(self.__tile_x, self.__tile_y - 0.5)
        else:
            return False

    def facing_north(self):
        """Returns True if the Robot is facing North, and False if not.\n
        **return type:** ```bool```
        """
        return self.__direction == 90

    def facing_south(self):
        """Returns True if the Robot is facing South, and False if not.\n
        **return type:** ```bool```
        """
        return self.__direction == 270

    def facing_east(self):
        """Returns True if the Robot is facing East, and False if not.\n
        **return type:** ```bool```
        """
        return self.__direction == 0

    def facing_west(self):
        """Returns True if the Robot is facing West, and False if not.\n
        **return type:** ```bool```
        """
        return self.__direction == 180

    def standing_on_any_beepers(self):
        """Returns True if the Robot is standing on at least 1 Beeper, and False if not.\n
        **return type:** ```bool```
        """
        return len([b for b in BEEPERS if b.tile_x == self.__tile_x and b.tile_y == self.__tile_y]) > 0

    def standing_on_any_robots(self):
        """##**NOT IMPLEMENTED YET**##
        Returns True if the Robot is standing on at least 1 other Robot, and False if not.\n
        **return type:** ```bool```
        """
        return False

    def turn_off(self):
        """Turns off the Robot.\n
        After this method is called, no more commands may be called on this Robot."""
        global TILE_WIDTH
        if self.is_alive:
            self.wait()
            self.is_alive = False
            self.__array = _replace_2d(self.__array, YELLOW, L_GREY)
            self._scale_image(TILE_WIDTH)

    def wait(self):
        """Makes the Robot freeze for a single frame."""
        global FPS
        if self.is_alive:  # prevents commands from being run before the loop checks for dead robots, putting it in an infinite loop
            while self.has_moved_this_frame:
                time.sleep(1.0 / FPS)

    def _draw(self, screen):
        screen.blit(self.__image, (self.__rect.x, self.__rect.y))

    def add_method(self):
        """[[Source]](https://medium.com/@mgarod/dynamically-add-a-method-to-a-class-in-python-c49204b85bd6)\n
        **See [Creating Custom Methods](#creating-custom-methods) for more information.**
        """

        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                return func(self, *args, **kwargs)

            setattr(self, func.__name__, wrapper)
            # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
            return func  # returning func means func can still be used normally

        return decorator

    def set_zoom_fps(self, fps):
        """**ADVANCED USERS ONLY**\n
Sets the speed for the Robot to use when zooming.\n

##Required Parameters:##

* **fps (int)** the fps to use when zooming
    * ```0 < fps```
        """
        self.__zoom_fps = fps

    def zoom(self, on):  # TODO: zooming is quirky
        """**ADVANCED USERS ONLY**\n
Makes the Robot start zooming if True, and makes the Robot stop zooming if False.\n
##Required Parameters:##
* **on (bool)** True if on, False if not
    * ```on == {True, False}```
        """
        if self.is_alive:
            self.wait()
            global FPS
            self.has_moved_this_frame = True
            if on:
                self.__prev_fps = FPS
                FPS = self.__zoom_fps
            else:
                FPS = self.__prev_fps


class _Beeper(pygame.sprite.Sprite):
    """doc for beeper and constructor"""

    def __init__(self, x, y, num):
        super().__init__()
        global BEEPER_SURF
        self.tile_x = x
        self.tile_y = y
        self.num = num
        self.image = 0
        self.rect = 0
        self._update_image()

    def _inc(self):
        self.num += 1
        self._update_image()

    def _dec(self):
        global BEEPERS
        self.num -= 1
        if self.num < 1:
            BEEPERS.remove(self)
            self.kill()
        else:
            self._update_image()

    def _update_image(self):
        global BEEPER_SURF
        self.image = BEEPER_SURF.copy()
        self.image.blit(
            pygame.font.Font('freesansbold.ttf', 10 if len(str(self.num)) == 1 else 8).render(str(self.num), True,
                                                                                              BLACK),
            ((0.475 if len(str(self.num)) == 1 else 0.45) * TILE_WIDTH, 0.425 * TILE_WIDTH))
        self.rect = self.image.get_rect()
        self.rect.x = _tile_to_point(self.tile_x - 0.5)
        self.rect.y = _tile_to_point(self.tile_y - 0.5)

    def _draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class World(object):
    """Creates a new World and stores information about it.
##Required Parameters:##
* **width (int)** the number of tiles the World should be horizontally
    * ```0 < width```
* **height (int)** the number of tiles the World should be vertically
    * ```0 < height```
##Optional Parameters:##
* **name (str)** the window name of the World
    * Default: ```"Karel J Robot"```
* **fps (int)** the FPS of the World
    * ```0 < fps```
    * Default: ```4```
* Other parameters exist but should only be used internally.
"""

    # maybe add window size attributes
    def __init__(self, width, height, name="Karel J Robot", fps=4, beeper_pos=[], wall_pos=[]):
        global FPS, BEEPERS, HORIZ_TILES, VERT_TILES
        self.IDEAL_HEIGHT = 700
        """####**CHANGE THIS VALUE DEPENDING ON THE DEVICE THIS SCRIPT IS RUNNING ON**####
        >This is the maximum number of pixels the World window can take up vertically.\n
        >Check your monitor resolution for the best results.\n
        >* Ideal value for Repl.it: 600"""
        self.IDEAL_WIDTH = 900
        """####**CHANGE THIS VALUE DEPENDING ON THE DEVICE THIS SCRIPT IS RUNNING ON**####
        >This is the maximum number of pixels the World window can take up horizontally.\n
        >Check your monitor resolution for the best results.\n
        >* Ideal value for Repl.it: 800"""
        FPS = fps

        HORIZ_TILES = width
        VERT_TILES = height
        self.__beeper_pos = beeper_pos
        self.__wall_pos = wall_pos

        BEEPERS = pygame.sprite.Group()
        self.__robots = []
        self.__screen = None
        self.__background = None
        self.__running = False
        self.__clock = None
        self.__idle_frames = 0
        # self.interval = 10

        self.__thread = threading.Thread(target=self.__run, args=())
        self.__thread.daemon = False  # Daemonize thread
        self.__name = name

    @classmethod  # constructor for loading a file
    def from_file(cls, filename):
        """Creates a World from a file.
##Required Parameters:##
* **filename (str)** the file name of the World to be loaded, including the file type
See [Setting up World Files](#setting-up-world-files) for information on setting up World files.
"""
        file = open(filename)
        width = 0
        height = 0
        fps = 4
        name = "Karel J Robot"
        beepers = []
        walls = []

        for l in file:
            if l.startswith("legacy: "):
                print("legacy mode")
            elif l.startswith("name: ") and len(l) > 6:
                name = str(l[6:])
            elif l.startswith("size: "):
                for i in range(6, len(l)):
                    if l[i] == '(':
                        p = _extract_vals_inside_parenthesis(l, i)
                        if len(p) == 2:
                            width = int(p[0])
                            height = int(p[1])
            elif l.startswith("fps: ") and len(l) > 5:
                fps = int(l[5:])
            elif l.startswith("beepers: "):
                for i in range(9, len(l)):
                    if l[i] == '(':
                        p = _extract_vals_inside_parenthesis(l, i)
                        if len(p) == 3:
                            beepers.append((int(p[0]), int(p[1]), int(p[2])))
            elif l.startswith("walls: "):
                for i in range(7, len(l)):
                    if l[i] == '(':
                        p = _extract_vals_inside_parenthesis(l, i)
                        if len(p) == 4:
                            walls.append((0 if p[0] == 'h' else 1, float(p[1]), float(p[2]), float(p[3])))
        file.close()
        return cls(width, height, name=name, fps=fps, beeper_pos=beepers, wall_pos=walls)

    def add_robots(self, *robots):
        """Adds Robots to the World.
##Required Parameters:##
* **robots (Robot...)** any Robots to be added to the World
See [Using Worlds within Code](#using-worlds-within-code) for more detailed information.
"""
        if self.__thread.is_alive():
            _continued_exception("[World] Cannot add robots while the world is running!")
        else:
            for r in robots:
                self.__robots.append(r)
                print("[World] Added " + r.get_sleeve_color() + " Robot")

    def save_screenshot(self, filename="screenshot.jpg"):
        """Saves a screenshot of the World.
##Optional Parameters:##
* **filename (str)** the desired filename of the screenshot
    * Default: ```"screenshot.jpg"```
    * ```.jpg``` will automatically be added to the end of the filename if it is not there already
"""
        if not filename.endswith(".jpg"):
            filename += ".jpg"
        if self.__thread.is_alive():
            pygame.image.save(self.__screen, filename)
            print("[World] Saved screenshot as \"" + filename + "\".")
        else:
            _continued_exception("[World] Cannot take screenshot until the World is running!")

    def set_fps(self, fps):
        """Sets the FPS of the World.\n
**IMPORTANT:** Can only be called before [```World.start()```](#karel_the_robot.World.start) is called.
##Required Parameters:##
* **fps (int)** the FPS for the World to run at
    * ```0 < fps```
"""
        global FPS
        if self.__thread.is_alive():
            _continued_exception("[World] Cannot change FPS while the World is running!")
        else:
            FPS = fps
            print("[World] Changed FPS.")

    def start(self):
        """Starts the World.\n
See [Using Worlds within Code](#using-worlds-within-code) for more detailed information."""
        if self.__thread.is_alive():
            _continued_exception("[World] Cannot start the World while the World is already running!")
        else:
            self.__thread.start()

    def __run(self):

        print("\n" + "[World] Initializing..." + "\n")
        global SCREEN_WIDTH, SCREEN_HEIGHT, TILE_WIDTH, FPS, BEEPERS, BEEPER_SURF, WALLS, HORIZ_TILES, VERT_TILES
        pygame.init()
        TILE_WIDTH = int(min(self.IDEAL_WIDTH / (HORIZ_TILES + 1), self.IDEAL_HEIGHT / (VERT_TILES + 1)))
        if TILE_WIDTH % 2 == 1:
            TILE_WIDTH -= 1
        SCREEN_WIDTH = TILE_WIDTH * (HORIZ_TILES + 1)
        SCREEN_HEIGHT = TILE_WIDTH * (VERT_TILES + 1)
        print("[World] Screen height is " + str(SCREEN_HEIGHT))
        self.__screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])  # add scaling

        BEEPER_SURF = pygame.transform.scale(_readable_pixarray_to_surface(numpy.array(BEEPER)),
                                             (TILE_WIDTH, TILE_WIDTH))

        print("[World] Scaling robots...")
        for r in self.__robots:
            r._scale_image(TILE_WIDTH)

        for p in self.__beeper_pos:
            BEEPERS.add(_Beeper(p[0], p[1], p[2]))

        print("[World] Generating background...")
        self.__background = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.__background.fill(WHITE)
        for x in range(0, HORIZ_TILES + 1):
            pygame.draw.line(self.__background, BLACK, ((x + 0.5) * TILE_WIDTH, 0.5 * TILE_WIDTH),
                             ((x + 0.5) * TILE_WIDTH, (VERT_TILES + 0.5) * TILE_WIDTH))
            self.__background.blit(pygame.font.Font("freesansbold.ttf", 10).render(str(x), True, BLACK),
                                   ((x + 0.5) * TILE_WIDTH, 0.25 * TILE_WIDTH))
        for y in range(0, VERT_TILES + 1):
            pygame.draw.line(self.__background, BLACK, (0.5 * TILE_WIDTH, (y + 0.5) * TILE_WIDTH),
                             ((HORIZ_TILES + 0.5) * TILE_WIDTH, (y + 0.5) * TILE_WIDTH))
            self.__background.blit(pygame.font.Font("freesansbold.ttf", 10).render(str(y), True, BLACK),
                                   (0.25 * TILE_WIDTH, (y + 0.5) * TILE_WIDTH))

        for w in self.__wall_pos:
            pygame.draw.line(self.__background, RED,
                             (_tile_to_point(w[1]), _tile_to_point(w[2])),
                             (_tile_to_point(w[3] if w[0] == 0 else w[1]), _tile_to_point(w[3] if w[0] == 1 else w[2])),
                             3)
            for i in range(0, int(abs(w[3] - w[1 if w[0] == 0 else 2]))):
                # works no matter what order the walls are in
                WALLS.append(
                    (w[1] + ((i + 0.5 if w[1] <= w[3] else 0 - i - 0.5) if w[0] == 0 else 0),
                     w[2] + ((i + 0.5 if w[2] <= w[3] else 0 - i - 0.5) if w[0] == 1 else 0))
                )
        pygame.display.set_caption(self.__name)

        self.__clock = pygame.time.Clock()
        self.__running = True
        self.__idle_frames = 0

        print("[World] Done!" + "\n\n\n\n")
        # quits if it idles for more than one second
        while sum(r.is_alive for r in self.__robots) > 0 and self.__idle_frames < FPS:
            pygame.event.get()  # required or else the window thinks it's not responding
            self.__screen.blit(self.__background, (0, 0))
            BEEPERS.draw(self.__screen)

            any_robots_moved = False
            for r in self.__robots:
                any_robots_moved = any_robots_moved or r.has_moved_this_frame
                r._draw(self.__screen)
                r.has_moved_this_frame = False

            if any_robots_moved:
                self.__idle_frames = 0
            else:
                self.__idle_frames += 1

            self.__clock.tick(FPS)
            pygame.display.flip()
        print("[World] Saving screenshot...")
        pygame.image.save(self.__screen, "final_world_status.jpg")
        print("[World] Quitting...")
        pygame.quit()

# TODO: add dialogue for all robot moves
# TODO: add more error messages
