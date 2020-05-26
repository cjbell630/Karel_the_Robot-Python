"""top line\n

##Question  1##
>Answer 1\n

##Question  2##
>Answer 2\n

##Question  3##
>Answer 3\n

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
    global WALLS
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
    """documentation for Robot and constructor

    """
    __ids = count(0)

    def __init__(self, x, y, direction, num_of_beepers, color=-1):
        # color is an int, maybe add string colors eventually
        super().__init__()
        self.id = next(self.__ids)
        """documentation for self.id"""
        self.__color = SLEEVE_COLORS[(self.id if color == -1 else color) % len(SLEEVE_COLORS)]
        self.__tile_x = x
        self.__tile_y = y
        self.__direction = direction
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
        """doc for get_sleeve_color"""
        return self.__color[0]

    def turn_left(self):
        """doc for turn_left"""
        if self.is_alive:
            self.wait()
            self.__image = pygame.transform.rotate(self.__image, 90)
            self.__direction = (self.__direction + 90) % 360
            self.has_moved_this_frame = True

    def move(self):
        """doc for move"""
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

            print("tried to move")
            self.has_moved_this_frame = True

    def pick_beeper(self):
        """doc for pick_beeper"""
        global BEEPERS

        if self.is_alive:
            self.wait()
            beepers_at_pos = [b for b in BEEPERS if b.__tile_x == self.__tile_x and b.__tile_y == self.__tile_y]
            if len(beepers_at_pos) > 0:
                beepers_at_pos[0]._dec()
                self.__beepers += 1
            self.has_moved_this_frame = True

    def put_beeper(self):
        """doc for put_beeper"""
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

            print("tried to put beeper" + str(self.__beepers))
            self.has_moved_this_frame = True

    def has_any_beepers(self):
        """doc for has_any_beepers"""
        return self.__beepers > 0

    def front_is_clear(self):
        """doc for front_is_clear"""
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
        """doc for facing_north"""
        return self.__direction == 90

    def facing_south(self):
        """doc for facing_south"""
        return self.__direction == 270

    def facing_east(self):
        """doc for facing_east"""
        return self.__direction == 0

    def facing_west(self):
        """doc for facing_west"""
        return self.__direction == 180

    def standing_on_any_beepers(self):
        """doc for standing_on_any_beepers"""
        return len([b for b in BEEPERS if b.__tile_x == self.__tile_x and b.__tile_y == self.__tile_y]) > 0

    def standing_on_any_robots(self):
        """doc for standing_on_any_robots"""
        return False

    def turn_off(self):
        """doc for turn_off"""
        global TILE_WIDTH
        if self.is_alive:
            self.wait()
            self.is_alive = False
            self.__array = _replace_2d(self.__array, YELLOW, L_GREY)
            self._scale_image(TILE_WIDTH)
            print("am dead")

    def wait(self):
        """doc for wait"""
        global FPS
        if self.is_alive:  # prevents commands from being run before the loop checks for dead robots, putting it in an infinite loop
            while self.has_moved_this_frame:
                # print("waiting for frame")
                time.sleep(1.0 / FPS)

    def _draw(self, screen):
        screen.blit(self.__image, (self.__rect.x, self.__rect.y))

    # https://medium.com/@mgarod/dynamically-add-a-method-to-a-class-in-python-c49204b85bd6
    def add_method(self):
        """doc for add_method
        https://medium.com/@mgarod/dynamically-add-a-method-to-a-class-in-python-c49204b85bd6"""

        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                return func(self, *args, **kwargs)

            setattr(self, func.__name__, wrapper)
            # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
            return func  # returning func means func can still be used normally

        return decorator

    def set_zoom_fps(self, fps):
        """doc for set_zoom_fps"""
        self.__zoom_fps = fps

    def zoom(self, on):  # TODO: zooming is quirky
        """doc for zoom"""
        if self.is_alive:
            self.wait()
            global FPS
            self.has_moved_this_frame = True
            if on:
                self.__prev_fps = FPS
                FPS = self.__zoom_fps
                print("ZOOM")
            else:
                FPS = self.__prev_fps
                print("no longer zooming")


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
    """doc for world and constructor"""

    # maybe add window size attributes
    def __init__(self, width, height, name="Karel J Robot", fps=4, beeper_pos=[], wall_pos=[]):
        global FPS, BEEPERS
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

        self.__width = width
        self.__height = height
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
        """doc for from_file"""
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
        """doc for add_robots"""
        if self.__thread.is_alive():
            _continued_exception("[World] Cannot add robots while the world is running!")
        else:
            for r in robots:
                self.__robots.append(r)
                print("[World] Added " + r.get_sleeve_color() + " Robot")

    def save_screenshot(self, filename="screenshot.jpg"):
        """doc for save_screenshot"""
        if not filename.endswith(".jpg"):
            filename += ".jpg"
        if self.__thread.is_alive():
            pygame.image.save(self.__screen, filename)
            print("[World] Saved screenshot as \"" + filename + "\".")
        else:
            _continued_exception("[World] Cannot take screenshot until the world is running!")

    def set_fps(self, fps):
        """doc for set_fps"""
        global FPS
        FPS = fps
        print("[World] Changed FPS")

    def start(self):
        """doc for start"""
        self.__thread.start()

    def __run(self):

        print("\n" + "[World] Initializing..." + "\n")
        global SCREEN_WIDTH, SCREEN_HEIGHT, TILE_WIDTH, FPS, BEEPERS, BEEPER_SURF, WALLS
        pygame.init()
        TILE_WIDTH = int(min(self.IDEAL_WIDTH / (self.__width + 1), self.IDEAL_HEIGHT / (self.__height + 1)))
        if TILE_WIDTH % 2 == 1:
            TILE_WIDTH -= 1
        SCREEN_WIDTH = TILE_WIDTH * (self.__width + 1)
        SCREEN_HEIGHT = TILE_WIDTH * (self.__height + 1)
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
        for x in range(0, self.__width + 1):
            pygame.draw.line(self.__background, BLACK, ((x + 0.5) * TILE_WIDTH, 0.5 * TILE_WIDTH),
                             ((x + 0.5) * TILE_WIDTH, (self.__height + 0.5) * TILE_WIDTH))
            self.__background.blit(pygame.font.Font('freesansbold.ttf', 10).render(str(x), True, BLACK),
                                   ((x + 0.5) * TILE_WIDTH, 0.25 * TILE_WIDTH))
        for y in range(0, self.__height + 1):
            pygame.draw.line(self.__background, BLACK, (0.5 * TILE_WIDTH, (y + 0.5) * TILE_WIDTH),
                             ((self.__width + 0.5) * TILE_WIDTH, (y + 0.5) * TILE_WIDTH))
            self.__background.blit(pygame.font.Font('freesansbold.ttf', 10).render(str(y), True, BLACK),
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
        print(WALLS)
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
