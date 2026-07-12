from random import random, randint
from typing import Literal
from app import App
from app_components import Menu, Notification, clear_background

initial_delay = 20
glance_delay = 10
min_delay = 20
max_delay = 50
eh = 85
ew = 20
x_gap = 60
blink_chance = 0.3

initial_position = [0, 0]
positions = [
    [-40, 0],
    [40, 0],
    [0, -40],
    [0, 40]
]

def parse_hex(s):
    r = int("0x" + s[1:3], 16)
    g = int("0x" + s[3:5], 16)
    b = int("0x" + s[5:7], 16)
    return [r / 255, g / 255, b / 255]

WHITE = [1, 1, 1]
BLACK = [0, 0, 0]
GREY = [0.4, 0.4, 0.4]
LIGHT_GREY = [0.8, 0.8, 0.8]
CRAB_ORANGE = [1, 0.5, 0.1]
DARK_BLUE = [0.17, 0.26, 0.32]
ICE_BLUE = [0.75, 0.99, 0.98]
ELECTRIC_PINK = [0.9, 0.01, 0.35]
ELECTRIC_BLUE = [0.1, 1, 1]
RED = parse_hex("#E40303")
ORANGE = parse_hex("#FF8C00")
YELLOW = parse_hex("#FFED00")
GREEN = parse_hex("#008026")
BLUE = parse_hex("#004CFF")
PURPLE = parse_hex("#732982")
FOREST_GREEN = parse_hex("#4F9D69")
BROWN = parse_hex("#504136")
DARK_PINK = parse_hex("#EF0AFF")
LIGHT_PINK = parse_hex("#FAADFF")

THEMES = {
    "Monochrome": [WHITE, BLACK],
    "Crab": [CRAB_ORANGE, WHITE],
    "Neon": [ELECTRIC_PINK, ELECTRIC_BLUE],
    "Noir": [GREY, LIGHT_GREY],
    "Desert": [YELLOW, WHITE],
    "Forest": [FOREST_GREEN, BROWN],
    "Rose": [LIGHT_PINK, DARK_PINK],
    "Pride": ["pride", WHITE],
    "Space": ["space", WHITE]
}

stars = []
for _ in range(100):
    stars.append([
        randint(-120, 120),
        randint(-120, 120),
        randint(1, 3),
        0.2 + (random() * 0.2)
    ])

# @TODO: theme swatches in the menu
# @TODO: don't move menu items when the menu isn't displayed

def rand_nth(coll):
    return coll[randint(0, len(coll) - 1)]

def new_delay():
    return randint(min_delay, max_delay)

def colour(ctx, c):
    r, g, b = c
    ctx.rgb(r, g, b)

class EyesApp(App):
    def __init__(self):
        self.state = "looking"
        self.blink_progress = 0
        self.menu = Menu(
            self,
            sorted(list(THEMES.keys())),
            select_handler = self.select_handler,
            back_handler = self.back_handler
        )
        self.display_menu = True
        self.remaining = initial_delay
        self.x = 0
        self.y = 0
        self.face_colour = WHITE
        self.eye_colour = BLACK
        self.eye_state = "open"

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

    def update_blinking(self, delta):
        self.blink_progress = self.blink_progress + 1
        p = self.blink_progress
        if p < 5:
            self.eye_state = "closed"
        elif p < 20:
            self.eye_state = "open"
        elif p < 22:
            self.eye_state = "closed"
        elif p < 24:
            self.eye_state = "open"
        elif p < 26:
            self.eye_state = "closed"
        else:
            self.eye_state = "open"
            self.state = "looking"
            self.blink_progress = 0
            self.remaining = new_delay()

    def update(self, delta):
        if self.display_menu:
            self.menu.update(delta)
        else:
            if self.state == "blinking":
                self.update_blinking(delta)
            else:
                if self.remaining <= 0:
                    self.delay_callback()
                self.remaining = self.remaining - 1

    def draw_pride_background(self, ctx):
        colour(ctx, RED)
        ctx.rectangle(-120, -120, 240, 240).fill()
        colour(ctx, ORANGE)
        ctx.rectangle(-120, -80, 240, 240).fill()
        colour(ctx, YELLOW)
        ctx.rectangle(-120, -40, 240, 240).fill()
        colour(ctx, GREEN)
        ctx.rectangle(-120, -0, 240, 240).fill()
        colour(ctx, BLUE)
        ctx.rectangle(-120, 40, 240, 240).fill()
        colour(ctx, PURPLE)
        ctx.rectangle(-120, 80, 240, 240).fill()

    def draw_space_background(self, ctx):
        colour(ctx, DARK_BLUE)
        ctx.rectangle(-120, -120, 240, 240).fill()
        for x, y, size, brightness in stars:
            ctx.rgba(1, 1, 1, brightness)
            ctx.rectangle(x, y, size, size).fill()

    def draw_open_eyes(self, ctx):
        colour(ctx, self.eye_colour)
        # draw left eye
        ctx.rectangle(
            self.x - (x_gap / 2) - (ew / 2),
            self.y - (eh / 2),
            ew,
            eh
        ).fill()

        # draw right eye
        ctx.rectangle(
            self.x + (x_gap / 2) - (ew / 2),
            self.y - (eh / 2),
            ew,
            eh
        ).fill()

    def draw_closed_eyes(self, ctx):
        colour(ctx, self.eye_colour)
        # draw left eye
        ctx.rectangle(
            self.x - (x_gap / 2) - (eh / 4),
            self.y - (ew / 2),
            eh / 2,
            ew / 2
        ).fill()

        # draw right eye
        ctx.rectangle(
            self.x + (x_gap / 2) - (eh / 4),
            self.y - (ew / 2),
            eh / 2,
            ew / 2
        ).fill()

    def draw_face(self, ctx):
        # background
        if self.face_colour == "pride":
            self.draw_pride_background(ctx)
        elif self.face_colour == "space":
            self.draw_space_background(ctx)
        else:
            colour(ctx, self.face_colour)
            ctx.rectangle(-120, -120, 240, 240).fill()

        if self.eye_state == "open":
            self.draw_open_eyes(ctx)
        else:
            self.draw_closed_eyes(ctx)

    def draw(self, ctx):
        clear_background(ctx)

        if self.display_menu:
            self.menu.draw(ctx)
        else:
            self.draw_face(ctx)

    # @TODO: this is kinda ugly state management
    def delay_callback(self):
        if (self.x == 0 and self.y == 0):
            if random() < blink_chance:
                self.state = "blinking"
            else:
                new_x, new_y = rand_nth(positions)
                self.remaining = glance_delay
                self.x = new_x
                self.y = new_y
        else:
            new_x, new_y = initial_position
            self.remaining = new_delay()
            self.x = new_x
            self.y = new_y

__app_export__ = EyesApp
