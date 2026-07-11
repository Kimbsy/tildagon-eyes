import random
from typing import Literal
from app import App
from app_components import Menu, Notification, clear_background

initial_delay = 20
glance_delay = 10
min_delay = 20
max_delay = 50
eh = 80
ew = 20
x_gap = 60

initial_position = [0, 0]
positions = [
    [-40, 0],
    [40, 0],
    [0, -40],
    [0, 40]
]

WHITE = [1, 1, 1]
BLACK = [0, 0, 0]
GREY = [0.4, 0.4, 0.4]
LIGHT_GREY = [0.8, 0.8, 0.8]
ORANGE = [1, 0.5, 0.1]
DARK_BLUE = [0.17, 0.26, 0.32]
ICE_BLUE = [0.75, 0.99, 0.98]
ELECTRIC_PINK = [0.9, 0.01, 0.35]
ELECTRIC_BLUE = [0.1, 1, 1]

THEMES = {
    "Monochrome": [WHITE, BLACK],
    "Crab": [ORANGE, WHITE],
    "Icy": [ICE_BLUE, BLACK],
    "Neon": [ELECTRIC_PINK, ELECTRIC_BLUE],
    "Noir": [GREY, LIGHT_GREY]
}

# @TODO: blinking animation
# @TODO: more complex animations + state machine

def rand_nth(coll):
    return coll[random.randint(0, len(coll) - 1)]

def new_delay():
    return random.randint(min_delay, max_delay)

def colour(ctx, c):
    r, g, b = c
    ctx.rgb(r, g, b)

class EyesApp(App):
    def __init__(self):
        self.menu = Menu(
            self,
            list(THEMES.keys()),
            select_handler = self.select_handler,
            back_handler = self.back_handler
        )
        self.display_menu = True
        self.remaining = initial_delay
        self.x = 0
        self.y = 0
        self.face_colour = WHITE
        self.eye_colour = BLACK

    def select_handler(self, item, idx):
        if self.display_menu:
            face_colour, eye_colour = THEMES[item]
            self.face_colour = face_colour
            self.eye_colour = eye_colour
            self.display_menu = False
        else:
            self.display_menu = True

    def back_handler(self):
        if self.display_menu:
            self.display_menu = False
        else:
            self.minimise()

    def update(self, delta):
        if (self.remaining <= 0):
            self.delay_callback()
        self.remaining = self.remaining - 1

    def draw_face(self, ctx):
        # background
        colour(ctx, self.face_colour)
        ctx.rectangle(-120, -120, 240, 240).fill()

        colour(ctx, self.eye_colour)
        # draw left eye
        ctx.rectangle(
            self.x - (x_gap / 2) - (ew / 2),
            self.y - (eh / 2),
            ew,
            eh).fill()

        # draw right eye
        ctx.rectangle(
            self.x + (x_gap / 2) - (ew / 2),
            self.y - (eh / 2),
            ew,
            eh).fill()

    def draw(self, ctx):
        clear_background(ctx)

        if self.display_menu:
            self.menu.draw(ctx)
        else:
            self.draw_face(ctx)
            
    def delay_callback(self):
        if (self.x == 0 and self.y == 0):
            new_x, new_y = rand_nth(positions)
            self.remaining = glance_delay
        else:
            new_x, new_y = initial_position
            self.remaining = new_delay()
            
        self.x = new_x
        self.y = new_y

__app_export__ = EyesApp
