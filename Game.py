"""Main game logic, race management, and rendering."""

import pygame
import math
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_BG, COLOR_WHITE, COLOR_RED,
    COLOR_BLUE, COLOR_GREEN, COLOR_YELLOW, COLOR_BLACK, AI_COLORS,
)
from track import Track
from car import Car
from ai_car import AICar
from iso_utils import world_to_iso, distance


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Isometric Racing")
        self.clock = pygame.time.Clock()
        self.running = True

        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)

        self.state = "menu"  # menu, racing, finished
        self.reset_race()

    def reset_race(self):
        """Initialize a new race."""
        self.track = Track()

        # Create player car
        start_x, start_y = self.track.waypoints[0]
        self.player = Car(start_x, start_y, COLOR_RED, is_player=True)

        # Create AI cars
        self.ai_cars = []
        for i, color in enumerate(AI_COLORS):
            offset_x = (i + 1) * 30
            offset_y = (i + 1) * 30
            ai = AICar(start_x + offset_x, start_y + offset_y, color, self.track)
            self.ai_cars.append(ai)

        self.all_cars = [self.player] + self.ai_cars
        self.total_laps = 3
        self.race_time = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.state == "menu" and event.key == pygame.K_SPACE:
                    self.state = "racing"
                    self.reset_race()
                elif self.state == "finished" and event.key == pygame.K_SPACE:
                    self.state = "menu"

        if self.state == "racing":
            self.player.update(keys, self.track)

    def update(self):
        if self.state != "racing":
            return

        self.race_time += 1

        # Update AI cars
        for ai in self.ai_cars:
            ai.update(track=self.track)

        # Check lap completion for all cars
        for car in self.all_cars:
            prev_x = car.x - car.vx
            prev_y = car.y - car.vy

            if self.track.is_lap_finished(prev_x, prev_y, car.x, car.y):
                car.finish_lap()

        # Check race completion
        for car in self.all_cars:
            if car.laps_completed >= self.total_laps and not car.finished:
                car.finish_race()

        # Check if player finished
        if self.player.finished:
            self.state = "finished"

    def draw(self):
        self.screen.fill(COLOR_BG)

        if self.state == "menu":
            self.draw_menu()
        elif self.state == "racing":
            self.draw_racing()
        elif self.state == "finished":
            self.draw_finished()

        pygame.display.flip()

    def draw_menu(self):
        title = self.font_large.render("ISOMETRIC RACER", True, COLOR_WHITE)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))

        instructions = [
            "ARROW KEYS or WASD to steer and accelerate",
            "Race 3 laps around the track",
            "Beat the AI opponents!",
            "",
            "Press SPACE to start",
        ]

        y = 300
        for line in instructions:
            text = self.font_medium.render(line, True, COLOR_WHITE)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y))
            y += 50

    def draw_racing(self):
        # Camera follows player
        camera_x, camera_y = world_to_iso(self.player.x, self.player.y)

        # Draw track
        self.track.draw(self.screen, camera_x, camera_y)

        # Draw all cars
        for car in self.all_cars:
            car.draw(self.screen, camera_x, camera_y)

        # Draw HUD
        self.draw_hud()

    def draw_hud(self):
        """Draw heads-up display with lap times and positions."""
        # Player info
        player_text = f"LAP {self.player.laps_completed + 1}/{self.total_laps}  TIME {self.player.lap_time // 60}s"
        text = self.font_small.render(player_text, True, COLOR_RED)
        self.screen.blit(text, (10, 10))

        # Race timer
        race_secs = self.race_time // 60
        timer_text = f"Race Time: {race_secs}s"
        text = self.font_small.render(timer_text, True, COLOR_WHITE)
        self.screen.blit(text, (10, 40))

        # Positions
        positions = self.get_race_positions()
        y = 80
        for i, (car, laps, time) in enumerate(positions):
            color = COLOR_RED if car == self.player else car.color
            pos_text = f"{i + 1}. Lap {laps} - {time}s"
            text = self.font_small.render(pos_text, True, color)
            self.screen.blit(text, (10, y))
            y += 30

    def get_race_positions(self):
        """Calculate current race positions."""

        # Sort by laps, then by progress to next waypoint
        def car_position(car):
            progress = distance(
                car.x, car.y,
                self.track.get_waypoint(car.current_waypoint)[0],
                self.track.get_waypoint(car.current_waypoint)[1],
            )
            return (-car.laps_completed, progress)

        sorted_cars = sorted(self.all_cars, key=car_position)
        return [(car, car.laps_completed, car.lap_time // 60) for car in sorted_cars]

    def draw_finished(self):
        positions = self.get_race_positions()

        title_text = "RACE FINISHED!"
        if positions[0][0] == self.player:
            title_text = "YOU WIN!"
            color = COLOR_RED
        else:
            title_text = "YOU FINISHED"
            color = COLOR_WHITE

        title = self.font_large.render(title_text, True, color)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        # Final standings
        y = 200
        standings_text = self.font_medium.render("Final Standings:", True, COLOR_WHITE)
        self.screen.blit(standings_text, (SCREEN_WIDTH // 2 - standings_text.get_width() // 2, y))
        y += 50

        for i, (car, laps, time) in enumerate(positions):
            car_name = "YOU" if car == self.player else f"AI {self.ai_cars.index(car) + 1}"
            pos_text = f"{i + 1}. {car_name} - {time}s"
            text = self.font_small.render(pos_text, True, car.color)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y))
            y += 40

        restart = self.font_small.render("Press SPACE to return to menu", True, COLOR_WHITE)
        self.screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 600))

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()