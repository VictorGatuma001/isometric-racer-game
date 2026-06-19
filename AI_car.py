"""AI car that races autonomously around the track."""

import math
from car import Car
from constants import AI_ACCELERATION, AI_BRAKE_DISTANCE, AI_TURN_RATE
from iso_utils import distance, angle_to_point, shortest_angle_diff, clamp_angle


class AICar(Car):
    """An AI-controlled racing car."""

    def __init__(self, x, y, color, track):
        super().__init__(x, y, color, is_player=False)
        self.track = track
        self.target_waypoint = 1
        self.ai_turn_rate = AI_TURN_RATE

    def update(self, keys=None, track=None):
        """Update AI car with autonomous behavior."""
        track = track or self.track

        # AI decision-making
        self._ai_think(track)

        # Apply physics (same as player car)
        if self.throttle > 0:
            accel = AI_ACCELERATION * self.throttle
            self.speed = min(self.speed + accel, 5.5)  # Slightly slower than player
        elif self.throttle < 0:
            self.speed = max(self.speed - 0.2, 0)
        else:
            self.speed = max(self.speed - 0.05, 0)

        # Apply steering
        if self.steer != 0:
            self.angle += self.ai_turn_rate * self.steer * (1 + self.speed / 5.5)

        # Calculate velocity
        import math as m
        self.vx = m.cos(self.angle) * self.speed
        self.vy = m.sin(self.angle) * self.speed

        # Update position with collision
        new_x = self.x + self.vx
        new_y = self.y + self.vy

        if track.is_on_track(new_x, new_y):
            self.x = new_x
            self.y = new_y
        else:
            self.speed *= 0.6
            self.x += self.vx * 0.2
            self.y += self.vy * 0.2

        # Lap tracking
        if not self.finished:
            self.lap_time += 1

        self.update_rect()
        self.throttle = 0
        self.steer = 0

    def _ai_think(self, track):
        """AI decision-making: steer toward waypoint and control throttle."""
        target = track.get_waypoint(self.target_waypoint)
        tx, ty = target

        # Distance to target waypoint
        dist_to_target = distance(self.x, self.y, tx, ty)

        # Angle toward target
        target_angle = angle_to_point(self.x, self.y, tx, ty)

        # Current angle difference
        angle_diff = shortest_angle_diff(self.angle, target_angle)

        # Steering: turn toward target
        if abs(angle_diff) > 0.1:
            self.steer = 1 if angle_diff > 0 else -1
        else:
            self.steer = 0

        # Throttle: accelerate normally, brake if turning hard or near waypoint
        if abs(angle_diff) > 1.0 or dist_to_target < AI_BRAKE_DISTANCE:
            self.throttle = 0.5  # Light throttle while turning
        else:
            self.throttle = 1.0  # Full throttle on straights

        # Check if reached waypoint (get next one)
        if dist_to_target < 80:
            self.target_waypoint = track.get_next_waypoint(self.target_waypoint)

    def set_track(self, track):
        """Set the track reference."""
        self.track = track