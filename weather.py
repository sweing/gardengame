"""
Weather system for the garden game
"""
import random
import time
from config import (
    WEATHER_OPTIONS, MIN_WEATHER_DURATION, MAX_WEATHER_DURATION,
    WINDOW_WIDTH, WINDOW_HEIGHT, WATER_BLUE, MAX_RAIN_PARTICLES, RAIN_SPAWN_RATE
)


class WeatherSystem:
    """Manages weather changes and rain particles"""

    def __init__(self):
        self.weather = 'sunny'
        self.last_weather_change = time.time()
        self.weather_duration = random.uniform(MIN_WEATHER_DURATION, MAX_WEATHER_DURATION)
        self.rain_particles = []

    def update(self):
        """Update weather state and particles"""
        current_time = time.time()

        # Check if weather should change
        if current_time - self.last_weather_change > self.weather_duration:
            self.weather = random.choice(WEATHER_OPTIONS)
            self.last_weather_change = current_time
            self.weather_duration = random.uniform(MIN_WEATHER_DURATION, MAX_WEATHER_DURATION)

        # Update rain particles
        if self.weather == 'rainy':
            self._update_rain_particles()
        else:
            self.rain_particles = []

    def _update_rain_particles(self):
        """Create and update rain particle effects"""
        # Spawn new rain particles
        if len(self.rain_particles) < MAX_RAIN_PARTICLES:
            for i in range(RAIN_SPAWN_RATE):
                particle = {
                    'x': random.randint(0, WINDOW_WIDTH),
                    'y': random.randint(-20, 0),
                    'speed': random.uniform(3, 7)
                }
                self.rain_particles.append(particle)

        # Update existing rain particles
        for particle in self.rain_particles[:]:
            particle['y'] += particle['speed']
            particle['x'] += random.uniform(-0.5, 0.5)
            if particle['y'] > WINDOW_HEIGHT:
                self.rain_particles.remove(particle)

    def draw_rain(self, screen):
        """Draw rain particles with splash effects"""
        import pygame
        for particle in self.rain_particles:
            # Main rain drop
            pygame.draw.line(screen, WATER_BLUE,
                           (particle['x'], particle['y']),
                           (particle['x'] - 2, particle['y'] + 10), 2)
            # Lighter drops for depth
            if random.random() > 0.7:
                pygame.draw.line(screen, (100, 200, 255),
                               (particle['x'] + 1, particle['y']),
                               (particle['x'] - 1, particle['y'] + 8), 1)

    def get_weather(self):
        """Get current weather"""
        return self.weather

    def get_forecast(self, periods=3):
        """Get weather forecast for next periods

        Returns list of weather predictions:
        [current, next, after_next]
        """
        forecast = [self.weather]  # Current weather

        # Calculate remaining time for current weather
        current_time = time.time()
        time_elapsed = current_time - self.last_weather_change
        time_remaining = self.weather_duration - time_elapsed

        # Seed random with current weather state for consistent predictions
        seed = int((self.last_weather_change + self.weather_duration) * 1000)

        # Predict next weather periods
        for i in range(1, periods):
            # Use seeded random for consistent forecast
            random.seed(seed + i)
            next_weather = random.choice(WEATHER_OPTIONS)
            forecast.append(next_weather)

        # Reset random seed
        random.seed()

        return forecast
