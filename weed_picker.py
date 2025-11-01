"""
Weed Picker - AI helper that walks through the garden removing weeds
"""
import pygame
import random
import math
import time


class WeedPicker:
    """A helper that walks between garden plots removing weeds"""

    def __init__(self, vegetables, weather='sunny'):
        self.vegetables = vegetables
        self.size = 25
        self.weather = weather

        # Start at a random position near the garden
        self.x = random.randint(150, 600)
        self.y = random.randint(150, 500)

        self.speed = 30  # Pixels per second
        self.target_plot = None
        self.working = False
        self.work_start_time = None
        self.work_duration = 0.5  # 0.5 seconds to remove weed level (faster!)

        # Duration: 2 minutes (120 seconds)
        self.spawn_time = time.time()
        self.lifetime = 120.0

        # Walking animation
        self.walk_cycle = 0
        self.walk_speed = 5.0  # Animation speed

        # Find first weedy plot
        self._find_next_target()

    def _find_next_target(self):
        """Find the next plot with weeds"""
        weedy_plots = [v for v in self.vegetables if v.weed_level > 0]
        if weedy_plots:
            self.target_plot = random.choice(weedy_plots)
            self.working = False
        else:
            self.target_plot = None

    def update(self, delta_time):
        """Update weed picker position and working state"""
        current_time = time.time()

        # Update walking animation
        if not self.working:
            self.walk_cycle += self.walk_speed * delta_time

        # Check if lifetime expired
        if current_time - self.spawn_time >= self.lifetime:
            return True  # Signal to remove picker

        # If working on a plot
        if self.working and self.work_start_time:
            elapsed = current_time - self.work_start_time
            if elapsed >= self.work_duration:
                # Finished removing one weed level
                if self.target_plot and self.target_plot.weed_level > 0:
                    self.target_plot.remove_weeds()

                    # Check if more weeds on this plot
                    if self.target_plot.weed_level == 0:
                        # Move to next plot
                        self._find_next_target()
                    else:
                        # Continue working on this plot
                        self.work_start_time = current_time
                else:
                    # Plot is clean, find next
                    self._find_next_target()
            return False

        # If no target, find one
        if not self.target_plot:
            self._find_next_target()
            if not self.target_plot:
                # No weeds anywhere, just wander
                return False

        # Move toward target plot
        target_x = self.target_plot.x + 30
        target_y = self.target_plot.y + 30

        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        # Check if reached target
        if distance < 10:
            self.working = True
            self.work_start_time = current_time
            return False

        # Move toward target
        if distance > 0:
            self.x += (dx / distance) * self.speed * delta_time
            self.y += (dy / distance) * self.speed * delta_time

        return False

    def update_weather(self, weather):
        """Update weather state"""
        self.weather = weather

    def draw(self, screen):
        """Draw the weed picker with walking animation"""
        x, y = int(self.x), int(self.y)

        # Walking animation - bob up and down
        bob_offset = int(math.sin(self.walk_cycle) * 2) if not self.working else 0

        # Draw body (person shape)
        # Head
        pygame.draw.circle(screen, (255, 200, 150), (x, y - 10 + bob_offset), 8)

        # Body
        pygame.draw.line(screen, (100, 150, 100), (x, y - 2 + bob_offset), (x, y + 12 + bob_offset), 5)

        # Arms
        if self.working:
            # Working animation - arms down
            pygame.draw.line(screen, (100, 150, 100), (x, y + 2 + bob_offset), (x - 8, y + 10 + bob_offset), 3)
            pygame.draw.line(screen, (100, 150, 100), (x, y + 2 + bob_offset), (x + 8, y + 10 + bob_offset), 3)
        else:
            # Walking - arms swinging
            arm_swing = int(math.sin(self.walk_cycle * 2) * 3)
            pygame.draw.line(screen, (100, 150, 100), (x, y + 2 + bob_offset), (x - 8, y + 8 + bob_offset + arm_swing), 3)
            pygame.draw.line(screen, (100, 150, 100), (x, y + 2 + bob_offset), (x + 8, y + 8 + bob_offset - arm_swing), 3)

        # Legs with walking animation
        if not self.working:
            leg_offset = int(math.sin(self.walk_cycle * 2) * 4)
            pygame.draw.line(screen, (80, 100, 200), (x, y + 12 + bob_offset), (x - 5, y + 20 + bob_offset + leg_offset), 4)
            pygame.draw.line(screen, (80, 100, 200), (x, y + 12 + bob_offset), (x + 5, y + 20 + bob_offset - leg_offset), 4)
        else:
            # Standing still while working
            pygame.draw.line(screen, (80, 100, 200), (x, y + 12 + bob_offset), (x - 5, y + 20 + bob_offset), 4)
            pygame.draw.line(screen, (80, 100, 200), (x, y + 12 + bob_offset), (x + 5, y + 20 + bob_offset), 4)

        # Draw tool in hand (small hoe)
        if self.working:
            pygame.draw.line(screen, (139, 69, 19), (x + 8, y + 10 + bob_offset), (x + 12, y + 18 + bob_offset), 2)
            pygame.draw.rect(screen, (150, 150, 150), (x + 10, y + 18 + bob_offset, 4, 2))

        # Draw timer bar showing remaining time
        remaining_ratio = 1.0 - ((time.time() - self.spawn_time) / self.lifetime)
        bar_width = 40
        bar_height = 4
        bar_x = x - bar_width // 2
        bar_y = y + 25

        # Background
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        # Progress
        pygame.draw.rect(screen, (100, 200, 100), (bar_x, bar_y, int(bar_width * remaining_ratio), bar_height))
        # Border
        pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 1)

        # Draw umbrella if raining
        if self.weather == 'rainy':
            umbrella_x = x
            umbrella_y = y - 25 + bob_offset

            # Umbrella stick
            pygame.draw.line(screen, (139, 69, 19), (umbrella_x, umbrella_y),
                           (umbrella_x, y - 10 + bob_offset), 2)

            # Umbrella canopy (arc)
            umbrella_radius = 15
            # Draw semi-circle for umbrella top
            for i in range(-umbrella_radius, umbrella_radius + 1):
                height = int(math.sqrt(max(0, umbrella_radius**2 - i**2)))
                pygame.draw.line(screen, (200, 50, 50),
                               (umbrella_x + i, umbrella_y - height),
                               (umbrella_x + i, umbrella_y), 1)

            # Umbrella outline
            pygame.draw.arc(screen, (150, 30, 30),
                          (umbrella_x - umbrella_radius, umbrella_y - umbrella_radius,
                           umbrella_radius * 2, umbrella_radius * 2),
                          0, math.pi, 2)

            # Umbrella handle
            pygame.draw.circle(screen, (139, 69, 19), (umbrella_x, y - 10 + bob_offset), 2)

        # Draw working indicator
        if self.working:
            pygame.draw.circle(screen, (255, 255, 0), (x, y - 20 + bob_offset), 4)
