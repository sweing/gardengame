import pygame
import sys
import random
import time
import math
import asyncio

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
BLACK = (0, 0, 0)
WATER_BLUE = (0, 191, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

class SoundManager:
    """Manages all game sounds with graceful fallback if files are missing"""
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music_playing = False
        self.muted = False
        self.volume = 0.7
        self.current_ambient = None  # Track current ambient sound

        # List of sound files to load
        sound_files = {
            'harvest': 'sounds/harvest.ogg',
            'water': 'sounds/water.ogg',
            'weed': 'sounds/weed.ogg',
            'fertilize': 'sounds/fertilize.ogg',
            'buy': 'sounds/buy.ogg',
            'plant': 'sounds/plant.ogg',
            'error': 'sounds/error.ogg',
            'rain': 'sounds/rain.ogg',
            'birds': 'sounds/birds.ogg'
        }

        # Try to load each sound
        for name, path in sound_files.items():
            try:
                sound = pygame.mixer.Sound(path)
                sound.set_volume(self.volume)
                self.sounds[name] = sound
                print(f"Loaded sound: {name}")
            except:
                # Sound file not found - that's okay, we'll just skip it
                self.sounds[name] = None
                print(f"Sound not found (optional): {path}")

        # Try to load background music
        try:
            pygame.mixer.music.load('sounds/bgm.ogg')
            pygame.mixer.music.set_volume(self.volume * 0.5)  # Music quieter than SFX
            print("Loaded background music")
        except:
            print("Background music not found (optional)")

    def play(self, sound_name):
        """Play a sound effect"""
        if self.muted:
            return

        if sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].play()

    def play_music(self, loops=-1):
        """Start background music (loops infinitely by default)"""
        if self.muted or self.music_playing:
            return

        try:
            pygame.mixer.music.play(loops)
            self.music_playing = True
        except:
            pass

    def stop_music(self):
        """Stop background music"""
        pygame.mixer.music.stop()
        self.music_playing = False

    def toggle_mute(self):
        """Toggle sound on/off"""
        self.muted = not self.muted
        if self.muted:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        return self.muted

    def set_volume(self, volume):
        """Set volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume * 0.5)
        for sound in self.sounds.values():
            if sound:
                sound.set_volume(self.volume)

    def play_ambient(self, sound_name):
        """Play an ambient sound on loop"""
        if self.muted or sound_name == self.current_ambient:
            return

        # Stop current ambient if different
        if self.current_ambient and self.sounds.get(self.current_ambient):
            self.sounds[self.current_ambient].stop()

        # Start new ambient
        if sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].play(loops=-1)  # Loop infinitely
            self.sounds[sound_name].set_volume(self.volume * 0.3)  # Quieter than SFX
            self.current_ambient = sound_name

    def stop_ambient(self):
        """Stop current ambient sound"""
        if self.current_ambient and self.sounds.get(self.current_ambient):
            self.sounds[self.current_ambient].stop()
            self.current_ambient = None

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
        self.regrow_time = time.time() + random.uniform(3, 8)
        self.rect = pygame.Rect(x, y, 60, 60)
        self.water_particles = []
        self.weed_level = 0
        self.weed_start_time = None
        self.last_weed_check = time.time()
        self.plant_dead = False
        self.weed_particles = []    # Für die Wegflieg-Animation
        self.seed_particles = []    # Für die Samen-Animation
        self.fertilizer_particles = []  # Für die Dünger-Animation
        
        self.colors = {
            'tomato': RED,
            'carrot': ORANGE, 
            'eggplant': PURPLE
        }
        
        self.credits = {
            'tomato': 5,
            'carrot': 3,
            'eggplant': 7
        }
    
    def draw(self, screen, font):
        # Immer die Bodenfarbe zeichnen - kein "TOT" Text mehr
        soil_color = BROWN if self.soil_fertility > 0.5 else (89, 39, 19)
        if self.plant_dead:
            soil_color = (50, 25, 12)  # Dunklere Farbe für tote Felder
        pygame.draw.rect(screen, soil_color, (self.x, self.y, 60, 60))
        
        # 1. Pflanzen zeichnen (erst die Pflanzen)
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
        
        # 2. Unkraut ÜBER den Pflanzen zeichnen
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
        
        # 3. Animationen ÜBER allem zeichnen
        # Samen-Partikel (ein einzelner Samen)
        for particle in self.seed_particles:
            alpha = max(0, 1 - (time.time() - particle['spawn_time']) / particle['lifetime'])
            if alpha > 0:
                size = int(particle['size'] * alpha)
                if size > 0:
                    # Samen als kleinen Kreis mit schwarzem Rand zeichnen
                    pygame.draw.circle(screen, particle['color'], 
                                    (int(particle['x']), int(particle['y'])), size)
                    pygame.draw.circle(screen, BLACK, 
                                    (int(particle['x']), int(particle['y'])), size, 1)
        
        # Dünger-Partikel (größer und besser sichtbar)
        for particle in self.fertilizer_particles:
            alpha = max(0, 1 - (time.time() - particle['spawn_time']) / particle['lifetime'])
            if alpha > 0:
                size = int(particle['size'] * alpha)
                if size > 0:
                    pygame.draw.circle(screen, (0, 255, 0), # Hellgrün für bessere Sichtbarkeit
                                    (int(particle['x']), int(particle['y'])), size)
        
        # Wasser-Partikel
        for particle in self.water_particles:
            alpha = max(0, 1 - (time.time() - particle['spawn_time']) / 1.0)
            if alpha > 0:
                size = int(3 * alpha)
                if size > 0:
                    pygame.draw.circle(screen, WATER_BLUE, 
                                     (int(particle['x']), int(particle['y'])), size)
        
        # Unkraut-Partikel (wegfliegende Animation)
        for particle in self.weed_particles:
            alpha = max(0, 1 - (time.time() - particle['spawn_time']) / 2.0)
            if alpha > 0:
                size = int(particle['size'] * alpha)
                if size > 0:
                    pygame.draw.circle(screen, particle['color'], 
                                     (int(particle['x']), int(particle['y'])), size)
        
        # 4. UI-Elemente zuletzt (immer sichtbar)
        # Fruchtbarkeits- und Feuchtigkeitsbalken
        fertility_bar_width = int(50 * self.soil_fertility)
        pygame.draw.rect(screen, RED, (self.x + 5, self.y + 55, 50, 3))
        pygame.draw.rect(screen, GREEN, (self.x + 5, self.y + 55, fertility_bar_width, 3))
        
        moisture_bar_width = int(50 * self.soil_moisture)
        pygame.draw.rect(screen, (139, 69, 19), (self.x + 5, self.y + 59, 50, 3))
        pygame.draw.rect(screen, WATER_BLUE, (self.x + 5, self.y + 59, moisture_bar_width, 3))
    
    def update(self, weather='sunny'):
        current_time = time.time()
        time_passed = current_time - self.last_moisture_update
        
        base_moisture_loss_rate = 0.005
        if weather == 'sunny':
            moisture_loss_rate = base_moisture_loss_rate * 2.0
        elif weather == 'rainy':
            moisture_loss_rate = base_moisture_loss_rate * 0.2
            self.soil_moisture = min(1.0, self.soil_moisture + 0.01 * time_passed)
        else:
            moisture_loss_rate = base_moisture_loss_rate
            
        self.soil_moisture = max(0.0, self.soil_moisture - moisture_loss_rate * time_passed)
        self.last_moisture_update = current_time
        
        # Wasser-Partikel aktualisieren
        self.water_particles = [p for p in self.water_particles if current_time - p['spawn_time'] < 1.0]
        
        for particle in self.water_particles:
            particle['y'] += particle['velocity'] * time_passed
            particle['velocity'] += 50 * time_passed
            
        # Unkraut-Partikel aktualisieren (wegfliegende Animation)
        self.weed_particles = [p for p in self.weed_particles if current_time - p['spawn_time'] < 2.0]
        
        for particle in self.weed_particles:
            particle['x'] += particle['vx'] * time_passed * 30
            particle['y'] += particle['vy'] * time_passed * 30
            particle['vy'] += particle['gravity'] * time_passed * 30
            particle['rotation'] += time_passed * 180  # Drehung
            
        # Samen-Partikel aktualisieren
        self.seed_particles = [p for p in self.seed_particles if current_time - p['spawn_time'] < p['lifetime']]
        
        for particle in self.seed_particles:
            particle['y'] += particle['vy'] * time_passed * 20  # Samen sinkt langsam in die Erde
            # Samen wird kleiner, je tiefer er sinkt
            elapsed = current_time - particle['spawn_time']
            if elapsed > 1.0:  # Nach 1 Sekunde beginnt er zu schrumpfen
                shrink_factor = max(0.3, 1.0 - (elapsed - 1.0))
                particle['size'] = 6 * shrink_factor
        
        # Dünger-Partikel aktualisieren
        self.fertilizer_particles = [p for p in self.fertilizer_particles if current_time - p['spawn_time'] < p['lifetime']]
        
        for particle in self.fertilizer_particles:
            particle['x'] += particle['vx'] * time_passed * 10
            particle['y'] += particle['vy'] * time_passed * 10
        
        if current_time - self.last_weed_check > 5.0:
            if random.random() < 0.3 and self.weed_level == 0:
                self.weed_level = 1
                self.weed_start_time = current_time
            self.last_weed_check = current_time
        
        if self.weed_level > 0 and self.weed_start_time:
            weed_age = current_time - self.weed_start_time
            if weed_age > 10 and self.weed_level < 10:
                self.weed_level = min(10, self.weed_level + 1)
                self.weed_start_time = current_time
        
        if self.soil_fertility <= 0 or self.soil_moisture <= 0:
            self.plant_dead = True
            self.grown = False
        
        if not self.grown and current_time >= self.regrow_time and not self.plant_dead:
            self.grown = True
    
    def harvest(self):
        if self.grown:
            self.grown = False
            self.harvest_count += 1
            self.soil_fertility = max(0.1, self.soil_fertility - 0.15)
            
            base_time = random.uniform(3, 8)
            fertility_modifier = 1 + (1 - self.soil_fertility) * 2
            moisture_modifier = 1 + (1 - self.soil_moisture) * 1.5
            weed_modifier = 1.0 + (self.weed_level * 0.5)
            self.regrow_time = time.time() + base_time * fertility_modifier * moisture_modifier * weed_modifier
            
            return self.credits[self.type]
        return 0
    
    def fertilize(self):
        self.soil_fertility = 1.0  # Immer vollständig füllen
        
        # Dünger-Animation hinzufügen
        for i in range(15):
            particle = {
                'x': self.x + 30 + random.uniform(-25, 25),
                'y': self.y + 20 + random.uniform(-15, 15),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-2, 2),
                'size': random.uniform(5, 10),  # Größer gemacht
                'color': (0, 255, 0),  # Hellgrün für Dünger
                'spawn_time': time.time(),
                'lifetime': random.uniform(2.0, 3.5)  # Länger sichtbar
            }
            self.fertilizer_particles.append(particle)
            
        return True
    
    def water(self):
        self.soil_moisture = min(1.0, self.soil_moisture + 0.4)
        
        for i in range(15):
            particle = {
                'x': self.x + 15 + random.randint(-15, 15),
                'y': self.y - 10,
                'velocity': random.randint(20, 40),
                'spawn_time': time.time()
            }
            self.water_particles.append(particle)
        
        return self.soil_moisture >= 1.0
    
    def remove_weeds(self):
        if self.weed_level > 0:
            clicks_needed = self.weed_level
            
            # Animation vorbereiten - Unkraut-Partikel erstellen
            weed_colors = [(0, 100, 0), (0, 120, 0), (0, 80, 0)]
            for i in range(5):
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
        if self.plant_dead and self.soil_fertility > 0.3 and self.soil_moisture > 0.3:
            self.plant_dead = False
            self.grown = False
            self.regrow_time = time.time() + random.uniform(5, 10)
            return True
        return False
    
    def plant_seed(self, seed_type):
        if self.plant_dead:
            self.type = seed_type
            self.plant_dead = False
            self.grown = False
            self.soil_fertility = 0.8
            self.soil_moisture = 0.8
            self.regrow_time = time.time() + random.uniform(3, 8)
            
            # Samen-Pflanz-Animation
            seed_colors = {
                'tomato': RED,
                'carrot': ORANGE,
                'eggplant': PURPLE
            }
            
            # Ein einzelner Samen, der in die Erde sinkt
            particle = {
                'x': self.x + 30,
                'y': self.y + 15,
                'vy': 1.0,
                'size': 6,  # Größer für bessere Sichtbarkeit
                'color': seed_colors[seed_type],
                'spawn_time': time.time(),
                'lifetime': 2.0  # 2 Sekunden sichtbar
            }
            self.seed_particles.append(particle)
                
            return True
        return False

class Garden:
    def __init__(self):
        self.vegetables = []
        self.credits = 50
        self.selected_vegetable = None
        self.show_shop = False
        self.active_tool = None
        self.button_rects = {}

        # Visual effects
        self.hovered_vegetable = None
        self.coin_popups = []  # Floating coin notifications
        self.sparkle_particles = []  # Sparkles for harvesting
        self.cloud_offset = 0  # For animated clouds
        self.sun_rotation = 0  # For rotating sun rays

        # Initialize sound system
        self.sound = SoundManager()
        self.sound.play_music()  # Start background music
        
        self.inventory = {
            'tomato_seeds': 0,
            'carrot_seeds': 0,
            'eggplant_seeds': 0,
            'sprinkler_system': False,
            'weed_killer': 0,
            'fertilizer': 0,
            'water': 0
        }
        
        self.shop_prices = {
            'tomato_seeds': 15,
            'carrot_seeds': 10,
            'eggplant_seeds': 20,
            'sprinkler_system': 100,
            'weed_killer': 25,
            'fertilizer': 10,
            'water': 1
        }
        
        self.last_sprinkler_time = time.time()
        self.sprinkler_particles = []
        self.permanent_sprinkler_particles = []
        
        self.weather = 'sunny'
        self.last_weather_change = time.time()
        self.weather_duration = random.uniform(30, 60)
        self.rain_particles = []
        
        for row in range(3):
            for col in range(4):
                x = 150 + col * 100
                y = 150 + row * 120
                # Leere Felder erstellen (tote Pflanzen)
                empty_veg = Vegetable(x, y, 'tomato')  # Typ ist egal, da tot
                empty_veg.plant_dead = True
                empty_veg.grown = False
                empty_veg.soil_fertility = 0.2  # Zu wenig zum Wiederbeleben
                empty_veg.soil_moisture = 0.2   # Zu wenig zum Wiederbeleben
                self.vegetables.append(empty_veg)
    
    def update(self):
        current_time = time.time()
        
        if current_time - self.last_weather_change > self.weather_duration:
            weather_options = ['sunny', 'rainy', 'cloudy']
            self.weather = random.choice(weather_options)
            self.last_weather_change = current_time
            self.weather_duration = random.uniform(20, 45)

        # Play appropriate ambient sound based on weather
        if self.weather == 'rainy':
            self.sound.play_ambient('rain')
        elif self.weather == 'sunny':
            self.sound.play_ambient('birds')
        else:  # cloudy
            self.sound.stop_ambient()

        if self.weather == 'rainy':
            if len(self.rain_particles) < 100:
                for i in range(5):
                    particle = {
                        'x': random.randint(0, WINDOW_WIDTH),
                        'y': random.randint(-20, 0),
                        'speed': random.uniform(3, 7)
                    }
                    self.rain_particles.append(particle)
            
            for particle in self.rain_particles[:]:
                particle['y'] += particle['speed']
                particle['x'] += random.uniform(-0.5, 0.5)
                if particle['y'] > WINDOW_HEIGHT:
                    self.rain_particles.remove(particle)
        else:
            self.rain_particles = []
        
        if self.inventory['sprinkler_system']:
            if len(self.permanent_sprinkler_particles) == 0:
                for vegetable in self.vegetables:
                    for i in range(5):
                        particle = {
                            'x': vegetable.x + 30 + random.randint(-15, 15),
                            'y': vegetable.y - 10 + random.randint(-5, 5),
                            'base_y': vegetable.y - 10,
                            'oscillation': random.uniform(0, 6.28),
                            'speed': random.uniform(0.02, 0.05)
                        }
                        self.permanent_sprinkler_particles.append(particle)
            
            for particle in self.permanent_sprinkler_particles:
                particle['oscillation'] += particle['speed']
                particle['y'] = particle['base_y'] + math.sin(particle['oscillation']) * 3
            
            if current_time - self.last_sprinkler_time > 10.0:
                for vegetable in self.vegetables:
                    if not vegetable.plant_dead and vegetable.soil_moisture < 0.8:
                        vegetable.soil_moisture = min(1.0, vegetable.soil_moisture + 0.3)
                self.last_sprinkler_time = current_time
        
        self.sprinkler_particles = [p for p in self.sprinkler_particles if current_time - p['spawn_time'] < 1.5]
        
        for particle in self.sprinkler_particles:
            time_passed = current_time - particle['spawn_time']
            particle['y'] += particle['velocity'] * time_passed
            particle['velocity'] += 50 * time_passed
        
        for vegetable in self.vegetables:
            vegetable.update(self.weather)

        # Update visual effects
        self.update_visual_effects()

    def update_visual_effects(self):
        """Update all visual effects animations"""
        current_time = time.time()

        # Update cloud animation
        self.cloud_offset = (self.cloud_offset + 0.5) % WINDOW_WIDTH

        # Update sun rotation
        self.sun_rotation = (self.sun_rotation + 0.02) % (2 * math.pi)

        # Update coin popups
        self.coin_popups = [p for p in self.coin_popups if current_time - p['spawn_time'] < 1.5]
        for popup in self.coin_popups:
            popup['y'] -= 0.5  # Float upward

        # Update sparkle particles
        self.sparkle_particles = [p for p in self.sparkle_particles if current_time - p['spawn_time'] < 0.8]

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
        for i in range(8):
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
        # Update sparkle positions
        for particle in self.sparkle_particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']

    def update_hover(self, mouse_pos):
        """Update which vegetable is being hovered over"""
        self.hovered_vegetable = None
        for vegetable in self.vegetables:
            if vegetable.rect.collidepoint(mouse_pos):
                self.hovered_vegetable = vegetable
                break

    def handle_click(self, mouse_pos, right_click=False):
        shop_button_rect = pygame.Rect(600, 280, 180, 40)
        mute_button_rect = pygame.Rect(600, 330, 180, 35)

        # Check Mute button first
        if mute_button_rect.collidepoint(mouse_pos) and not right_click:
            self.sound.toggle_mute()
            return "Sound " + ("ausgeschaltet" if self.sound.muted else "eingeschaltet")

        # Prüfe Inventory-Button-Klicks zuerst
        for tool, rect in self.button_rects.items():
            if rect.collidepoint(mouse_pos) and not right_click:
                if self.inventory[tool] > 0:
                    self.active_tool = tool
                    return f"{tool.replace('_', ' ').title()} ausgewählt - Feld anklicken"
                else:
                    return f"Kein {tool.replace('_', ' ')} vorhanden!"
        
        if shop_button_rect.collidepoint(mouse_pos) and not right_click:
            self.show_shop = not self.show_shop
            return "Shop geöffnet!" if self.show_shop else "Shop geschlossen!"
        
        if self.show_shop:
            return self.handle_shop_click(mouse_pos)
        
        for vegetable in self.vegetables:
            if vegetable.rect.collidepoint(mouse_pos):
                if right_click:
                    self.selected_vegetable = vegetable
                    return f"Feld ausgewählt (Fruchtbarkeit: {vegetable.soil_fertility:.1f})"
                else:
                    # Tool anwenden wenn eins ausgewählt ist
                    if self.active_tool:
                        return self.apply_tool(vegetable)
                    else:
                        # Standard-Aktionen ohne Tool
                        if vegetable.weed_level > 0:
                            clicks_needed = vegetable.remove_weeds()
                            self.sound.play('weed')
                            if vegetable.weed_level > 0:
                                return f"Unkraut reduziert! Level {vegetable.weed_level} ({vegetable.weed_level} Klicks nötig)"
                            else:
                                return "Unkraut komplett entfernt!"
                        elif vegetable.plant_dead:
                            self.sound.play('error')
                            return "Totes Feld - kaufe Samen im Shop zum Pflanzen!"
                        else:
                            earned = vegetable.harvest()
                            if earned > 0:
                                self.sound.play('harvest')
                                # Add visual effects
                                self.add_sparkles(vegetable.x, vegetable.y, YELLOW)
                                self.add_coin_popup(vegetable.x, vegetable.y, earned)
                            self.credits += earned
                            return f"Geerntet: {earned} Credits"
        return ""
    
    def apply_tool(self, vegetable):
        if self.active_tool == 'fertilizer':
            if self.inventory['fertilizer'] > 0:
                self.inventory['fertilizer'] -= 1
                vegetable.fertilize()
                self.sound.play('fertilize')
                self.add_sparkles(vegetable.x, vegetable.y, GREEN)
                self.active_tool = None
                return f"Gedüngt! ({self.inventory['fertilizer']} übrig)"
            else:
                self.sound.play('error')
                return "Kein Dünger vorhanden!"

        elif self.active_tool == 'water':
            if self.inventory['water'] > 0:
                self.inventory['water'] -= 1
                vegetable.water()
                self.sound.play('water')
                self.add_sparkles(vegetable.x, vegetable.y, WATER_BLUE)
                self.active_tool = None
                return f"Gegossen! ({self.inventory['water']} übrig)"
            else:
                self.sound.play('error')
                return "Kein Wasser vorhanden!"

        elif self.active_tool == 'weed_killer':
            if self.inventory['weed_killer'] > 0 and vegetable.weed_level > 0:
                self.inventory['weed_killer'] -= 1
                vegetable.weed_level = 0
                vegetable.weed_start_time = None
                self.sound.play('weed')
                self.active_tool = None
                return f"Unkraut entfernt! ({self.inventory['weed_killer']} übrig)"
            elif vegetable.weed_level == 0:
                self.sound.play('error')
                return "Kein Unkraut auf diesem Feld!"
            else:
                self.sound.play('error')
                return "Kein Unkrautkiller vorhanden!"

        elif self.active_tool in ['tomato_seeds', 'carrot_seeds', 'eggplant_seeds']:
            if vegetable.weed_level > 0:
                self.sound.play('error')
                return "Unkraut muss zuerst entfernt werden!"
            elif self.inventory[self.active_tool] > 0 and vegetable.plant_dead:
                self.inventory[self.active_tool] -= 1
                seed_type = self.active_tool.replace('_seeds', '')
                vegetable.plant_seed(seed_type)
                self.sound.play('plant')
                self.active_tool = None
                return f"{seed_type.title()}-Samen gepflanzt! ({self.inventory[self.active_tool + '_seeds'] if self.active_tool else 0} übrig)"
            elif not vegetable.plant_dead:
                self.sound.play('error')
                return "Feld ist nicht tot - kann nicht pflanzen!"
            else:
                self.sound.play('error')
                return f"Keine {self.active_tool.replace('_', ' ')} vorhanden!"
        
        return ""
    
    def handle_shop_click(self, mouse_pos):
        shop_items = [
            ('tomato_seeds', 210, 240),
            ('carrot_seeds', 210, 270),
            ('eggplant_seeds', 210, 300),
            ('sprinkler_system', 210, 330),
            ('weed_killer', 210, 360),
            ('fertilizer', 210, 390),
            ('water', 210, 420)
        ]
        
        for item, x, y in shop_items:
            button_rect = pygame.Rect(x, y, 380, 25)
            if button_rect.collidepoint(mouse_pos):
                return self.buy_item(item)
        
        return ""
    
    def buy_item(self, item):
        if item == 'sprinkler_system' and self.inventory['sprinkler_system']:
            self.sound.play('error')
            return "Sprinkleranlage bereits gekauft!"

        price = self.shop_prices[item]
        if self.credits >= price:
            self.credits -= price
            if item == 'sprinkler_system':
                self.inventory[item] = True
            else:
                self.inventory[item] += 1
            self.sound.play('buy')
            return f"{item.replace('_', ' ').title()} gekauft für {price} Credits!"
        else:
            self.sound.play('error')
            return f"Nicht genug Credits! Brauche {price}"
    
    def draw_icon(self, screen, tool_type, x, y):
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
    
    def draw_inventory_buttons(self, screen, font):
        buttons = [
            ('fertilizer', 600, 80),     ('water', 700, 80),
            ('weed_killer', 600, 130),   ('tomato_seeds', 700, 130),
            ('carrot_seeds', 600, 180),  ('eggplant_seeds', 700, 180)
        ]
        
        self.button_rects = {}
        
        for tool, x, y in buttons:
            if self.inventory[tool] > 0:
                color = GREEN
            else:
                color = RED
            
            if self.active_tool == tool:
                color = YELLOW
            
            rect = pygame.Rect(x, y, 85, 40)
            self.button_rects[tool] = rect
            
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            
            self.draw_icon(screen, tool, x, y)
            
            count_text = font.render(str(self.inventory[tool]), True, BLACK)
            screen.blit(count_text, (x + 65, y + 25))

    def draw(self, screen, font, title_font):
        if self.weather == 'sunny':
            screen.fill((50, 150, 50))
        elif self.weather == 'rainy':
            screen.fill((40, 100, 40))
        else:
            screen.fill((45, 120, 45))
        
        title = title_font.render("Garten-Spiel", True, BLACK)
        screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 20))
        
        credits_text = font.render(f"Credits: {self.credits}", True, BLACK)
        screen.blit(credits_text, (20, 20))
        
        weather_colors = {'sunny': YELLOW, 'rainy': WATER_BLUE, 'cloudy': GRAY}
        weather_text = font.render(f"Wetter: {self.weather.title()}", True, weather_colors[self.weather])
        screen.blit(weather_text, (20, 50))
        
        self.draw_inventory_buttons(screen, font)

        shop_button = pygame.Rect(600, 280, 180, 40)
        pygame.draw.rect(screen, YELLOW, shop_button)
        pygame.draw.rect(screen, BLACK, shop_button, 2)
        shop_text = font.render("Shop", True, BLACK)
        screen.blit(shop_text, (665, 295))

        # Mute Button
        mute_button = pygame.Rect(600, 330, 180, 35)
        mute_color = RED if self.sound.muted else GREEN
        pygame.draw.rect(screen, mute_color, mute_button)
        pygame.draw.rect(screen, BLACK, mute_button, 2)
        mute_text = font.render("🔇 Muted" if self.sound.muted else "🔊 Sound ON", True, BLACK)
        screen.blit(mute_text, (630, 338))
        
        if self.selected_vegetable:
            selection_rect = pygame.Rect(self.selected_vegetable.x - 2, 
                                       self.selected_vegetable.y - 2, 64, 64)
            pygame.draw.rect(screen, (255, 255, 0), selection_rect, 3)
        
        info_text1 = font.render("Links: Ernten/Unkraut entfernen | Rechts: Feld wählen", True, BLACK)
        screen.blit(info_text1, (20, WINDOW_HEIGHT - 60))
        
        info_text2 = font.render("Tool wählen → Feld klicken | Rechts=Feld auswählen | Gelb=Aktives Tool", True, BLACK)
        screen.blit(info_text2, (20, WINDOW_HEIGHT - 40))
        
        for vegetable in self.vegetables:
            vegetable.draw(screen, font)

            # Draw hover effect
            if self.hovered_vegetable == vegetable:
                glow_rect = pygame.Rect(vegetable.x - 4, vegetable.y - 4, 68, 68)
                pygame.draw.rect(screen, (255, 255, 100), glow_rect, 3)
                # Draw tooltip with info
                if not vegetable.plant_dead:
                    if vegetable.grown:
                        tooltip_text = font.render(f"Bereit zum Ernten! +{vegetable.credits[vegetable.type]}", True, WHITE)
                    else:
                        remaining = max(0, vegetable.regrow_time - time.time())
                        tooltip_text = font.render(f"Wächst... {remaining:.1f}s", True, WHITE)
                    tooltip_bg = pygame.Rect(vegetable.x - 10, vegetable.y - 40, tooltip_text.get_width() + 10, 25)
                    pygame.draw.rect(screen, BLACK, tooltip_bg)
                    pygame.draw.rect(screen, YELLOW, tooltip_bg, 1)
                    screen.blit(tooltip_text, (vegetable.x - 5, vegetable.y - 35))

            # Draw growth progress bar for growing plants
            if not vegetable.plant_dead and not vegetable.grown:
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
        
        if self.inventory['sprinkler_system']:
            for row in range(3):
                for col in range(4):
                    x = 150 + col * 100 + 45
                    y = 150 + row * 120 - 25
                    pygame.draw.rect(screen, GRAY, (x, y, 10, 15))
                    pygame.draw.circle(screen, (100, 100, 100), (x + 5, y + 5), 3)
        
        for particle in self.permanent_sprinkler_particles:
            pygame.draw.circle(screen, WATER_BLUE, 
                             (int(particle['x']), int(particle['y'])), 2)
        
        for particle in self.sprinkler_particles:
            alpha = max(0, 1 - (time.time() - particle['spawn_time']) / 1.5)
            if alpha > 0:
                size = int(2 * alpha)
                if size > 0:
                    pygame.draw.circle(screen, WATER_BLUE, 
                                     (int(particle['x']), int(particle['y'])), size)
        
        if self.weather == 'sunny':
            # Draw sun with animated rays
            pygame.draw.circle(screen, YELLOW, (WINDOW_WIDTH - 60, 60), 25)
            for i in range(12):  # More rays
                angle = i * math.pi / 6 + self.sun_rotation
                start_x = WINDOW_WIDTH - 60 + math.cos(angle) * 35
                start_y = 60 + math.sin(angle) * 35
                end_x = WINDOW_WIDTH - 60 + math.cos(angle) * 48
                end_y = 60 + math.sin(angle) * 48
                # Varying thickness for better effect
                thickness = 3 if i % 2 == 0 else 2
                pygame.draw.line(screen, YELLOW, (start_x, start_y), (end_x, end_y), thickness)
            # Add sun glow
            pygame.draw.circle(screen, (255, 255, 150), (WINDOW_WIDTH - 60, 60), 25, 2)
        elif self.weather == 'cloudy':
            # Animated clouds
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
        
        # Draw improved rain with splash effects
        for particle in self.rain_particles:
            # Rain drops
            pygame.draw.line(screen, WATER_BLUE,
                           (particle['x'], particle['y']),
                           (particle['x'] - 2, particle['y'] + 10), 2)
            # Add some lighter drops for depth
            if random.random() > 0.7:
                pygame.draw.line(screen, (100, 200, 255),
                               (particle['x'] + 1, particle['y']),
                               (particle['x'] - 1, particle['y'] + 8), 1)

        # Draw sparkle particles (harvest/water/fertilize effects)
        for particle in self.sparkle_particles:
            age = time.time() - particle['spawn_time']
            alpha = max(0, 1 - age / 0.8)
            if alpha > 0:
                size = int(particle['size'] * alpha)
                if size > 0:
                    # Draw sparkle as a star shape
                    x, y = int(particle['x']), int(particle['y'])
                    color = particle['color']
                    pygame.draw.circle(screen, color, (x, y), size)
                    # Add cross for star effect
                    if size > 2:
                        pygame.draw.line(screen, color, (x - size, y), (x + size, y), 2)
                        pygame.draw.line(screen, color, (x, y - size), (x, y + size), 2)

        # Draw coin popups
        for popup in self.coin_popups:
            age = time.time() - popup['spawn_time']
            alpha = max(0, 1 - age / 1.5)
            if alpha > 0:
                # Fade out and float up
                coin_text = font.render(f"+{popup['amount']}", True, YELLOW)
                text_with_shadow = font.render(f"+{popup['amount']}", True, BLACK)
                # Shadow
                screen.blit(text_with_shadow, (int(popup['x']) + 22, int(popup['y']) - 42))
                # Main text
                screen.blit(coin_text, (int(popup['x']) + 20, int(popup['y']) - 44))

        if self.show_shop:
            self.draw_shop(screen, font)
    
    def draw_shop(self, screen, font):
        shop_bg = pygame.Rect(200, 200, 400, 300)
        pygame.draw.rect(screen, WHITE, shop_bg)
        pygame.draw.rect(screen, BLACK, shop_bg, 3)
        
        title_text = font.render("SHOP", True, BLACK)
        screen.blit(title_text, (370, 210))
        
        shop_items = [
            ('Tomaten-Samen', 'tomato_seeds', 15),
            ('Karotten-Samen', 'carrot_seeds', 10), 
            ('Auberginen-Samen', 'eggplant_seeds', 20),
            ('Sprinkleranlage', 'sprinkler_system', 100),
            ('Unkrautkiller', 'weed_killer', 25),
            ('Dünger', 'fertilizer', 10),
            ('Wasser', 'water', 1)
        ]
        
        y_offset = 240
        for display_name, item_key, price in shop_items:
            color = GREEN if self.credits >= price else RED
            if item_key == 'sprinkler_system' and self.inventory[item_key]:
                color = GRAY
                display_name += " (Gekauft)"
            
            button_rect = pygame.Rect(210, y_offset, 380, 25)
            pygame.draw.rect(screen, color, button_rect)
            pygame.draw.rect(screen, BLACK, button_rect, 1)
            
            item_text = font.render(f"{display_name}: {price} Credits", True, BLACK)
            screen.blit(item_text, (215, y_offset + 5))
            
            if item_key != 'sprinkler_system' and self.inventory[item_key] > 0:
                count_text = font.render(f"({self.inventory[item_key]})", True, BLACK)
                screen.blit(count_text, (550, y_offset + 5))
            
            y_offset += 30
        
        if self.inventory['sprinkler_system']:
            sprinkler_text = font.render("Sprinkler aktiv!", True, GREEN)
            screen.blit(sprinkler_text, (265, 470))

async def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Garten-Spiel")
    clock = pygame.time.Clock()
    
    font = pygame.font.Font(None, 24)
    title_font = pygame.font.Font(None, 48)
    
    garden = Garden()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    message = garden.handle_click(event.pos, False)
                    if message:
                        print(message)
                elif event.button == 3:
                    message = garden.handle_click(event.pos, True)
                    if message:
                        print(message)

        # Update hover effect based on mouse position
        mouse_pos = pygame.mouse.get_pos()
        garden.update_hover(mouse_pos)

        garden.update()
        garden.draw(screen, font, title_font)
        
        pygame.display.flip()
        await asyncio.sleep(0)  # Allow other async tasks to run
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())