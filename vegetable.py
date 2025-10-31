"""
Vegetable class for individual garden plots
"""
import pygame
import random
import time
from config import (
    BROWN, BLACK, WHITE, RED, ORANGE, PURPLE, GREEN, WATER_BLUE,
    VEGETABLE_COLORS, VEGETABLE_CREDITS,
    MIN_REGROW_TIME, MAX_REGROW_TIME, FERTILITY_LOSS_PER_HARVEST, MIN_FERTILITY,
    BASE_MOISTURE_LOSS_RATE, MOISTURE_LOSS_SUNNY, MOISTURE_LOSS_RAINY, MOISTURE_LOSS_CLOUDY,
    RAIN_MOISTURE_GAIN, WATER_INCREASE_AMOUNT,
    WEED_CHECK_INTERVAL, WEED_SPAWN_CHANCE, WEED_GROWTH_TIME, MAX_WEED_LEVEL,
    REVIVAL_MIN_FERTILITY, REVIVAL_MIN_MOISTURE,
    SEED_PLANT_FERTILITY, SEED_PLANT_MOISTURE,
    WATER_PARTICLE_COUNT, FERTILIZER_PARTICLE_COUNT, WEED_PARTICLE_COUNT,
    WATER_PARTICLE_LIFETIME, FERTILIZER_PARTICLE_LIFETIME_MIN, FERTILIZER_PARTICLE_LIFETIME_MAX,
    WEED_PARTICLE_LIFETIME, SEED_PARTICLE_LIFETIME
)


class Vegetable:
    def __init__(self, x, y, veg_type):
        self.x = x
        self.y = y
        self.type = veg_type
        self.grown = True
        self.soil_fertility = 1.0
        self.soil_moisture = 1.0
        self.last_moisture_update = time.time()
        self.harvest_count = 0
        self.regrow_time = time.time() + random.uniform(MIN_REGROW_TIME, MAX_REGROW_TIME)
        self.rect = pygame.Rect(x, y, 60, 60)
        self.water_particles = []
        self.weed_level = 0
        self.weed_start_time = None
        self.last_weed_check = time.time()
        self.plant_dead = False
        self.weed_particles = []
        self.seed_particles = []
        self.fertilizer_particles = []

        self.colors = VEGETABLE_COLORS
        self.credits = VEGETABLE_CREDITS

    def draw(self, screen, font):
        # Draw soil
        soil_color = BROWN if self.soil_fertility > 0.5 else (89, 39, 19)
        if self.plant_dead:
            soil_color = (50, 25, 12)
        pygame.draw.rect(screen, soil_color, (self.x, self.y, 60, 60))

        # Draw plants
        if self.grown and not self.plant_dead:
            if self.type == 'tomato':
                pygame.draw.circle(screen, RED, (self.x + 30, self.y + 30), 25)
                pygame.draw.circle(screen, (139, 69, 19), (self.x + 30, self.y + 10), 5)
            elif self.type == 'carrot':
                pygame.draw.polygon(screen, ORANGE,
                                  [(self.x + 30, self.y + 20), (self.x + 25, self.y + 50), (self.x + 35, self.y + 50)])
                pygame.draw.lines(screen, (34, 139, 34), False,
                                [(self.x + 20, self.y + 15), (self.x + 30, self.y + 20), (self.x + 40, self.y + 15)], 3)
            elif self.type == 'eggplant':
                pygame.draw.ellipse(screen, PURPLE, (self.x + 20, self.y + 25, 20, 30))
                pygame.draw.circle(screen, (34, 139, 34), (self.x + 30, self.y + 25), 3)

            credit_text = font.render(f"+{self.credits[self.type]}", True, BLACK)
            screen.blit(credit_text, (self.x + 10, self.y - 20))
        elif not self.plant_dead:
            pygame.draw.rect(screen, (101, 67, 33), (self.x + 5, self.y + 5, 50, 50))
            remaining_time = max(0, self.regrow_time - time.time())
            time_text = font.render(f"{remaining_time:.1f}s", True, WHITE)
            screen.blit(time_text, (self.x + 5, self.y + 25))

        # Draw weeds
        if self.weed_level > 0:
            weed_colors = [(0, 100, 0), (0, 120, 0), (0, 80, 0)]
            weed_count = min(3 + self.weed_level, 8)

            for i in range(weed_count):
                weed_x = self.x + 5 + (i * 8) % 50 + random.randint(-2, 2)
                weed_y = self.y + 5 + (i // 6) * 15 + random.randint(-3, 3)
                weed_height = 15 + self.weed_level * 5
                weed_thickness = 1 + self.weed_level

                color = weed_colors[i % len(weed_colors)]
                pygame.draw.line(screen, color, (weed_x, weed_y + weed_height), (weed_x, weed_y), weed_thickness)
                pygame.draw.circle(screen, color, (weed_x, weed_y), 2 + self.weed_level)

        # Draw particle animations
        self._draw_particles(screen)

        # Draw UI bars
        self._draw_ui_bars(screen)

    def _draw_particles(self, screen):
        """Draw all particle effects"""
        current_time = time.time()

        # Seed particles
        for particle in self.seed_particles:
            alpha = max(0, 1 - (current_time - particle['spawn_time']) / particle['lifetime'])
            if alpha > 0:
                size = int(particle['size'] * alpha)
                if size > 0:
                    pygame.draw.circle(screen, particle['color'],
                                    (int(particle['x']), int(particle['y'])), size)
                    pygame.draw.circle(screen, BLACK,
                                    (int(particle['x']), int(particle['y'])), size, 1)

        # Fertilizer particles
        for particle in self.fertilizer_particles:
            alpha = max(0, 1 - (current_time - particle['spawn_time']) / particle['lifetime'])
            if alpha > 0:
                size = int(particle['size'] * alpha)
                if size > 0:
                    pygame.draw.circle(screen, (0, 255, 0),
                                    (int(particle['x']), int(particle['y'])), size)

        # Water particles
        for particle in self.water_particles:
            alpha = max(0, 1 - (current_time - particle['spawn_time']) / WATER_PARTICLE_LIFETIME)
            if alpha > 0:
                size = int(3 * alpha)
                if size > 0:
                    pygame.draw.circle(screen, WATER_BLUE,
                                     (int(particle['x']), int(particle['y'])), size)

        # Weed particles
        for particle in self.weed_particles:
            alpha = max(0, 1 - (current_time - particle['spawn_time']) / WEED_PARTICLE_LIFETIME)
            if alpha > 0:
                size = int(particle['size'] * alpha)
                if size > 0:
                    pygame.draw.circle(screen, particle['color'],
                                     (int(particle['x']), int(particle['y'])), size)

    def _draw_ui_bars(self, screen):
        """Draw fertility and moisture bars"""
        # Fertility bar
        fertility_bar_width = int(50 * self.soil_fertility)
        pygame.draw.rect(screen, RED, (self.x + 5, self.y + 55, 50, 3))
        pygame.draw.rect(screen, GREEN, (self.x + 5, self.y + 55, fertility_bar_width, 3))

        # Moisture bar
        moisture_bar_width = int(50 * self.soil_moisture)
        pygame.draw.rect(screen, (139, 69, 19), (self.x + 5, self.y + 59, 50, 3))
        pygame.draw.rect(screen, WATER_BLUE, (self.x + 5, self.y + 59, moisture_bar_width, 3))

    def update(self, weather='sunny'):
        """Update vegetable state"""
        current_time = time.time()
        time_passed = current_time - self.last_moisture_update

        # Update moisture based on weather
        if weather == 'sunny':
            moisture_loss_rate = BASE_MOISTURE_LOSS_RATE * MOISTURE_LOSS_SUNNY
        elif weather == 'rainy':
            moisture_loss_rate = BASE_MOISTURE_LOSS_RATE * MOISTURE_LOSS_RAINY
            self.soil_moisture = min(1.0, self.soil_moisture + RAIN_MOISTURE_GAIN * time_passed)
        else:
            moisture_loss_rate = BASE_MOISTURE_LOSS_RATE

        self.soil_moisture = max(0.0, self.soil_moisture - moisture_loss_rate * time_passed)
        self.last_moisture_update = current_time

        # Update particles
        self._update_particles(current_time, time_passed)

        # Update weeds
        self._update_weeds(current_time)

        # Check for plant death
        if self.soil_fertility <= 0 or self.soil_moisture <= 0:
            self.plant_dead = True
            self.grown = False

        # Check for regrowth
        if not self.grown and current_time >= self.regrow_time and not self.plant_dead:
            self.grown = True

    def _update_particles(self, current_time, time_passed):
        """Update all particle animations"""
        # Water particles
        self.water_particles = [p for p in self.water_particles
                               if current_time - p['spawn_time'] < WATER_PARTICLE_LIFETIME]
        for particle in self.water_particles:
            particle['y'] += particle['velocity'] * time_passed
            particle['velocity'] += 50 * time_passed

        # Weed particles
        self.weed_particles = [p for p in self.weed_particles
                              if current_time - p['spawn_time'] < WEED_PARTICLE_LIFETIME]
        for particle in self.weed_particles:
            particle['x'] += particle['vx'] * time_passed * 30
            particle['y'] += particle['vy'] * time_passed * 30
            particle['vy'] += particle['gravity'] * time_passed * 30
            particle['rotation'] += time_passed * 180

        # Seed particles
        self.seed_particles = [p for p in self.seed_particles
                              if current_time - p['spawn_time'] < p['lifetime']]
        for particle in self.seed_particles:
            particle['y'] += particle['vy'] * time_passed * 20
            elapsed = current_time - particle['spawn_time']
            if elapsed > 1.0:
                shrink_factor = max(0.3, 1.0 - (elapsed - 1.0))
                particle['size'] = 6 * shrink_factor

        # Fertilizer particles
        self.fertilizer_particles = [p for p in self.fertilizer_particles
                                    if current_time - p['spawn_time'] < p['lifetime']]
        for particle in self.fertilizer_particles:
            particle['x'] += particle['vx'] * time_passed * 10
            particle['y'] += particle['vy'] * time_passed * 10

    def _update_weeds(self, current_time):
        """Update weed growth"""
        if current_time - self.last_weed_check > WEED_CHECK_INTERVAL:
            if random.random() < WEED_SPAWN_CHANCE and self.weed_level == 0:
                self.weed_level = 1
                self.weed_start_time = current_time
            self.last_weed_check = current_time

        if self.weed_level > 0 and self.weed_start_time:
            weed_age = current_time - self.weed_start_time
            if weed_age > WEED_GROWTH_TIME and self.weed_level < MAX_WEED_LEVEL:
                self.weed_level = min(MAX_WEED_LEVEL, self.weed_level + 1)
                self.weed_start_time = current_time

    def harvest(self):
        """Harvest the vegetable"""
        if self.grown:
            self.grown = False
            self.harvest_count += 1
            self.soil_fertility = max(MIN_FERTILITY, self.soil_fertility - FERTILITY_LOSS_PER_HARVEST)

            base_time = random.uniform(MIN_REGROW_TIME, MAX_REGROW_TIME)
            fertility_modifier = 1 + (1 - self.soil_fertility) * 2
            moisture_modifier = 1 + (1 - self.soil_moisture) * 1.5
            weed_modifier = 1.0 + (self.weed_level * 0.5)
            self.regrow_time = time.time() + base_time * fertility_modifier * moisture_modifier * weed_modifier

            return self.credits[self.type]
        return 0

    def fertilize(self):
        """Apply fertilizer to the plot"""
        self.soil_fertility = 1.0

        # Add fertilizer animation
        for i in range(FERTILIZER_PARTICLE_COUNT):
            particle = {
                'x': self.x + 30 + random.uniform(-25, 25),
                'y': self.y + 20 + random.uniform(-15, 15),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-2, 2),
                'size': random.uniform(5, 10),
                'color': (0, 255, 0),
                'spawn_time': time.time(),
                'lifetime': random.uniform(FERTILIZER_PARTICLE_LIFETIME_MIN, FERTILIZER_PARTICLE_LIFETIME_MAX)
            }
            self.fertilizer_particles.append(particle)

        return True

    def water(self):
        """Water the plot"""
        self.soil_moisture = min(1.0, self.soil_moisture + WATER_INCREASE_AMOUNT)

        # Add water animation
        for i in range(WATER_PARTICLE_COUNT):
            particle = {
                'x': self.x + 15 + random.randint(-15, 15),
                'y': self.y - 10,
                'velocity': random.randint(20, 40),
                'spawn_time': time.time()
            }
            self.water_particles.append(particle)

        return self.soil_moisture >= 1.0

    def remove_weeds(self):
        """Remove weeds from the plot"""
        if self.weed_level > 0:
            clicks_needed = self.weed_level

            # Add weed removal animation
            weed_colors = [(0, 100, 0), (0, 120, 0), (0, 80, 0)]
            for i in range(WEED_PARTICLE_COUNT):
                particle = {
                    'x': self.x + 5 + (i * 8) % 50 + random.randint(-2, 2),
                    'y': self.y + 5 + (i // 2) * 15 + random.randint(-3, 3),
                    'vx': random.uniform(-3, 3),
                    'vy': random.uniform(-7, -2),
                    'gravity': random.uniform(0.1, 0.3),
                    'rotation': random.uniform(0, 360),
                    'size': random.randint(4, 8),
                    'color': weed_colors[i % len(weed_colors)],
                    'spawn_time': time.time()
                }
                self.weed_particles.append(particle)

            self.weed_level = max(0, self.weed_level - 1)
            if self.weed_level == 0:
                self.weed_start_time = None
            return clicks_needed
        return 0

    def revive_plant(self):
        """Revive a dead plant"""
        if self.plant_dead and self.soil_fertility > REVIVAL_MIN_FERTILITY and self.soil_moisture > REVIVAL_MIN_MOISTURE:
            self.plant_dead = False
            self.grown = False
            self.regrow_time = time.time() + random.uniform(5, 10)
            return True
        return False

    def plant_seed(self, seed_type):
        """Plant a new seed"""
        if self.plant_dead:
            self.type = seed_type
            self.plant_dead = False
            self.grown = False
            self.soil_fertility = SEED_PLANT_FERTILITY
            self.soil_moisture = SEED_PLANT_MOISTURE
            self.regrow_time = time.time() + random.uniform(MIN_REGROW_TIME, MAX_REGROW_TIME)

            # Add seed planting animation
            seed_colors = {
                'tomato': RED,
                'carrot': ORANGE,
                'eggplant': PURPLE
            }

            particle = {
                'x': self.x + 30,
                'y': self.y + 15,
                'vy': 1.0,
                'size': 6,
                'color': seed_colors[seed_type],
                'spawn_time': time.time(),
                'lifetime': SEED_PARTICLE_LIFETIME
            }
            self.seed_particles.append(particle)

            return True
        return False
