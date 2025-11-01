"""
Storage House - A building where inventory is stored
"""
import pygame
import math
import time


class StorageHouse:
    """A decorative house that represents the storage/inventory system"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 80
        self.height = 90

        # Create clickable rect
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # Animation for chimney smoke
        self.smoke_particles = []
        self.last_smoke_spawn = time.time()
        self.smoke_spawn_interval = 0.5  # Spawn smoke every 0.5 seconds

    def update(self):
        """Update house animations"""
        current_time = time.time()

        # Spawn smoke particles from chimney
        if current_time - self.last_smoke_spawn > self.smoke_spawn_interval:
            self.smoke_particles.append({
                'x': self.x + 60,
                'y': self.y + 10,
                'offset_x': 0,
                'offset_y': 0,
                'spawn_time': current_time,
                'lifetime': 2.0
            })
            self.last_smoke_spawn = current_time

        # Update smoke particles
        for particle in self.smoke_particles[:]:
            elapsed = current_time - particle['spawn_time']
            if elapsed > particle['lifetime']:
                self.smoke_particles.remove(particle)
            else:
                # Smoke rises and drifts
                particle['offset_y'] -= 0.5
                particle['offset_x'] += math.sin(elapsed * 2) * 0.3

    def draw(self, screen):
        """Draw the storage house"""
        x, y = self.x, self.y

        # Draw house base (walls)
        house_rect = pygame.Rect(x, y + 30, self.width, 60)
        pygame.draw.rect(screen, (139, 90, 43), house_rect)  # Brown walls
        pygame.draw.rect(screen, (101, 67, 33), house_rect, 3)  # Darker brown outline

        # Draw roof
        roof_points = [
            (x + self.width // 2, y),  # Top center
            (x - 5, y + 35),  # Bottom left
            (x + self.width + 5, y + 35)  # Bottom right
        ]
        pygame.draw.polygon(screen, (150, 50, 50), roof_points)  # Red roof
        pygame.draw.polygon(screen, (120, 30, 30), roof_points, 3)  # Dark red outline

        # Draw chimney
        chimney_rect = pygame.Rect(x + 55, y + 10, 12, 25)
        pygame.draw.rect(screen, (120, 30, 30), chimney_rect)
        pygame.draw.rect(screen, (80, 20, 20), chimney_rect, 2)

        # Draw door
        door_rect = pygame.Rect(x + 30, y + 55, 20, 35)
        pygame.draw.rect(screen, (101, 67, 33), door_rect)  # Dark brown door
        pygame.draw.rect(screen, (70, 45, 20), door_rect, 2)  # Darker outline

        # Door knob
        pygame.draw.circle(screen, (255, 215, 0), (x + 45, y + 72), 2)  # Gold knob

        # Draw windows
        # Left window
        left_window = pygame.Rect(x + 10, y + 45, 15, 15)
        pygame.draw.rect(screen, (135, 206, 235), left_window)  # Sky blue
        pygame.draw.rect(screen, (70, 45, 20), left_window, 2)
        # Window cross
        pygame.draw.line(screen, (70, 45, 20), (x + 17, y + 45), (x + 17, y + 60), 1)
        pygame.draw.line(screen, (70, 45, 20), (x + 10, y + 52), (x + 25, y + 52), 1)

        # Right window
        right_window = pygame.Rect(x + 55, y + 45, 15, 15)
        pygame.draw.rect(screen, (135, 206, 235), right_window)  # Sky blue
        pygame.draw.rect(screen, (70, 45, 20), right_window, 2)
        # Window cross
        pygame.draw.line(screen, (70, 45, 20), (x + 62, y + 45), (x + 62, y + 60), 1)
        pygame.draw.line(screen, (70, 45, 20), (x + 55, y + 52), (x + 70, y + 52), 1)

        # Draw smoke from chimney
        for particle in self.smoke_particles:
            px = int(particle['x'] + particle['offset_x'])
            py = int(particle['y'] + particle['offset_y'])

            # Calculate alpha based on lifetime
            elapsed = time.time() - particle['spawn_time']
            alpha = max(0, 1 - (elapsed / particle['lifetime']))

            if alpha > 0:
                # Draw smoke puff (light gray circle)
                size = int(3 + (elapsed * 2))
                color_value = int(200 * alpha)
                pygame.draw.circle(screen, (color_value, color_value, color_value), (px, py), size)

        # Draw sign above door
        sign_rect = pygame.Rect(x + 25, y + 45, 30, 8)
        pygame.draw.rect(screen, (139, 90, 43), sign_rect)
        pygame.draw.rect(screen, (70, 45, 20), sign_rect, 1)

        # Optional: Draw "LAGER" text on sign (Storage in German)
        font = pygame.font.Font(None, 12)
        sign_text = font.render("LAGER", True, (70, 45, 20))
        screen.blit(sign_text, (x + 26, y + 46))

    def is_clicked(self, mouse_pos):
        """Check if the house was clicked"""
        return self.rect.collidepoint(mouse_pos)
