"""Car entity with physics, movement, and isometric rendering."""

import pygame
import math
from constants import (
    CAR_WIDTH, CAR_HEIGHT, CAR_MAX_SPEED, CAR_ACCELERATION,
    CAR_BRAKING, CAR_FRICTION, CAR_TURN_RATE,
)
from iso_utils import world_to_iso


class Car(pygame.sprite.Sprite):
    """A racing car with physics-based movement."""

    def __init__(self, x, y, color, is_player=False):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.is_player = is_player

        # Physics
        self.vx = 0  # velocity x
        self.vy = 0  # velocity y
        self.angle = 0  # facing direction in radians
        self.speed = 0  # magnitude of velocity

        # State
        self.throttle = 0  # -1 (brake), 0 (idle), 1 (accelerate)
        self.steer = 0  # -1 (left), 0 (straight), 1 (right)

        # Lap tracking
        self.current_waypoint = 0
        self.laps_completed = 0
        self.lap_time = 0
        self.finished = False

        # Sprite
        self.image = self._create_sprite()
        self.rect = self.image.get_rect()
        self.update_rect()

    def _create_sprite(self):
        """Create a simple car sprite (rectangle with direction indicator)."""
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)

        # Car body
        pygame.draw.rect(surf, self.color, (0, 0, CAR_WIDTH, CAR_HEIGHT))
        pygame.draw.rect(surf, (255, 255, 255), (0, 0, CAR_WIDTH, CAR_HEIGHT), 2)

        # Direction indicator (front of car)
        pygame.draw.circle(surf, (255, 255, 255), (CAR_WIDTH // 2, 3), 2)

        return surf

    def update(self, keys=None, track=None):
        """Update car physics and position."""
        if keys:
            self._handle_input(keys)

        # Apply throttle
        if self.throttle > 0:
            # Accelerate in facing direction
            accel = CAR_ACCELERATION * self.throttle
            self.speed = min(self.speed + accel, CAR_MAX_SPEED)
        elif self.throttle < 0:
            # Brake
            self.speed = max(self.speed - CAR_BRAKING, 0)
        else:
            # Friction
            self.speed = max(self.speed - CAR_FRICTION, 0)

        # Apply steering
        if self.steer != 0:
            self.angle += CAR_TURN_RATE * self.steer * (1 + self.speed / CAR_MAX_SPEED)

        # Calculate velocity from speed and angle
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed

        # Update position
        new_x = self.x + self.vx
        new_y = self.y + self.vy

        # Check track boundaries
        if track:
            if track.is_on_track(new_x, new_y):
                self.x = new_x
                self.y = new_y
            else:
                # Bounce/slide on grass
                self.speed *= 0.7  # Slow down on off-road
                self.x += self.vx * 0.3
                self.y += self.vy * 0.3
        else:
            self.x = new_x
            self.y = new_y

        # Update lap timer
        if not self.finished:
            self.lap_time += 1

        self.update_rect()
        self.throttle = 0  # Reset each frame
        self.steer = 0

    def _handle_input(self, keys):
        """Handle keyboard input for player car."""
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.throttle = 1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.throttle = -1

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.steer = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.steer = 1

    def update_rect(self):
        """Update sprite position and rotation for rendering."""
        # Rotate sprite to face direction
        rotated = pygame.transform.rotate(self.image, -math.degrees(self.angle))
        self.rect = rotated.get_rect(center=self.get_screen_pos())

    def get_screen_pos(self, camera_x=0, camera_y=0):
        """Get the screen position of the car in isometric view."""
        iso_x, iso_y = world_to_iso(self.x, self.y)
        screen_x = iso_x - camera_x + 500
        screen_y = iso_y - camera_y + 350
        return screen_x, screen_y

    def draw(self, screen, camera_x=0, camera_y=0):
        """Draw the car on screen with proper rotation."""
        rotated = pygame.transform.rotate(self.image, -math.degrees(self.angle))
        rect = rotated.get_rect(center=self.get_screen_pos(camera_x, camera_y))
        screen.blit(rotated, rect)

    def set_waypoint(self, waypoint_index):
        """Update current waypoint."""
        self.current_waypoint = waypoint_index

    def finish_lap(self):
        """Called when car crosses finish line."""
        self.laps_completed += 1
        self.lap_time = 0

    def finish_race(self):
        """Called when car completes final lap."""
        self.finished = True