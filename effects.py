"""
Visual effects and particle systems
"""
import pygame
import random
import time
import math
from config import (
    YELLOW, BLACK, WATER_BLUE, WINDOW_WIDTH,
    SPARKLE_PARTICLE_COUNT, SPARKLE_LIFETIME, COIN_POPUP_LIFETIME,
    SPRINKLER_INTERVAL, SPRINKLER_THRESHOLD, SPRINKLER_WATER_INCREASE
)


class VisualEffects:
    """Manages visual effects like sparkles, coin popups, clouds, and sun"""

    def __init__(self):
        self.coin_popups = []
        self.sparkle_particles = []
        self.cloud_offset = 0
        self.sun_rotation = 0
        self.hovered_vegetable = None

    def update(self):
        """Update all visual effects"""
        current_time = time.time()

        # Update cloud animation
        self.cloud_offset = (self.cloud_offset + 0.5) % WINDOW_WIDTH

        # Update sun rotation
        self.sun_rotation = (self.sun_rotation + 0.02) % (2 * math.pi)

        # Update coin popups
        self.coin_popups = [p for p in self.coin_popups
                           if current_time - p['spawn_time'] < COIN_POPUP_LIFETIME]
        for popup in self.coin_popups:
            popup['y'] -= 0.5  # Float upward

        # Update sparkle particles
        self.sparkle_particles = [p for p in self.sparkle_particles
                                 if current_time - p['spawn_time'] < SPARKLE_LIFETIME]
        for particle in self.sparkle_particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']

    def add_coin_popup(self, x, y, amount):
        """Add a floating coin notification"""
        self.coin_popups.append({
            'x': x,
            'y': y,
            'amount': amount,
            'spawn_time': time.time()
        })

    def add_sparkles(self, x, y, color):
        """Add sparkle particles for visual feedback"""
        for i in range(SPARKLE_PARTICLE_COUNT):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)
            self.sparkle_particles.append({
                'x': x + 30,
                'y': y + 30,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'color': color,
                'size': random.randint(3, 6),
                'spawn_time': time.time()
            })

    def draw_sparkles(self, screen):
        """Draw sparkle particles"""
        for particle in self.sparkle_particles:
            age = time.time() - particle['spawn_time']
            alpha = max(0, 1 - age / SPARKLE_LIFETIME)
            if alpha > 0:
                size = int(particle['size'] * alpha)
                if size > 0:
                    x, y = int(particle['x']), int(particle['y'])
                    color = particle['color']
                    pygame.draw.circle(screen, color, (x, y), size)
                    # Add cross for star effect
                    if size > 2:
                        pygame.draw.line(screen, color, (x - size, y), (x + size, y), 2)
                        pygame.draw.line(screen, color, (x, y - size), (x, y + size), 2)

    def draw_coin_popups(self, screen, font):
        """Draw floating coin notifications"""
        for popup in self.coin_popups:
            age = time.time() - popup['spawn_time']
            alpha = max(0, 1 - age / COIN_POPUP_LIFETIME)
            if alpha > 0:
                coin_text = font.render(f"+{popup['amount']}", True, YELLOW)
                text_with_shadow = font.render(f"+{popup['amount']}", True, BLACK)
                # Shadow
                screen.blit(text_with_shadow, (int(popup['x']) + 22, int(popup['y']) - 42))
                # Main text
                screen.blit(coin_text, (int(popup['x']) + 20, int(popup['y']) - 44))

    def draw_sun(self, screen):
        """Draw animated sun with rays"""
        sun_x = WINDOW_WIDTH - 60
        sun_y = 60
        pygame.draw.circle(screen, YELLOW, (sun_x, sun_y), 25)

        # Draw rotating rays
        for i in range(12):
            angle = i * math.pi / 6 + self.sun_rotation
            start_x = sun_x + math.cos(angle) * 35
            start_y = sun_y + math.sin(angle) * 35
            end_x = sun_x + math.cos(angle) * 48
            end_y = sun_y + math.sin(angle) * 48
            thickness = 3 if i % 2 == 0 else 2
            pygame.draw.line(screen, YELLOW, (start_x, start_y), (end_x, end_y), thickness)

        # Add sun glow
        pygame.draw.circle(screen, (255, 255, 150), (sun_x, sun_y), 25, 2)

    def draw_clouds(self, screen):
        """Draw animated clouds"""
        from config import GRAY
        cloud_x = WINDOW_WIDTH - 90 + int(self.cloud_offset * 0.1) % 50
        pygame.draw.ellipse(screen, GRAY, (cloud_x, 40, 60, 30))
        pygame.draw.ellipse(screen, GRAY, (cloud_x + 20, 35, 50, 25))
        pygame.draw.ellipse(screen, GRAY, (cloud_x + 5, 50, 40, 20))

        # Second cloud
        cloud2_x = cloud_x - 150
        if cloud2_x < -100:
            cloud2_x += WINDOW_WIDTH + 100
        pygame.draw.ellipse(screen, (150, 150, 150), (cloud2_x, 80, 50, 25))
        pygame.draw.ellipse(screen, (150, 150, 150), (cloud2_x + 15, 75, 40, 20))

    def update_hover(self, mouse_pos, vegetables):
        """Update which vegetable is being hovered over"""
        self.hovered_vegetable = None
        for vegetable in vegetables:
            if vegetable.rect.collidepoint(mouse_pos):
                self.hovered_vegetable = vegetable
                break

    def draw_hover_effect(self, screen, font):
        """Draw hover effect and tooltip"""
        if self.hovered_vegetable:
            vegetable = self.hovered_vegetable
            glow_rect = pygame.Rect(vegetable.x - 4, vegetable.y - 4, 68, 68)
            pygame.draw.rect(screen, (255, 255, 100), glow_rect, 3)

            # Draw tooltip
            if not vegetable.plant_dead:
                from config import WHITE, BLACK, YELLOW
                if vegetable.grown:
                    tooltip_text = font.render(f"Bereit zum Ernten! +{vegetable.credits[vegetable.type]}", True, WHITE)
                else:
                    remaining = max(0, vegetable.regrow_time - time.time())
                    tooltip_text = font.render(f"Wächst... {remaining:.1f}s", True, WHITE)
                tooltip_bg = pygame.Rect(vegetable.x - 10, vegetable.y - 40, tooltip_text.get_width() + 10, 25)
                pygame.draw.rect(screen, BLACK, tooltip_bg)
                pygame.draw.rect(screen, YELLOW, tooltip_bg, 1)
                screen.blit(tooltip_text, (vegetable.x - 5, vegetable.y - 35))

    def draw_growth_progress(self, screen, vegetable):
        """Draw growth progress bar for growing plants"""
        if not vegetable.plant_dead and not vegetable.grown:
            from config import GREEN, BLACK
            total_time = 8  # Average regrow time
            elapsed = total_time - max(0, vegetable.regrow_time - time.time())
            progress = min(1.0, elapsed / total_time)

            bar_width = 50
            bar_height = 5
            bar_x = vegetable.x + 5
            bar_y = vegetable.y - 10

            # Background bar
            pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            # Progress bar
            pygame.draw.rect(screen, GREEN, (bar_x, bar_y, int(bar_width * progress), bar_height))
            # Border
            pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height), 1)


class SprinklerSystem:
    """Manages sprinkler system effects and functionality"""

    def __init__(self):
        self.last_sprinkler_time = time.time()
        self.sprinkler_particles = []
        self.permanent_sprinkler_particles = []
        self.active = False

    def activate(self):
        """Activate the sprinkler system"""
        self.active = True

    def update(self, vegetables):
        """Update sprinkler system"""
        if not self.active:
            return

        current_time = time.time()

        # Initialize permanent particles if needed
        if len(self.permanent_sprinkler_particles) == 0:
            for vegetable in vegetables:
                for i in range(5):
                    particle = {
                        'x': vegetable.x + 30 + random.randint(-15, 15),
                        'y': vegetable.y - 10 + random.randint(-5, 5),
                        'base_y': vegetable.y - 10,
                        'oscillation': random.uniform(0, 6.28),
                        'speed': random.uniform(0.02, 0.05)
                    }
                    self.permanent_sprinkler_particles.append(particle)

        # Animate particles
        for particle in self.permanent_sprinkler_particles:
            particle['oscillation'] += particle['speed']
            particle['y'] = particle['base_y'] + math.sin(particle['oscillation']) * 3

        # Water vegetables periodically
        if current_time - self.last_sprinkler_time > SPRINKLER_INTERVAL:
            for vegetable in vegetables:
                if not vegetable.plant_dead and vegetable.soil_moisture < SPRINKLER_THRESHOLD:
                    vegetable.soil_moisture = min(1.0, vegetable.soil_moisture + SPRINKLER_WATER_INCREASE)
            self.last_sprinkler_time = current_time

        # Clean up old temporary particles
        self.sprinkler_particles = [p for p in self.sprinkler_particles
                                   if current_time - p['spawn_time'] < 1.5]

        # Update temporary particles
        for particle in self.sprinkler_particles:
            time_passed = current_time - particle['spawn_time']
            particle['y'] += particle['velocity'] * time_passed
            particle['velocity'] += 50 * time_passed

    def draw(self, screen, vegetables):
        """Draw sprinkler system"""
        if not self.active:
            return

        from config import GRAY

        # Draw sprinkler heads
        for row in range(3):
            for col in range(4):
                from config import GARDEN_START_X, GARDEN_START_Y, GARDEN_SPACING_X, GARDEN_SPACING_Y
                x = GARDEN_START_X + col * GARDEN_SPACING_X + 45
                y = GARDEN_START_Y + row * GARDEN_SPACING_Y - 25
                pygame.draw.rect(screen, GRAY, (x, y, 10, 15))
                pygame.draw.circle(screen, (100, 100, 100), (x + 5, y + 5), 3)

        # Draw permanent particles
        for particle in self.permanent_sprinkler_particles:
            pygame.draw.circle(screen, WATER_BLUE,
                             (int(particle['x']), int(particle['y'])), 2)

        # Draw temporary particles
        for particle in self.sprinkler_particles:
            alpha = max(0, 1 - (time.time() - particle['spawn_time']) / 1.5)
            if alpha > 0:
                size = int(2 * alpha)
                if size > 0:
                    pygame.draw.circle(screen, WATER_BLUE,
                                     (int(particle['x']), int(particle['y'])), size)
