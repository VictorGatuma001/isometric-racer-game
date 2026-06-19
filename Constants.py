"""Game configuration and constants for isometric racer."""

import math

# Screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# Colors
COLOR_BG = (50, 120, 80)        # grass green
COLOR_ROAD = (60, 60, 60)       # dark gray
COLOR_ROAD_LINE = (255, 255, 200)
COLOR_GRASS = (40, 100, 60)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 50, 50)
COLOR_BLUE = (50, 100, 255)
COLOR_GREEN = (50, 255, 100)
COLOR_YELLOW = (255, 255, 50)
COLOR_BLACK = (0, 0, 0)

# Isometric projection constants
ISO_ANGLE = math.radians(30)  # 30 degrees for classic isometric
ISO_SCALE_X = math.cos(ISO_ANGLE)
ISO_SCALE_Y = math.sin(ISO_ANGLE)

# Car properties
CAR_WIDTH = 24
CAR_HEIGHT = 40
CAR_MAX_SPEED = 6.0
CAR_ACCELERATION = 0.15
CAR_BRAKING = 0.2
CAR_FRICTION = 0.05
CAR_TURN_RATE = 0.08  # radians per frame

# Track
TRACK_WIDTH = 150
TRACK_WAYPOINTS = [
    (500, 100),    # start/finish
    (700, 150),
    (800, 350),
    (700, 550),
    (400, 600),
    (150, 550),
    (50, 350),
    (150, 150),
]

# AI
AI_ACCELERATION = 0.12
AI_BRAKE_DISTANCE = 200
AI_TURN_RATE = 0.07
AI_COLORS = [COLOR_BLUE, COLOR_GREEN, COLOR_YELLOW]

# UI
FONT_SIZE_LARGE = 36
FONT_SIZE_MEDIUM = 24
FONT_SIZE_SMALL = 16