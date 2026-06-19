"""Racing track generation and collision detection."""

import pygame
import math
from constants import TRACK_WAYPOINTS, TRACK_WIDTH, COLOR_ROAD, COLOR_ROAD_LINE, COLOR_GRASS
from iso_utils import world_to_iso, distance


class Track:
    """Represents the racing track with waypoints and collision detection."""

    def __init__(self):
        self.waypoints = TRACK_WAYPOINTS
        self.track_width = TRACK_WIDTH
        self.lap_finish_line = self._create_finish_line()

    def _create_finish_line(self):
        """Create the finish line (between first two waypoints)."""
        p1 = self.waypoints[0]
        p2 = self.waypoints[1]
        return (p1, p2)

    def get_next_waypoint(self, current_waypoint_index):
        """Get the next waypoint index."""
        return (current_waypoint_index + 1) % len(self.waypoints)

    def get_waypoint(self, index):
        """Get waypoint by index."""
        return self.waypoints[index % len(self.waypoints)]

    def is_on_track(self, x, y, car_radius=20):
        """
        Check if a position (x, y) is on the track (within road bounds).
        Returns True if on track, False if on grass/off-road.
        """
        # Find closest point on track center line
        min_dist = float('inf')
        for i in range(len(self.waypoints)):
            p1 = self.waypoints[i]
            p2 = self.waypoints[(i + 1) % len(self.waypoints)]
            dist_to_segment = self._distance_to_segment(x, y, p1, p2)
            min_dist = min(min_dist, dist_to_segment)

        # On track if within track width + some car radius
        return min_dist <= (self.track_width / 2 + car_radius)

    def _distance_to_segment(self, x, y, p1, p2):
        """Calculate perpendicular distance from (x, y) to line segment p1-p2."""
        x1, y1 = p1
        x2, y2 = p2

        # Vector from p1 to p2
        dx = x2 - x1
        dy = y2 - y1
        len_sq = dx * dx + dy * dy

        if len_sq == 0:
            return distance(x, y, x1, y1)

        # Parameter t of closest point on line segment
        t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / len_sq))

        # Closest point on segment
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

        return distance(x, y, closest_x, closest_y)

    def get_track_center_point(self, waypoint_index):
        """Get the center point of a waypoint."""
        return self.waypoints[waypoint_index % len(self.waypoints)]

    def is_lap_finished(self, prev_x, prev_y, curr_x, curr_y):
        """
        Check if the car crossed the finish line (between waypoints 0 and 1).
        Returns True if the car crosses from prev to curr position.
        """
        p1, p2 = self.lap_finish_line
        return self._crosses_line_segment(prev_x, prev_y, curr_x, curr_y, p1, p2)

    def _crosses_line_segment(self, x1, y1, x2, y2, p1, p2):
        """Check if line segment (x1,y1)-(x2,y2) crosses line segment p1-p2."""
        # Simple bounding box check first
        px1, py1 = p1
        px2, py2 = p2

        # Check if either endpoint is on different sides of the line
        def sign(px, py):
            return (px2 - px1) * (py - py1) - (py2 - py1) * (px - px1)

        s1 = sign(x1, y1)
        s2 = sign(x2, y2)

        # Crossed if signs differ (one positive, one negative)
        return s1 * s2 < 0

    def draw(self, screen, camera_x, camera_y):
        """Draw the track on the screen with camera offset."""
        # Draw grass background
        screen.fill(COLOR_GRASS)

        # Draw track segments
        for i in range(len(self.waypoints)):
            p1 = self.waypoints[i]
            p2 = self.waypoints[(i + 1) % len(self.waypoints)]
            self._draw_track_segment(screen, p1, p2, camera_x, camera_y)

    def _draw_track_segment(self, screen, p1, p2, camera_x, camera_y):
        """Draw a curved track segment between two waypoints."""
        x1, y1 = p1
        x2, y2 = p2

        # Create perpendicular offset for track width
        dx = x2 - x1
        dy = y2 - y1
        length = (dx * dx + dy * dy) ** 0.5

        if length == 0:
            return

        # Unit perpendicular vector
        perp_x = -dy / length
        perp_y = dx / length

        half_width = self.track_width / 2

        # Create quad for track (4 corners)
        corners = [
            (x1 + perp_x * half_width, y1 + perp_y * half_width),
            (x2 + perp_x * half_width, y2 + perp_y * half_width),
            (x2 - perp_x * half_width, y2 - perp_y * half_width),
            (x1 - perp_x * half_width, y1 - perp_y * half_width),
        ]

        # Convert to iso and screen coords
        iso_corners = []
        for cx, cy in corners:
            iso_x, iso_y = world_to_iso(cx, cy)
            screen_x = iso_x - camera_x + 500
            screen_y = iso_y - camera_y + 350
            iso_corners.append((screen_x, screen_y))

        # Draw road
        if len(iso_corners) >= 3:
            pygame.draw.polygon(screen, COLOR_ROAD, iso_corners)

        # Draw center line
        p1_iso_x, p1_iso_y = world_to_iso(x1, y1)
        p2_iso_x, p2_iso_y = world_to_iso(x2, y2)

        p1_screen = (p1_iso_x - camera_x + 500, p1_iso_y - camera_y + 350)
        p2_screen = (p2_iso_x - camera_x + 500, p2_iso_y - camera_y + 350)

        pygame.draw.line(screen, COLOR_ROAD_LINE, p1_screen, p2_screen, 2)