"""
Shop system for buying seeds and upgrades
"""
import pygame
from config import (
    SHOP_X, SHOP_Y, SHOP_WIDTH, SHOP_HEIGHT,
    SHOP_ITEM_START_Y, SHOP_ITEM_SPACING, SHOP_ITEM_HEIGHT,
    SHOP_ITEMS, SHOP_PRICES,
    WHITE, BLACK, GREEN, RED, GRAY
)


class Shop:
    """Manages the shop UI and purchases"""

    def __init__(self):
        self.show = False

    def toggle(self):
        """Toggle shop visibility"""
        self.show = not self.show
        return self.show

    def handle_click(self, mouse_pos, inventory, credits):
        """Handle shop item purchases and close button"""
        if not self.show:
            return None, credits

        # Check close button (X)
        close_button_size = 30
        close_button_x = SHOP_X + SHOP_WIDTH - close_button_size - 5
        close_button_y = SHOP_Y + 5
        close_button_rect = pygame.Rect(close_button_x, close_button_y, close_button_size, close_button_size)

        if close_button_rect.collidepoint(mouse_pos):
            self.show = False
            return "Shop geschlossen!", credits

        # Check shop items
        for display_name, item_key, price in SHOP_ITEMS:
            y_pos = SHOP_ITEM_START_Y + SHOP_ITEMS.index((display_name, item_key, price)) * SHOP_ITEM_SPACING
            button_rect = pygame.Rect(SHOP_X + 10, y_pos, SHOP_WIDTH - 20, SHOP_ITEM_HEIGHT)

            if button_rect.collidepoint(mouse_pos):
                return self._buy_item(item_key, price, inventory, credits)

        return None, credits

    def _buy_item(self, item, price, inventory, credits):
        """Process item purchase"""
        # Check if sprinkler system already owned
        if item == 'sprinkler_system' and inventory.has_sprinkler():
            return "Sprinkleranlage bereits gekauft!", credits

        # Check if rain barrel already owned
        if item == 'rain_barrel' and inventory.has_rain_barrel():
            return "Regentonne bereits gekauft!", credits

        # Check if weather TV already owned
        if item == 'weather_tv' and inventory.has_weather_tv():
            return "Wetter-TV bereits gekauft!", credits

        # Check if enough credits
        if credits >= price:
            credits -= price
            if item == 'sprinkler_system':
                inventory.set_sprinkler(True)
            elif item == 'rain_barrel':
                inventory.set_rain_barrel(True)
            elif item == 'weather_tv':
                inventory.set_weather_tv(True)
            elif item == 'weed_picker' or item == 'duck':
                # Weed picker and duck are used immediately, not stored in inventory
                pass
            else:
                inventory.add_item(item, 1)
            return f"{item.replace('_', ' ').title()} gekauft für {price} Credits!", credits
        else:
            return f"Nicht genug Credits! Brauche {price}", credits

    def draw(self, screen, font, inventory, credits):
        """Draw the shop interface"""
        if not self.show:
            return

        # Draw shop background
        shop_bg = pygame.Rect(SHOP_X, SHOP_Y, SHOP_WIDTH, SHOP_HEIGHT)
        pygame.draw.rect(screen, WHITE, shop_bg)
        pygame.draw.rect(screen, BLACK, shop_bg, 3)

        # Draw close button (X) in top-right corner
        close_button_size = 30
        close_button_x = SHOP_X + SHOP_WIDTH - close_button_size - 5
        close_button_y = SHOP_Y + 5
        close_button_rect = pygame.Rect(close_button_x, close_button_y, close_button_size, close_button_size)
        pygame.draw.rect(screen, RED, close_button_rect)
        pygame.draw.rect(screen, BLACK, close_button_rect, 2)

        # Draw X
        x_font = pygame.font.Font(None, 28)
        x_text = x_font.render("X", True, WHITE)
        screen.blit(x_text, (close_button_x + 8, close_button_y + 4))

        # Draw title
        title_text = font.render("SHOP", True, BLACK)
        screen.blit(title_text, (SHOP_X + SHOP_WIDTH // 2 - title_text.get_width() // 2, SHOP_Y + 10))

        # Draw shop items
        y_offset = SHOP_ITEM_START_Y
        for display_name, item_key, price in SHOP_ITEMS:
            color = GREEN if credits >= price else RED

            # Gray out sprinkler if already owned
            if item_key == 'sprinkler_system' and inventory.has_sprinkler():
                color = GRAY
                display_name += " (Gekauft)"

            # Gray out rain barrel if already owned
            if item_key == 'rain_barrel' and inventory.has_rain_barrel():
                color = GRAY
                display_name += " (Gekauft)"

            # Gray out weather TV if already owned
            if item_key == 'weather_tv' and inventory.has_weather_tv():
                color = GRAY
                display_name += " (Gekauft)"

            button_rect = pygame.Rect(SHOP_X + 10, y_offset, SHOP_WIDTH - 20, SHOP_ITEM_HEIGHT)
            pygame.draw.rect(screen, color, button_rect)
            pygame.draw.rect(screen, BLACK, button_rect, 1)

            item_text = font.render(f"{display_name}: {price} Credits", True, BLACK)
            screen.blit(item_text, (SHOP_X + 15, y_offset + 5))

            # Show inventory count
            if item_key not in ['sprinkler_system', 'rain_barrel', 'weather_tv']:
                count = inventory.get_item_count(item_key)
                if count > 0:
                    count_text = font.render(f"({count})", True, BLACK)
                    screen.blit(count_text, (SHOP_X + SHOP_WIDTH - 60, y_offset + 5))

            y_offset += SHOP_ITEM_SPACING

        # Show sprinkler status
        status_y = SHOP_Y + SHOP_HEIGHT - 50
        if inventory.has_sprinkler():
            sprinkler_text = font.render("Sprinkler aktiv!", True, GREEN)
            screen.blit(sprinkler_text, (SHOP_X + 65, status_y))
            status_y += 20

        # Show rain barrel status
        if inventory.has_rain_barrel():
            barrel_text = font.render("Regentonne aktiv!", True, GREEN)
            screen.blit(barrel_text, (SHOP_X + 65, status_y))
            status_y += 20

        # Show weather TV status
        if inventory.has_weather_tv():
            tv_text = font.render("Wetter-TV aktiv!", True, GREEN)
            screen.blit(tv_text, (SHOP_X + 65, status_y))

    def draw_button(self, screen, font):
        """Draw the shop toggle button"""
        from config import SHOP_BUTTON_X, SHOP_BUTTON_Y, SHOP_BUTTON_WIDTH, SHOP_BUTTON_HEIGHT, YELLOW
        shop_button = pygame.Rect(SHOP_BUTTON_X, SHOP_BUTTON_Y, SHOP_BUTTON_WIDTH, SHOP_BUTTON_HEIGHT)
        pygame.draw.rect(screen, YELLOW, shop_button)
        pygame.draw.rect(screen, BLACK, shop_button, 2)
        shop_text = font.render("Shop", True, BLACK)
        screen.blit(shop_text, (SHOP_BUTTON_X + 65, SHOP_BUTTON_Y + 15))
        return shop_button
