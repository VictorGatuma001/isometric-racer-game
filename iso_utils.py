"""Isometric coordinate conversion and geometry utilities."""

import math
from constants import ISO_SCALE_X, ISO_SCALE_Y


def world_to_iso(x, y):
    """
    Convert world coordinates (x, y) to isometric screen coordinates.
    Isometric projection formula: screen_x, screen_y based on world coords.
    """
    # Classic isometric: rotate 45 degrees and apply perspective
    iso_x = (x - y) * ISO_SCALE_X
    iso_y = (x + y) * ISO_SCALE_Y
    return iso_x, iso_y


def iso_to_world(iso_x, iso_y):
    """
    Convert isometric screen coordinates back to world coordinates.
    Inverse of world_to_iso.
    """
    # Reverse the isometric projection
    x = (iso_x / ISO_SCALE_X + iso_y / ISO_SCALE_Y) / 2
    y = (iso_y / ISO_SCALE_Y - iso_x / ISO_SCALE_X) / 2
    return x, y


def distance(x1, y1, x2, y2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def angle_to_point(x1, y1, x2, y2):
    """
    Calculate angle (in radians) from point (x1, y1) to (x2, y2).
    0 radians points right, pi/2 points down.
    """
    return math.atan2(y2 - y1, x2 - x1)


def clamp_angle(angle):
    """Normalize angle to [-pi, pi]."""
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle


def shortest_angle_diff(angle1, angle2):
    """
    Calculate the shortest angular difference between two angles.
    Returns a value in [-pi, pi].
    """
    diff = clamp_angle(angle2 - angle1)
    return diff