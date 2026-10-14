import sys
import random
import pygame
import math
import numpy as np

pygame.init()
w = 1920
h = 930
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Langton's Ant")
clock = pygame.time.Clock()
targetFps = 500
fontObj = pygame.font.SysFont('Arial Black', 24)
paused = False
empty = True
Ax = 100
Ay = 45
direction = 1 # N,E,S,W

CellSize = 10
# Calculate how many cells actually fit on the screen
cols = w // CellSize
rows = h // CellSize

if empty:
    grid = np.zeros((cols, rows))
else:
    grid = np.random.choice([0, 1], size=(rows, cols), p=[0.9, 0.1])

def update():
    global Ax,Ay,direction

    if grid[Ax,Ay] == 1:
        direction += 1
        grid[Ax,Ay] = 0
    else:
        direction -= 1
        grid[Ax, Ay] = 1

    if direction > 4:
        direction = 1
    elif direction < 1:
        direction = 4

    if direction == 1:
        Ay -= 1
    elif direction == 2:
        Ax += 1
    elif direction == 3:
        Ay += 1
    elif direction == 4:
        Ax -= 1

running = True
while running:
    deltaTime = clock.tick(targetFps) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                paused = not paused

    if not paused:
        update()
    for x in range(cols):
        for y in range(rows):
            screen_x = x * CellSize
            screen_y = y * CellSize
            pygame.draw.rect(
                screen,
                (255, 255, 255) if grid[x,y] == 1 else (0,0,0),
                (screen_x, screen_y, CellSize, CellSize)
            )

    fps = clock.get_fps()
    fpsText = fontObj.render(f"FPS: {fps:.0f}", True, (0, 255, 0))  # Red text stands out better
    screen.blit(fpsText, (15, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
