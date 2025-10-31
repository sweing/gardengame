"""
Main garden game logic
"""
import pygame
import time
import random
from vegetable import Vegetable
from inventory import Inventory
from shop import Shop
from weather import WeatherSystem
from effects import VisualEffects, SprinklerSystem
from sound_manager import SoundManager
from snail import Snail
from weed_picker import WeedPicker
from duck import Duck
from config import (
    INITIAL_CREDITS, GARDEN_ROWS, GARDEN_COLS,
    GARDEN_START_X, GARDEN_START_Y, GARDEN_SPACING_X, GARDEN_SPACING_Y,
    INITIAL_PLOT_FERTILITY, INITIAL_PLOT_MOISTURE,
    BACKGROUND_COLORS, WEATHER_COLORS, BLACK,
    MUTE_BUTTON_X, MUTE_BUTTON_Y, MUTE_BUTTON_WIDTH, MUTE_BUTTON_HEIGHT,
    GREEN as CONFIG_GREEN, RED as CONFIG_RED, YELLOW, WHITE
)


class Garden:
    """Main garden game manager"""

    def __init__(self):
        self.vegetables = []
        self.credits = INITIAL_CREDITS
        self.selected_vegetable = None

        # Initialize subsystems
        self.inventory = Inventory()
        self.shop = Shop()
        self.weather = WeatherSystem()
        self.effects = VisualEffects()
        self.sprinkler = SprinklerSystem()
        self.sound = SoundManager()

        # Start background music
        self.sound.play_music()

        # Snail system
        self.snails = []
        self.last_snail_spawn = time.time()
        self.snail_spawn_interval = 15.0  # Spawn snail every 15 seconds

        # Weed picker system
        self.weed_pickers = []

        # Duck system
        self.ducks = []

        # Initialize garden plots
        self._initialize_plots()

    def _initialize_plots(self):
        """Create initial garden plots (all dead)"""
        for row in range(GARDEN_ROWS):
            for col in range(GARDEN_COLS):
                x = GARDEN_START_X + col * GARDEN_SPACING_X
                y = GARDEN_START_Y + row * GARDEN_SPACING_Y
                veg = Vegetable(x, y, 'tomato')
                veg.plant_dead = True
                veg.grown = False
                veg.soil_fertility = INITIAL_PLOT_FERTILITY
                veg.soil_moisture = INITIAL_PLOT_MOISTURE
                self.vegetables.append(veg)

    def update(self):
        """Update all game systems"""
        # Update weather
        self.weather.update()
        current_weather = self.weather.get_weather()

        # Play ambient sounds based on weather
        if current_weather == 'rainy':
            self.sound.play_ambient('rain')
        elif current_weather == 'sunny':
            self.sound.play_ambient('birds')
        else:
            self.sound.stop_ambient()

        # Update vegetables
        for vegetable in self.vegetables:
            vegetable.update(current_weather)

        # Update sprinkler system
        if self.inventory.has_sprinkler():
            if not self.sprinkler.active:
                self.sprinkler.activate()
            self.sprinkler.update(self.vegetables)

        # Update visual effects
        self.effects.update()

        # Update snails
        self._update_snails()

        # Update weed pickers
        self._update_weed_pickers()

        # Update ducks
        self._update_ducks()

    def update_hover(self, mouse_pos):
        """Update hover state"""
        self.effects.update_hover(mouse_pos, self.vegetables)

    def handle_click(self, mouse_pos, right_click=False):
        """Handle mouse clicks"""
        # Check mute button
        mute_rect = pygame.Rect(MUTE_BUTTON_X, MUTE_BUTTON_Y, MUTE_BUTTON_WIDTH, MUTE_BUTTON_HEIGHT)
        if mute_rect.collidepoint(mouse_pos) and not right_click:
            self.sound.toggle_mute()
            return "Sound " + ("ausgeschaltet" if self.sound.muted else "eingeschaltet")

        # Check music button
        from config import MUSIC_BUTTON_X, MUSIC_BUTTON_Y, MUSIC_BUTTON_WIDTH, MUSIC_BUTTON_HEIGHT
        music_rect = pygame.Rect(MUSIC_BUTTON_X, MUSIC_BUTTON_Y, MUSIC_BUTTON_WIDTH, MUSIC_BUTTON_HEIGHT)
        if music_rect.collidepoint(mouse_pos) and not right_click:
            self.sound.toggle_music()
            return "Musik " + ("ausgeschaltet" if not self.sound.music_playing else "eingeschaltet")

        # Check inventory buttons
        inventory_msg = self.inventory.handle_click(mouse_pos)
        if inventory_msg and not right_click:
            return inventory_msg

        # Check shop button
        from config import SHOP_BUTTON_X, SHOP_BUTTON_Y, SHOP_BUTTON_WIDTH, SHOP_BUTTON_HEIGHT
        shop_rect = pygame.Rect(SHOP_BUTTON_X, SHOP_BUTTON_Y, SHOP_BUTTON_WIDTH, SHOP_BUTTON_HEIGHT)
        if shop_rect.collidepoint(mouse_pos) and not right_click:
            self.shop.toggle()
            return "Shop geöffnet!" if self.shop.show else "Shop geschlossen!"

        # Handle shop purchases
        if self.shop.show and not right_click:
            message, new_credits = self.shop.handle_click(mouse_pos, self.inventory, self.credits)
            if message:
                if "gekauft" in message:
                    self.sound.play('buy')
                    if "Sprinkleranlage" in message:
                        self.sprinkler.activate()
                    elif "Weed Picker" in message or "Unkrautpflücker" in message:
                        # Spawn a weed picker
                        self.weed_pickers.append(WeedPicker(self.vegetables))
                    elif "Duck" in message or "Ente" in message:
                        # Spawn a duck
                        self.ducks.append(Duck(self.snails))
                else:
                    self.sound.play('error')
                self.credits = new_credits
                return message

        # Check snail clicks first
        for snail in self.snails[:]:
            if snail.is_clicked(mouse_pos) and not right_click:
                self.snails.remove(snail)
                self.sound.play('weed')
                return "Schnecke entfernt!"

        # Handle vegetable interactions
        for vegetable in self.vegetables:
            if vegetable.rect.collidepoint(mouse_pos):
                if right_click:
                    self.selected_vegetable = vegetable
                    return f"Feld ausgewählt (Fruchtbarkeit: {vegetable.soil_fertility:.1f})"
                else:
                    return self._handle_vegetable_click(vegetable)

        return ""

    def _handle_vegetable_click(self, vegetable):
        """Handle clicking on a vegetable plot"""
        active_tool = self.inventory.get_active_tool()

        if active_tool:
            return self._apply_tool(vegetable, active_tool)
        else:
            return self._default_action(vegetable)

    def _apply_tool(self, vegetable, tool):
        """Apply a tool to a vegetable plot"""
        if tool == 'fertilizer':
            if self.inventory.get_item_count('fertilizer') > 0:
                self.inventory.remove_item('fertilizer')
                vegetable.fertilize()
                self.sound.play('fertilize')
                self.effects.add_sparkles(vegetable.x, vegetable.y, CONFIG_GREEN)
                self.inventory.clear_active_tool()
                return f"Gedüngt! ({self.inventory.get_item_count('fertilizer')} übrig)"
            else:
                self.inventory.clear_active_tool()
                return self._default_action(vegetable)

        elif tool == 'water':
            if self.inventory.get_item_count('water') > 0:
                self.inventory.remove_item('water')
                vegetable.water()
                self.sound.play('water')
                from config import WATER_BLUE
                self.effects.add_sparkles(vegetable.x, vegetable.y, WATER_BLUE)
                self.inventory.clear_active_tool()
                return f"Gegossen! ({self.inventory.get_item_count('water')} übrig)"
            else:
                self.inventory.clear_active_tool()
                return self._default_action(vegetable)

        elif tool == 'weed_killer':
            if self.inventory.get_item_count('weed_killer') > 0 and vegetable.weed_level > 0:
                self.inventory.remove_item('weed_killer')
                vegetable.weed_level = 0
                vegetable.weed_start_time = None
                self.sound.play('weed')
                self.inventory.clear_active_tool()
                return f"Unkraut entfernt! ({self.inventory.get_item_count('weed_killer')} übrig)"
            else:
                self.inventory.clear_active_tool()
                return self._default_action(vegetable)

        elif tool in ['tomato_seeds', 'carrot_seeds', 'eggplant_seeds']:
            if vegetable.weed_level > 0:
                self.inventory.clear_active_tool()
                return self._default_action(vegetable)
            elif self.inventory.get_item_count(tool) > 0 and vegetable.plant_dead:
                self.inventory.remove_item(tool)
                seed_type = tool.replace('_seeds', '')
                vegetable.plant_seed(seed_type)
                self.sound.play('plant')
                self.inventory.clear_active_tool()
                remaining = self.inventory.get_item_count(tool)
                return f"{seed_type.title()}-Samen gepflanzt! ({remaining} übrig)"
            else:
                self.inventory.clear_active_tool()
                return self._default_action(vegetable)

        return ""

    def _update_snails(self):
        """Update snail spawning and movement"""
        current_time = time.time()
        delta_time = 1.0 / 60.0  # Approximate delta time
        current_weather = self.weather.get_weather()

        # Adjust spawn interval based on weather
        if current_weather == 'rainy':
            spawn_interval = 5.0  # Much faster spawning in rain (every 5 seconds)
        else:
            spawn_interval = self.snail_spawn_interval  # Normal 15 seconds

        # Spawn new snails
        if current_time - self.last_snail_spawn > spawn_interval:
            # Find all living vegetables (both ripe and unripe)
            living_vegetables = [v for v in self.vegetables if not v.plant_dead]
            if living_vegetables:
                # In rain, spawn multiple snails at once
                snail_count = random.randint(2, 4) if current_weather == 'rainy' else 1
                for _ in range(snail_count):
                    if living_vegetables:  # Check again in case we run out
                        target = random.choice(living_vegetables)
                        self.snails.append(Snail(target))
                self.last_snail_spawn = current_time

        # Update existing snails
        for snail in self.snails[:]:
            finished = snail.update(delta_time)
            if finished:
                # Snail finished eating - kill the plant (both ripe and unripe)
                snail.target.grown = False
                snail.target.plant_dead = True
                self.snails.remove(snail)

    def _update_weed_pickers(self):
        """Update weed picker movement and working"""
        delta_time = 1.0 / 60.0  # Approximate delta time

        for picker in self.weed_pickers[:]:
            finished = picker.update(delta_time)
            if finished:
                # Picker's time is up
                self.weed_pickers.remove(picker)

    def _update_ducks(self):
        """Update duck movement and snail eating"""
        delta_time = 1.0 / 60.0  # Approximate delta time

        for duck in self.ducks[:]:
            finished = duck.update(delta_time)
            if finished:
                # Duck's time is up
                self.ducks.remove(duck)

    def _default_action(self, vegetable):
        """Perform default action on vegetable plot (no tool selected)"""
        # Priority 1: Remove weeds
        if vegetable.weed_level > 0:
            vegetable.remove_weeds()
            self.sound.play('weed')
            if vegetable.weed_level > 0:
                return f"Unkraut reduziert! Level {vegetable.weed_level} ({vegetable.weed_level} Klicks nötig)"
            else:
                return "Unkraut komplett entfernt!"
        # Priority 3: Dead plants
        elif vegetable.plant_dead:
            self.sound.play('error')
            return "Totes Feld - kaufe Samen im Shop zum Pflanzen!"
        # Priority 4: Harvest
        else:
            earned = vegetable.harvest()
            if earned > 0:
                self.sound.play('harvest')
                self.effects.add_sparkles(vegetable.x, vegetable.y, YELLOW)
                self.effects.add_coin_popup(vegetable.x, vegetable.y, earned)
            self.credits += earned
            return f"Geerntet: {earned} Credits"

    def draw(self, screen, font, title_font):
        """Draw the entire game"""
        # Draw background
        current_weather = self.weather.get_weather()
        screen.fill(BACKGROUND_COLORS[current_weather])

        # Draw title
        title = title_font.render("Garten-Spiel", True, BLACK)
        from config import WINDOW_WIDTH
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 20))

        # Draw credits
        credits_text = font.render(f"Credits: {self.credits}", True, BLACK)
        screen.blit(credits_text, (20, 20))

        # Draw weather
        weather_color = WEATHER_COLORS[current_weather]
        weather_text = font.render(f"Wetter: {current_weather.title()}", True, weather_color)
        screen.blit(weather_text, (20, 50))

        # Draw inventory
        self.inventory.draw(screen, font)

        # Draw shop button
        self.shop.draw_button(screen, font)

        # Draw mute button
        self._draw_mute_button(screen, font)

        # Draw music button
        self._draw_music_button(screen, font)

        # Draw selected vegetable highlight
        if self.selected_vegetable:
            selection_rect = pygame.Rect(self.selected_vegetable.x - 2,
                                        self.selected_vegetable.y - 2, 64, 64)
            pygame.draw.rect(screen, YELLOW, selection_rect, 3)

        # Draw info text
        from config import WINDOW_HEIGHT
        info_text1 = font.render("Links: Ernten/Unkraut entfernen | Rechts: Feld wählen", True, BLACK)
        screen.blit(info_text1, (20, WINDOW_HEIGHT - 60))

        info_text2 = font.render("Tool wählen → Feld klicken | Rechts=Feld auswählen | Gelb=Aktives Tool", True, BLACK)
        screen.blit(info_text2, (20, WINDOW_HEIGHT - 40))

        # Draw vegetables
        for vegetable in self.vegetables:
            vegetable.draw(screen, font)
            self.effects.draw_hover_effect(screen, font)
            self.effects.draw_growth_progress(screen, vegetable)

        # Draw snails
        for snail in self.snails:
            snail.draw(screen)

        # Draw weed pickers
        for picker in self.weed_pickers:
            picker.draw(screen)

        # Draw ducks
        for duck in self.ducks:
            duck.draw(screen)

        # Draw sprinkler system
        self.sprinkler.draw(screen, self.vegetables)

        # Draw weather effects
        if current_weather == 'sunny':
            self.effects.draw_sun(screen)
        elif current_weather == 'cloudy':
            self.effects.draw_clouds(screen)

        self.weather.draw_rain(screen)

        # Draw particle effects
        self.effects.draw_sparkles(screen)
        self.effects.draw_coin_popups(screen, font)

        # Draw shop
        self.shop.draw(screen, font, self.inventory, self.credits)

    def _draw_mute_button(self, screen, font):
        """Draw the mute button"""
        mute_button = pygame.Rect(MUTE_BUTTON_X, MUTE_BUTTON_Y, MUTE_BUTTON_WIDTH, MUTE_BUTTON_HEIGHT)
        mute_color = CONFIG_RED if self.sound.muted else CONFIG_GREEN
        pygame.draw.rect(screen, mute_color, mute_button)
        pygame.draw.rect(screen, BLACK, mute_button, 2)
        mute_text = font.render("🔇 Muted" if self.sound.muted else "🔊 Sound ON", True, BLACK)
        screen.blit(mute_text, (MUTE_BUTTON_X + 30, MUTE_BUTTON_Y + 8))

    def _draw_music_button(self, screen, font):
        """Draw the music toggle button"""
        from config import MUSIC_BUTTON_X, MUSIC_BUTTON_Y, MUSIC_BUTTON_WIDTH, MUSIC_BUTTON_HEIGHT
        music_button = pygame.Rect(MUSIC_BUTTON_X, MUSIC_BUTTON_Y, MUSIC_BUTTON_WIDTH, MUSIC_BUTTON_HEIGHT)
        music_color = CONFIG_RED if not self.sound.music_playing else CONFIG_GREEN
        pygame.draw.rect(screen, music_color, music_button)
        pygame.draw.rect(screen, BLACK, music_button, 2)
        music_text = font.render("🎵 Musik AUS" if not self.sound.music_playing else "🎵 Musik AN", True, BLACK)
        screen.blit(music_text, (MUSIC_BUTTON_X + 30, MUSIC_BUTTON_Y + 8))
