"""
Snail pest system - snails crawl from edges to eat vegetables
"""
import pygame
import random
import math
import time
from config import GARDEN_ROWS, GARDEN_COLS, GARDEN_START_X, GARDEN_START_Y, GARDEN_SPACING_X, GARDEN_SPACING_Y


class Snail:
    """A single snail that crawls from the edge toward a target vegetable"""

    def __init__(self, target_vegetable):
        self.target = target_vegetable
        self.size = 20  # Larger, more visible snail

        # Spawn from random edge
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            self.x = random.randint(100, 750)
            self.y = -30
        elif edge == 'bottom':
            self.x = random.randint(100, 750)
            self.y = 630
        elif edge == 'left':
            self.x = -30
            self.y = random.randint(100, 550)
        else:  # right
            self.x = 750
            self.y = random.randint(100, 550)

        self.speed = 15  # Pixels per second
        self.reached_target = False
        self.eating_start_time = None
        self.eating_duration = 5.0  # 5 seconds to eat

        # Create hitbox for clicking
        self.rect = pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)

    def update(self, delta_time):
        """Update snail position and eating state"""
        if self.eating_start_time:
            # Already eating
            elapsed = time.time() - self.eating_start_time
            if elapsed >= self.eating_duration:
                # Finished eating - plant should be dead
                return True  # Signal to remove snail
            return False

        # Move toward target
        target_x = self.target.x + 30  # Center of vegetable plot
        target_y = self.target.y + 30

        # Calculate direction
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        # Check if reached target
        if distance < 5:
            self.reached_target = True
            self.eating_start_time = time.time()
            return False

        # Move toward target
        if distance > 0:
            self.x += (dx / distance) * self.speed * delta_time
            self.y += (dy / distance) * self.speed * delta_time

        # Update hitbox
        self.rect.x = self.x - self.size // 2
        self.rect.y = self.y - self.size // 2

        return False

    def draw(self, screen):
        """Draw the snail"""
        x, y = int(self.x), int(self.y)

        # Draw snail body (larger oval)
        body_rect = pygame.Rect(x - 12, y - 6, 24, 12)
        pygame.draw.ellipse(screen, (139, 90, 43), body_rect)

        # Draw snail shell (larger spiral)
        shell_x = x + 5
        shell_y = y - 2
        # Outer shell
        pygame.draw.circle(screen, (101, 67, 33), (shell_x, shell_y), 10)
        # Middle shell
        pygame.draw.circle(screen, (139, 90, 43), (shell_x, shell_y), 7)
        # Inner spiral
        pygame.draw.circle(screen, (101, 67, 33), (shell_x, shell_y), 4)

        # Draw antennae
        antenna_left_x = x - 8
        antenna_right_x = x - 4
        antenna_y = y - 6
        pygame.draw.line(screen, (101, 67, 33), (antenna_left_x, y - 2), (antenna_left_x, antenna_y), 2)
        pygame.draw.line(screen, (101, 67, 33), (antenna_right_x, y - 2), (antenna_right_x, antenna_y), 2)
        pygame.draw.circle(screen, (139, 90, 43), (antenna_left_x, antenna_y), 2)
        pygame.draw.circle(screen, (139, 90, 43), (antenna_right_x, antenna_y), 2)

        # Draw eating progress bar if eating
        if self.eating_start_time:
            elapsed = time.time() - self.eating_start_time
            progress = elapsed / self.eating_duration
            bar_width = 30
            bar_height = 4
            bar_x = x - bar_width // 2
            bar_y = y + 15

            # Background
            pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            # Progress
            pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, int(bar_width * progress), bar_height))
            # Border
            pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 1)

    def is_clicked(self, mouse_pos):
        """Check if snail was clicked"""
        return self.rect.collidepoint(mouse_pos)
