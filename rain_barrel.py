"""
Rain Barrel - Visual representation of the water collection system
"""
import pygame
import math
import time


class RainBarrel:
    """A decorative rain barrel that collects water during rain"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40

        # Animation for water drops during rain
        self.water_drops = []
        self.last_drop_spawn = time.time()
        self.drop_spawn_interval = 0.2  # Drop every 0.2 seconds when raining

    def update(self, weather='sunny'):
        """Update rain barrel animations"""
        current_time = time.time()

        # Spawn water drops during rain
        if weather == 'rainy':
            if current_time - self.last_drop_spawn > self.drop_spawn_interval:
                self.water_drops.append({
                    'x': self.x + self.width // 2 + random.randint(-5, 5),
                    'y': self.y - 10,
                    'velocity': random.randint(80, 120),
                    'spawn_time': current_time,
                    'lifetime': 1.0
                })
                self.last_drop_spawn = current_time

        # Update water drops
        for drop in self.water_drops[:]:
            elapsed = current_time - drop['spawn_time']
            if elapsed > drop['lifetime']:
                self.water_drops.remove(drop)
            else:
                drop['y'] += drop['velocity'] * (1/60.0)

    def draw(self, screen):
        """Draw the rain barrel"""
        x, y = self.x, self.y

        # Draw barrel body (brown cylinder)
        barrel_rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(screen, (101, 67, 33), barrel_rect)  # Dark brown
        pygame.draw.rect(screen, (70, 45, 20), barrel_rect, 2)  # Darker outline

        # Draw barrel bands (metal rings)
        band_y_positions = [y + 10, y + 20, y + 30]
        for band_y in band_y_positions:
            pygame.draw.line(screen, (150, 150, 150), (x, band_y), (x + self.width, band_y), 2)

        # Draw barrel lid (gray oval)
        lid_rect = pygame.Rect(x - 2, y - 5, self.width + 4, 8)
        pygame.draw.ellipse(screen, (120, 120, 120), lid_rect)
        pygame.draw.ellipse(screen, (80, 80, 80), lid_rect, 2)

        # Draw water level indicator (blue rectangle inside)
        water_height = 25  # Assume always has some water
        water_rect = pygame.Rect(x + 3, y + self.height - water_height, self.width - 6, water_height)
        pygame.draw.rect(screen, (0, 150, 200), water_rect)

        # Draw water drops falling into barrel
        for drop in self.water_drops:
            if drop['y'] < y + self.height:
                pygame.draw.circle(screen, (0, 191, 255),
                                 (int(drop['x']), int(drop['y'])), 2)

        # Draw splash effect when drops hit water
        for drop in self.water_drops:
            if y + self.height - 5 < drop['y'] < y + self.height + 5:
                # Small splash ripple
                elapsed = time.time() - drop['spawn_time']
                ripple_radius = int(3 + elapsed * 10)
                if ripple_radius < 8:
                    pygame.draw.circle(screen, (0, 191, 255),
                                     (int(drop['x']), y + self.height - water_height),
                                     ripple_radius, 1)


import random
