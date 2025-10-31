"""
Duck - Cute helper that walks through the garden eating snails
"""
import pygame
import random
import math
import time


class Duck:
    """A cute duck that walks between garden plots eating snails"""

    def __init__(self, snails):
        self.snails = snails
        self.size = 30

        # Start at a random position near the garden
        self.x = random.randint(150, 600)
        self.y = random.randint(150, 500)

        self.speed = 40  # Pixels per second
        self.target_snail = None
        self.eating = False
        self.eat_start_time = None
        self.eat_duration = 0.8  # 0.8 seconds to eat a snail

        # Duration: 2 minutes (120 seconds)
        self.spawn_time = time.time()
        self.lifetime = 120.0

        # Walking animation
        self.walk_cycle = 0
        self.walk_speed = 5.0  # Animation speed

        # Find first snail
        self._find_next_target()

    def _find_next_target(self):
        """Find the next snail to eat"""
        if self.snails:
            self.target_snail = random.choice(self.snails)
            self.eating = False
        else:
            self.target_snail = None

    def update(self, delta_time):
        """Update duck position and eating state"""
        current_time = time.time()

        # Update walking animation
        self.walk_cycle += self.walk_speed * delta_time

        # Check if lifetime expired
        if current_time - self.spawn_time >= self.lifetime:
            return True  # Signal to remove duck

        # If eating a snail
        if self.eating and self.eat_start_time:
            elapsed = current_time - self.eat_start_time
            if elapsed >= self.eat_duration:
                # Finished eating snail
                if self.target_snail in self.snails:
                    self.snails.remove(self.target_snail)

                # Find next snail
                self._find_next_target()
            return False

        # If no target, find one
        if not self.target_snail or self.target_snail not in self.snails:
            self._find_next_target()
            if not self.target_snail:
                # No snails anywhere, just wander randomly
                return False

        # Move toward target snail
        target_x = self.target_snail.x
        target_y = self.target_snail.y

        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        # Check if reached target
        if distance < 15:
            self.eating = True
            self.eat_start_time = current_time
            return False

        # Move toward target
        if distance > 0:
            self.x += (dx / distance) * self.speed * delta_time
            self.y += (dy / distance) * self.speed * delta_time

        return False

    def draw(self, screen):
        """Draw the cute duck with walking animation"""
        x, y = int(self.x), int(self.y)

        # Walking animation - bob up and down
        bob_offset = int(math.sin(self.walk_cycle) * 2) if not self.eating else 0

        # Duck body (yellow oval)
        body_rect = pygame.Rect(x - 12, y - 8 + bob_offset, 24, 16)
        pygame.draw.ellipse(screen, (255, 220, 50), body_rect)
        pygame.draw.ellipse(screen, (200, 180, 40), body_rect, 2)

        # Duck head (yellow circle)
        head_y = y - 12 + bob_offset
        pygame.draw.circle(screen, (255, 220, 50), (x + 8, head_y), 10)
        pygame.draw.circle(screen, (200, 180, 40), (x + 8, head_y), 10, 2)

        # Duck beak (orange triangle)
        if self.eating:
            # Open beak when eating
            beak_points = [
                (x + 16, head_y - 2),
                (x + 24, head_y),
                (x + 16, head_y + 2)
            ]
        else:
            # Closed beak
            beak_points = [
                (x + 16, head_y),
                (x + 22, head_y - 2),
                (x + 22, head_y + 2)
            ]
        pygame.draw.polygon(screen, (255, 140, 0), beak_points)
        pygame.draw.polygon(screen, (200, 100, 0), beak_points, 1)

        # Duck eye (black dot)
        pygame.draw.circle(screen, (0, 0, 0), (x + 12, head_y - 3), 2)

        # Duck legs with walking animation
        if not self.eating:
            leg_offset = int(math.sin(self.walk_cycle * 2) * 3)
            # Left leg
            pygame.draw.line(screen, (255, 140, 0), (x - 4, y + 8 + bob_offset),
                           (x - 4, y + 14 + bob_offset + leg_offset), 3)
            # Right leg
            pygame.draw.line(screen, (255, 140, 0), (x + 4, y + 8 + bob_offset),
                           (x + 4, y + 14 + bob_offset - leg_offset), 3)

            # Feet (webbed)
            pygame.draw.line(screen, (255, 140, 0), (x - 6, y + 14 + bob_offset + leg_offset),
                           (x - 2, y + 14 + bob_offset + leg_offset), 2)
            pygame.draw.line(screen, (255, 140, 0), (x + 2, y + 14 + bob_offset - leg_offset),
                           (x + 6, y + 14 + bob_offset - leg_offset), 2)
        else:
            # Standing still while eating
            pygame.draw.line(screen, (255, 140, 0), (x - 4, y + 8), (x - 4, y + 14), 3)
            pygame.draw.line(screen, (255, 140, 0), (x + 4, y + 8), (x + 4, y + 14), 3)
            pygame.draw.line(screen, (255, 140, 0), (x - 6, y + 14), (x - 2, y + 14), 2)
            pygame.draw.line(screen, (255, 140, 0), (x + 2, y + 14), (x + 6, y + 14), 2)

        # Draw timer bar showing remaining time
        remaining_ratio = 1.0 - ((time.time() - self.spawn_time) / self.lifetime)
        bar_width = 40
        bar_height = 4
        bar_x = x - bar_width // 2
        bar_y = y + 20

        # Background
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        # Progress
        pygame.draw.rect(screen, (255, 220, 50), (bar_x, bar_y, int(bar_width * remaining_ratio), bar_height))
        # Border
        pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 1)

        # Draw eating indicator (heart when eating snail)
        if self.eating:
            # Draw little heart above duck
            heart_x = x + 8
            heart_y = y - 25
            pygame.draw.circle(screen, (255, 100, 100), (heart_x - 3, heart_y), 4)
            pygame.draw.circle(screen, (255, 100, 100), (heart_x + 3, heart_y), 4)
            pygame.draw.polygon(screen, (255, 100, 100), [
                (heart_x - 6, heart_y + 2),
                (heart_x, heart_y + 8),
                (heart_x + 6, heart_y + 2)
            ])
