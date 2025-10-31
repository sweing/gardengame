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
        """Handle shop item purchases"""
        if not self.show:
            return None, credits

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

        # Check if enough credits
        if credits >= price:
            credits -= price
            if item == 'sprinkler_system':
                inventory.set_sprinkler(True)
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

            button_rect = pygame.Rect(SHOP_X + 10, y_offset, SHOP_WIDTH - 20, SHOP_ITEM_HEIGHT)
            pygame.draw.rect(screen, color, button_rect)
            pygame.draw.rect(screen, BLACK, button_rect, 1)

            item_text = font.render(f"{display_name}: {price} Credits", True, BLACK)
            screen.blit(item_text, (SHOP_X + 15, y_offset + 5))

            # Show inventory count
            if item_key != 'sprinkler_system':
                count = inventory.get_item_count(item_key)
                if count > 0:
                    count_text = font.render(f"({count})", True, BLACK)
                    screen.blit(count_text, (SHOP_X + SHOP_WIDTH - 60, y_offset + 5))

            y_offset += SHOP_ITEM_SPACING

        # Show sprinkler status
        if inventory.has_sprinkler():
            sprinkler_text = font.render("Sprinkler aktiv!", True, GREEN)
            screen.blit(sprinkler_text, (SHOP_X + 65, SHOP_Y + SHOP_HEIGHT - 30))

    def draw_button(self, screen, font):
        """Draw the shop toggle button"""
        from config import SHOP_BUTTON_X, SHOP_BUTTON_Y, SHOP_BUTTON_WIDTH, SHOP_BUTTON_HEIGHT, YELLOW
        shop_button = pygame.Rect(SHOP_BUTTON_X, SHOP_BUTTON_Y, SHOP_BUTTON_WIDTH, SHOP_BUTTON_HEIGHT)
        pygame.draw.rect(screen, YELLOW, shop_button)
        pygame.draw.rect(screen, BLACK, shop_button, 2)
        shop_text = font.render("Shop", True, BLACK)
        screen.blit(shop_text, (SHOP_BUTTON_X + 65, SHOP_BUTTON_Y + 15))
        return shop_button
