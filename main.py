"""
Garden Game - Main Entry Point

A pygame-based garden management game with:
- Planting, harvesting, watering, and fertilizing
- Weather system (sunny, rainy, cloudy)
- Shop system with seeds and upgrades
- Sprinkler automation
- Sound effects and background music
"""
import pygame
import asyncio
from garden import Garden
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS


async def main():
    """Main game loop"""
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Garten-Spiel")
    clock = pygame.time.Clock()

    # Setup fonts
    font = pygame.font.Font(None, 24)
    title_font = pygame.font.Font(None, 48)

    # Create garden
    garden = Garden()

    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    message = garden.handle_click(event.pos, False)
                    if message:
                        print(message)
                elif event.button == 3:  # Right click
                    message = garden.handle_click(event.pos, True)
                    if message:
                        print(message)

        # Update hover effect based on mouse position
        mouse_pos = pygame.mouse.get_pos()
        garden.update_hover(mouse_pos)

        # Update game state
        garden.update()

        # Draw everything
        garden.draw(screen, font, title_font)

        # Update display
        pygame.display.flip()
        await asyncio.sleep(0)  # Allow other async tasks to run
        clock.tick(FPS)

    # Cleanup
    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
