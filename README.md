# Garden Game

A pygame-based garden management game with weather systems, shop mechanics, and particle effects.

## Features

- **Garden Management**: Plant, water, fertilize, and harvest 3 types of vegetables
- **Weather System**: Dynamic weather (sunny, rainy, cloudy) affects plant growth
- **Shop System**: Buy seeds, tools, and upgrades
- **Sprinkler Automation**: Purchase and automate watering
- **Sound & Music**: Background music and sound effects
- **Visual Effects**: Particle effects, animations, and tooltips

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
6. **Remove Weeds**: Click on plots with weeds to remove them

### Vegetables

| Vegetable | Cost | Credits | Growth Time |
|-----------|------|---------|-------------|
| Tomato    | 15   | 5       | 3-8 seconds |
| Carrot    | 10   | 3       | 3-8 seconds |
| Eggplant  | 20   | 7       | 3-8 seconds |

### Tools & Upgrades

- **Water** (1 credit): Increase soil moisture
- **Fertilizer** (10 credits): Restore soil fertility
- **Weed Killer** (25 credits): Instantly remove all weeds from a plot
- **Sprinkler System** (100 credits): Automatically waters all plots every 10 seconds

## Project Structure

```
gardengame/
├── main.py              # Entry point
├── config.py            # Game configuration and constants
├── garden.py            # Main game logic
├── vegetable.py         # Vegetable plot class
├── inventory.py         # Inventory management
├── shop.py              # Shop system
├── weather.py           # Weather system
├── effects.py           # Visual effects and particles
├── sound_manager.py     # Sound and music management
├── sounds/              # Sound files (optional)
└── README.md            # This file
```

## Development

The game is structured using modular Python classes for maintainability:

- **Config Module**: Centralized game constants and settings
- **Garden Module**: Main game coordinator
- **Vegetable Module**: Individual plot logic and rendering
- **Inventory Module**: Tool and seed management
- **Shop Module**: Purchase and upgrade system
- **Weather Module**: Dynamic weather effects
- **Effects Module**: Particle systems and visual feedback
- **Sound Manager**: Audio playback and management

## License

This project is open source and available for educational purposes.

## Credits

Developed with Python and Pygame.
