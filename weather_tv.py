"""
Weather TV - Displays 3-day weather forecast
"""
import pygame
import time
import math
from config import WEATHER_TV_X, WEATHER_TV_Y, WEATHER_TV_WIDTH, WEATHER_TV_HEIGHT, YELLOW, WATER_BLUE, GRAY, BLACK, WHITE


class WeatherTV:
    """A TV that displays weather forecast"""

    def __init__(self, x=WEATHER_TV_X, y=WEATHER_TV_Y):
        self.x = x
        self.y = y
        self.width = WEATHER_TV_WIDTH
        self.height = WEATHER_TV_HEIGHT

        # Screen flicker animation
        self.flicker_time = 0

    def update(self):
        """Update TV animations"""
        self.flicker_time += 0.1

    def draw(self, screen, font, forecast):
        """Draw the TV with weather forecast

        Args:
            forecast: List of 3 weather strings ['sunny', 'rainy', 'cloudy']
        """
        x, y = self.x, self.y

        # Draw TV body (dark gray box)
        tv_body = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(screen, (40, 40, 40), tv_body)
        pygame.draw.rect(screen, (20, 20, 20), tv_body, 3)

        # Draw screen (lighter inset)
        screen_rect = pygame.Rect(x + 8, y + 8, self.width - 16, self.height - 30)
        # Screen glow effect
        glow_brightness = int(200 + 20 * math.sin(self.flicker_time))
        pygame.draw.rect(screen, (glow_brightness, glow_brightness, glow_brightness), screen_rect)
        pygame.draw.rect(screen, (100, 100, 100), screen_rect, 2)

        # Draw antenna (centered on top)
        antenna_x = x + self.width // 2
        antenna_y = y
        pygame.draw.line(screen, (150, 150, 150), (antenna_x, antenna_y), (antenna_x - 8, antenna_y - 12), 2)
        pygame.draw.line(screen, (150, 150, 150), (antenna_x, antenna_y), (antenna_x + 8, antenna_y - 12), 2)
        pygame.draw.circle(screen, (255, 0, 0), (antenna_x - 8, antenna_y - 12), 2)
        pygame.draw.circle(screen, (255, 0, 0), (antenna_x + 8, antenna_y - 12), 2)

        # Draw power button (centered at bottom)
        button_x = x + self.width // 2
        button_y = y + self.height - 8
        pygame.draw.circle(screen, (0, 255, 0), (button_x, button_y), 3)
        pygame.draw.circle(screen, (0, 180, 0), (button_x, button_y), 3, 1)

        # Draw forecast on screen (horizontal layout, compact)
        if forecast and len(forecast) >= 3:
            forecast_x_start = x + 10
            forecast_y = y + 15
            icon_size = 18
            spacing = 35

            labels = ["JTZ", "BLD", "SPT"]

            for i, (weather, label) in enumerate(zip(forecast[:3], labels)):
                icon_x = forecast_x_start + (i * spacing)

                # Draw weather icon
                self._draw_weather_icon(screen, icon_x, forecast_y, icon_size, weather)

                # Draw label below icon (smaller font)
                label_font = pygame.font.Font(None, 11)
                label_text = label_font.render(label, True, BLACK)
                label_rect = label_text.get_rect(center=(icon_x + icon_size // 2, forecast_y + icon_size + 8))
                screen.blit(label_text, label_rect)

    def _draw_weather_icon(self, screen, x, y, size, weather):
        """Draw weather icon on TV screen"""
        center_x = x + size // 2
        center_y = y + size // 2

        if weather == 'sunny':
            # Sun
            pygame.draw.circle(screen, YELLOW, (center_x, center_y), size // 3)
            # Sun rays
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                start_x = center_x + math.cos(rad) * (size // 3 + 2)
                start_y = center_y + math.sin(rad) * (size // 3 + 2)
                end_x = center_x + math.cos(rad) * (size // 2 + 2)
                end_y = center_y + math.sin(rad) * (size // 2 + 2)
                pygame.draw.line(screen, YELLOW, (start_x, start_y), (end_x, end_y), 2)

        elif weather == 'rainy':
            # Cloud
            pygame.draw.circle(screen, GRAY, (center_x - 5, center_y - 3), size // 4)
            pygame.draw.circle(screen, GRAY, (center_x + 5, center_y - 3), size // 4)
            pygame.draw.circle(screen, GRAY, (center_x, center_y), size // 3)
            # Rain drops
            for i in range(3):
                drop_x = center_x - 8 + (i * 8)
                drop_y = center_y + 8
                pygame.draw.line(screen, WATER_BLUE, (drop_x, drop_y), (drop_x, drop_y + 5), 2)

        elif weather == 'cloudy':
            # Cloud
            pygame.draw.circle(screen, GRAY, (center_x - 5, center_y - 2), size // 4)
            pygame.draw.circle(screen, GRAY, (center_x + 5, center_y - 2), size // 4)
            pygame.draw.circle(screen, GRAY, (center_x, center_y + 2), size // 3)
