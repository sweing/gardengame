# Garden Game 🌱

A pygame-based garden management game with weather systems, pest control, automated helpers, and beautiful animations.

## Features

### Core Gameplay
- **Garden Management**: Plant, water, fertilize, and harvest 3 types of vegetables (tomatoes, carrots, eggplants)
- **Weather System**: Dynamic weather (sunny, rainy, cloudy) affects plant growth and moisture
- **Shop System**: Buy seeds, tools, upgrades, and helpers
- **Storage House**: Decorative building representing your inventory with animated chimney smoke

### Pests & Challenges
- **Snails**: Crawl from screen edges to eat your plants (both ripe and unripe!)
  - More snails spawn during rain (2-4 every 5 seconds)
  - Click snails while moving to remove them
- **Weeds**: Grow on plots and slow down plant growth
  - Manual removal by clicking
  - Purchase weed killer for instant removal

### Helpers & Automation
- **Duck 🦆** (15 credits, 2 min): Cute helper that waddles around eating snails
  - Animated walking with waddling motion
  - Shows hearts when eating snails
- **Weed Picker** (10 credits, 2 min): Helper that removes weeds automatically
  - Animated walking with swinging arms and legs
  - Holds umbrella ☂️ when it rains!
- **Sprinkler System** (100 credits): Automatically waters all plots every 10 seconds

### Polish & Effects
- **Sound & Music**: Background music with separate toggles for music and sound effects
- **Visual Effects**: Particle effects, animations, growth indicators, and tooltips
- **Walking Animations**: All helpers have smooth walking animations with bobbing and leg movement

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sweing/gardengame.git
cd gardengame
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pygame
```

## Running the Game

```bash
python main.py
```

## How to Play

### Controls
- **Left Click**: Harvest vegetables, remove weeds, or use selected tool
- **Right Click**: Select a plot to view details
- **Shop Button**: Open/close the shop
- **Inventory Buttons**: Select tools (fertilizer, water, seeds, etc.)

### Game Mechanics

1. **Starting Out**: You begin with 50 credits and empty plots
2. **Buy Seeds**: Open the shop and purchase seeds
3. **Plant**: Select seeds from inventory and click on dead plots
4. **Maintain**: Water and fertilize plants to keep them healthy
5. **Harvest**: Click on grown vegetables to earn credits
6. **Manage Threats**:
   - Remove weeds by clicking (or buy weed picker helper)
   - Click on snails to remove them (or buy duck helper)
   - Watch out for rain - snails spawn 3x faster!
7. **Automate**: Purchase helpers and sprinkler system to automate tasks

### Vegetables

| Vegetable | Cost | Credits | Growth Time |
|-----------|------|---------|-------------|
| Tomato    | 15   | 5       | 3-8 seconds |
| Carrot    | 10   | 3       | 3-8 seconds |
| Eggplant  | 20   | 7       | 3-8 seconds |

### Tools & Upgrades

| Item | Cost | Duration | Description |
|------|------|----------|-------------|
| Water | 1 | Instant | Increase soil moisture on one plot |
| Fertilizer | 10 | Instant | Restore soil fertility on one plot |
| Weed Killer | 25 | Instant | Remove all weeds from one plot |
| Weed Picker | 10 | 2 minutes | Helper that walks around removing weeds |
| Duck 🦆 | 15 | 2 minutes | Helper that eats snails |
| Sprinkler System | 100 | Permanent | Automatically waters all plots every 10 seconds |

## Project Structure

```
gardengame/
├── main.py              # Entry point
├── config.py            # Game configuration and constants
├── garden.py            # Main game logic coordinator
├── vegetable.py         # Vegetable plot class with growth mechanics
├── inventory.py         # Inventory and tool management
├── shop.py              # Shop system for purchases
├── weather.py           # Dynamic weather system
├── effects.py           # Visual effects and particle systems
├── sound_manager.py     # Sound and music management
├── snail.py             # Snail pest system
├── duck.py              # Duck helper that eats snails
├── weed_picker.py       # Weed picker helper
├── storage_house.py     # Storage building with animations
├── sounds/              # Sound files (optional)
└── README.md            # This file
```

## Development

The game is structured using modular Python classes for maintainability:

- **Config Module**: Centralized game constants and settings
- **Garden Module**: Main game coordinator that manages all systems
- **Vegetable Module**: Individual plot logic, growth mechanics, and rendering
- **Inventory Module**: Tool and seed management with UI
- **Shop Module**: Purchase and upgrade system
- **Weather Module**: Dynamic weather effects that influence gameplay
- **Effects Module**: Particle systems and visual feedback
- **Sound Manager**: Audio playback and management with separate music/SFX controls
- **Pest System**: Snail enemies that threaten plants
- **Helper System**: Duck and weed picker AI helpers with pathfinding
- **Storage House**: Decorative building with smoke animation

## License

This project is open source and available for educational purposes.

## Credits

Developed with Python and Pygame.
