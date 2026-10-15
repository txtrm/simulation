import sys
import random
import pygame
import math
import numpy as np

pygame.init()
w = 1920
h = 930
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()
targetFps = 60
fontObj = pygame.font.SysFont('Arial Black', 24)
paused = False
empty = False

CellSize = 10
# Calculate how many cells actually fit on the screen
cols = w // CellSize
rows = h // CellSize

if empty:
    grid = np.zeros((rows, cols))
else:
    grid = np.random.choice([0, 1], size=(rows, cols), p=[0.9, 0.1])

def update():
    global grid
    # Create a copy to read from so modifications don't ruin neighbor counts
    current_grid = grid.copy()

    for x in range(cols):
        for y in range(rows):
            neighbors = 0
            if x != 0 and current_grid[y, x-1] == 1: # left
                neighbors += 1
            if x != 0 and y != 0 and current_grid[y-1, x-1] == 1: # top-left
                neighbors += 1
            if y != 0 and current_grid[y-1, x] == 1: # top
                neighbors += 1
            if y != 0 and x != cols-1 and current_grid[y-1, x+1] == 1: # top-right
                neighbors += 1
            if x != cols-1 and current_grid[y, x+1] == 1: # right
                neighbors += 1
            if x != cols-1 and y != rows-1 and current_grid[y+1, x+1] == 1: # bottom-right
                neighbors += 1
            if y != rows-1 and current_grid[y+1, x] == 1: # bottom
                neighbors += 1
            if y != rows-1 and x != 0 and current_grid[y+1, x-1] == 1: # bottom-left
                neighbors += 1

            # RULES
            if neighbors < 2:
                grid[y, x] = 0
            if neighbors == 3:
                grid[y, x] = 1
            if neighbors > 3:
                grid[y, x] = 0

running = True
while running:
    deltaTime = clock.tick(targetFps) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                paused = not paused

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pixel_x, pixel_y = event.pos
                x = pixel_x // CellSize
                y = pixel_y // CellSize
                if grid[y,x] == 1:
                    grid[y,x] = 0
                elif grid[y,x] == 0:
                    grid[y,x] = 1

    screen.fill((0, 0, 0))
    if not paused:
        update()
    for x in range(cols):
        for y in range(rows):
            if grid[y, x] == 1:
                screen_x = x * CellSize
                screen_y = y * CellSize
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    (screen_x, screen_y, CellSize, CellSize)
                )

    fps = clock.get_fps()
    fpsText = fontObj.render(f"FPS: {fps:.0f}", True, (0, 255, 0))  # Red text stands out better
    screen.blit(fpsText, (15, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
