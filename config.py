"""
Game configuration and constants
"""

# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
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

# Vegetable settings
VEGETABLE_COLORS = {
    'tomato': RED,
    'carrot': ORANGE,
    'eggplant': PURPLE
}

VEGETABLE_CREDITS = {
    'tomato': 5,
    'carrot': 3,
    'eggplant': 7
}

# Shop prices
SHOP_PRICES = {
    'tomato_seeds': 15,
    'carrot_seeds': 10,
    'eggplant_seeds': 20,
    'sprinkler_system': 100,
    'weed_killer': 25,
    'weed_picker': 10,
    'duck': 15,
    'rain_barrel': 10,
    'weather_tv': 20,
    'fertilizer': 10,
    'water': 1
}

# Game mechanics
INITIAL_CREDITS = 50
BASE_MOISTURE_LOSS_RATE = 0.005
MOISTURE_LOSS_SUNNY = 2.0
MOISTURE_LOSS_RAINY = 0.2
MOISTURE_LOSS_CLOUDY = 1.0
RAIN_MOISTURE_GAIN = 0.01

# Growth settings
MIN_REGROW_TIME = 3
MAX_REGROW_TIME = 8
FERTILITY_LOSS_PER_HARVEST = 0.15
MIN_FERTILITY = 0.1

# Water settings
WATER_INCREASE_AMOUNT = 0.4
SPRINKLER_WATER_INCREASE = 0.3
SPRINKLER_INTERVAL = 10.0
SPRINKLER_THRESHOLD = 0.8

# Rain barrel settings
RAIN_BARREL_COLLECTION_INTERVAL = 10.0  # Collect water every 10 seconds during rain

# Weather TV settings
WEATHER_TV_X = 20
WEATHER_TV_Y = 400
WEATHER_TV_WIDTH = 120
WEATHER_TV_HEIGHT = 80

# Weed settings
WEED_CHECK_INTERVAL = 5.0
WEED_SPAWN_CHANCE = 0.3
WEED_GROWTH_TIME = 10
MAX_WEED_LEVEL = 10

# Snail settings (Schnecken)
SNAIL_CHECK_INTERVAL = 10.0  # Check every 10 seconds for snail spawn
SNAIL_SPAWN_CHANCE = 0.25     # 25% chance to spawn on ripe vegetables
SNAIL_EATING_TIME = 20.0      # Time in seconds until vegetable is eaten
MAX_SNAILS_PER_PLANT = 3      # Maximum snails on one plant

# Weather settings
MIN_WEATHER_DURATION = 20
MAX_WEATHER_DURATION = 45
WEATHER_OPTIONS = ['sunny', 'rainy', 'cloudy']

# Weather colors
WEATHER_COLORS = {
    'sunny': YELLOW,
    'rainy': WATER_BLUE,
    'cloudy': GRAY
}

# Background colors by weather
BACKGROUND_COLORS = {
    'sunny': (50, 150, 50),
    'rainy': (40, 100, 40),
    'cloudy': (45, 120, 45)
}

# Garden layout
GARDEN_ROWS = 3
GARDEN_COLS = 4
GARDEN_START_X = 150
GARDEN_START_Y = 150
GARDEN_SPACING_X = 100
GARDEN_SPACING_Y = 120

# Plot settings
PLOT_SIZE = 60
INITIAL_PLOT_FERTILITY = 0.2
INITIAL_PLOT_MOISTURE = 0.2

# Revival thresholds
REVIVAL_MIN_FERTILITY = 0.3
REVIVAL_MIN_MOISTURE = 0.3

# Seed planting values
SEED_PLANT_FERTILITY = 0.8
SEED_PLANT_MOISTURE = 0.8

# Sound files
SOUND_FILES = {
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

BACKGROUND_MUSIC = 'sounds/bgm.ogg'
DEFAULT_VOLUME = 0.7
MUSIC_VOLUME_MULTIPLIER = 0.5
AMBIENT_VOLUME_MULTIPLIER = 0.3

# Particle effects
WATER_PARTICLE_COUNT = 15
FERTILIZER_PARTICLE_COUNT = 15
WEED_PARTICLE_COUNT = 5
SPARKLE_PARTICLE_COUNT = 8
MAX_RAIN_PARTICLES = 100
RAIN_SPAWN_RATE = 5

# Animation settings
WATER_PARTICLE_LIFETIME = 1.0
FERTILIZER_PARTICLE_LIFETIME_MIN = 2.0
FERTILIZER_PARTICLE_LIFETIME_MAX = 3.5
WEED_PARTICLE_LIFETIME = 2.0
SEED_PARTICLE_LIFETIME = 2.0
SPARKLE_LIFETIME = 0.8
COIN_POPUP_LIFETIME = 1.5

# UI positions
SHOP_BUTTON_X = 600
SHOP_BUTTON_Y = 280
SHOP_BUTTON_WIDTH = 180
SHOP_BUTTON_HEIGHT = 40

MUTE_BUTTON_X = 600
MUTE_BUTTON_Y = 330
MUTE_BUTTON_WIDTH = 180
MUTE_BUTTON_HEIGHT = 35

MUSIC_BUTTON_X = 600
MUSIC_BUTTON_Y = 375
MUSIC_BUTTON_WIDTH = 180
MUSIC_BUTTON_HEIGHT = 35

# Inventory button layout
INVENTORY_BUTTONS = [
    ('fertilizer', 600, 80),
    ('water', 700, 80),
    ('weed_killer', 600, 130),
    ('tomato_seeds', 700, 130),
    ('carrot_seeds', 600, 180),
    ('eggplant_seeds', 700, 180)
]

INVENTORY_BUTTON_WIDTH = 85
INVENTORY_BUTTON_HEIGHT = 40

# Shop UI
SHOP_X = 150
SHOP_Y = 150
SHOP_WIDTH = 500
SHOP_HEIGHT = 400
SHOP_ITEM_HEIGHT = 25
SHOP_ITEM_START_Y = 190
SHOP_ITEM_SPACING = 30

SHOP_ITEMS = [
    ('Tomaten-Samen', 'tomato_seeds', 15),
    ('Karotten-Samen', 'carrot_seeds', 10),
    ('Auberginen-Samen', 'eggplant_seeds', 20),
    ('Sprinkleranlage', 'sprinkler_system', 100),
    ('Regentonne', 'rain_barrel', 10),
    ('Wetter-TV 📺', 'weather_tv', 20),
    ('Unkrautkiller', 'weed_killer', 25),
    ('Unkrautpflücker (2min)', 'weed_picker', 10),
    ('Ente 🦆 (2min)', 'duck', 15),
    ('Dünger', 'fertilizer', 10),
    ('Wasser', 'water', 1)
]
