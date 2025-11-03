"""
Inventory management system
"""
import pygame
from config import (
    INVENTORY_BUTTONS, INVENTORY_BUTTON_WIDTH, INVENTORY_BUTTON_HEIGHT,
    GREEN, RED, YELLOW, BLACK, WHITE, WATER_BLUE, GRAY, ORANGE, PURPLE
)


class Inventory:
    """Manages player inventory and tool selection"""

    def __init__(self):
        self.items = {
            'tomato_seeds': 0,
            'carrot_seeds': 0,
            'eggplant_seeds': 0,
            'sprinkler_system': False,
            'rain_barrel': False,
            'weed_killer': 0,
            'fertilizer': 0,
            'water': 0
        }
        self.active_tool = None
        self.button_rects = {}

    def add_item(self, item, amount):
        """Add items to inventory"""
        if item in self.items and isinstance(self.items[item], int):
            self.items[item] += amount

    def remove_item(self, item, amount=1):
        """Remove items from inventory"""
        if item in self.items and isinstance(self.items[item], int):
            self.items[item] = max(0, self.items[item] - amount)
            return True
        return False

    def get_item_count(self, item):
        """Get count of an item"""
        if item in self.items:
            if isinstance(self.items[item], bool):
                return 1 if self.items[item] else 0
            return self.items[item]
        return 0

    def has_sprinkler(self):
        """Check if sprinkler system is owned"""
        return self.items['sprinkler_system']

    def set_sprinkler(self, value):
        """Set sprinkler system status"""
        self.items['sprinkler_system'] = value

    def has_rain_barrel(self):
        """Check if rain barrel is owned"""
        return self.items['rain_barrel']

    def set_rain_barrel(self, value):
        """Set rain barrel status"""
        self.items['rain_barrel'] = value

    def get_active_tool(self):
        """Get currently active tool"""
        return self.active_tool

    def set_active_tool(self, tool):
        """Set active tool"""
        self.active_tool = tool

    def clear_active_tool(self):
        """Clear active tool selection"""
        self.active_tool = None

    def handle_click(self, mouse_pos):
        """Handle inventory button clicks"""
        for tool, rect in self.button_rects.items():
            if rect.collidepoint(mouse_pos):
                if self.items[tool] > 0 or (tool == 'sprinkler_system' and self.items[tool]):
                    self.active_tool = tool
                    return f"{tool.replace('_', ' ').title()} ausgewählt - Feld anklicken"
                else:
                    return f"Kein {tool.replace('_', ' ')} vorhanden!"
        return None

    def _draw_icon(self, screen, tool_type, x, y):
        """Draw icon for a tool"""
        if tool_type == 'fertilizer':
            pygame.draw.rect(screen, (0, 150, 0), (x+5, y+10, 15, 15))
            font = pygame.font.Font(None, 16)
            text = font.render("D", True, WHITE)
            screen.blit(text, (x+10, y+12))
        elif tool_type == 'water':
            pygame.draw.circle(screen, WATER_BLUE, (x+12, y+15), 8)
        elif tool_type == 'weed_killer':
            pygame.draw.rect(screen, GRAY, (x+5, y+10, 15, 15))
            pygame.draw.line(screen, RED, (x+7, y+12), (x+17, y+22), 2)
            pygame.draw.line(screen, RED, (x+17, y+12), (x+7, y+22), 2)
        elif tool_type == 'tomato_seeds':
            pygame.draw.circle(screen, RED, (x+12, y+15), 8)
            pygame.draw.circle(screen, (139, 69, 19), (x+12, y+8), 2)
        elif tool_type == 'carrot_seeds':
            pygame.draw.polygon(screen, ORANGE, [(x+12, y+8), (x+8, y+20), (x+16, y+20)])
            pygame.draw.lines(screen, GREEN, False, [(x+9, y+6), (x+12, y+8), (x+15, y+6)], 2)
        elif tool_type == 'eggplant_seeds':
            pygame.draw.ellipse(screen, PURPLE, (x+7, y+10, 10, 15))
            pygame.draw.circle(screen, GREEN, (x+12, y+10), 2)

    def draw(self, screen, font):
        """Draw inventory buttons"""
        self.button_rects = {}

        for tool, x, y in INVENTORY_BUTTONS:
            # Determine button color
            if self.items[tool] > 0 or (tool == 'sprinkler_system' and self.items[tool]):
                color = GREEN
            else:
                color = RED

            if self.active_tool == tool:
                color = YELLOW

            rect = pygame.Rect(x, y, INVENTORY_BUTTON_WIDTH, INVENTORY_BUTTON_HEIGHT)
            self.button_rects[tool] = rect

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)

            self._draw_icon(screen, tool, x, y)

            # Draw count
            count = self.items[tool]
            if isinstance(count, bool):
                count = 1 if count else 0
            count_text = font.render(str(count), True, BLACK)
            screen.blit(count_text, (x + 65, y + 25))
