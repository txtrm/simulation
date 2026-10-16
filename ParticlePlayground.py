import sys
import random
import pygame
import numpy as np

pygame.init()
w, h = 1920, 930
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Physics Particle Playground")
clock = pygame.time.Clock()
targetFps = 60
fontObj = pygame.font.SysFont('Arial Black', 24)
paused = False

CellSize = 5
cols, rows = w // CellSize, h // CellSize
grid = np.zeros((rows, cols))
DrawState = 1

COLORS = {
    1: (255, 222, 59),  # Sand
    2: (61, 113, 255),  # Water
    3: (128, 128, 128), # Stone
    4: (238, 255, 0)    # Acid
}

def update():
    for x in range(cols):
        for y in range(rows - 1, -1, -1):
            t = grid[y, x]
            if t == 0 or t == 3:  # Skip empty space and static stone
                continue

            # Acid dissolution check (destroys itself and any adjacent neighbor)
            if t == 4:
                destroyed = False
                for ny in (y - 1, y, y + 1):
                    for nx in (x - 1, x, x + 1):
                        if 0 <= ny < rows and 0 <= nx < cols and (ny != y or nx != x) and grid[ny, nx] in (1, 2, 3):
                            grid[ny, nx] = 0
                            grid[y, x] = 0
                            destroyed = True
                            break
                    if destroyed:
                        break
                if destroyed:
                    continue

            # Movement logic for Sand (1), Water (2), and Acid (4)
            d = random.choice([-1, 1])
            if y + 1 < rows and grid[y + 1, x] == 0:
                grid[y + 1, x], grid[y, x] = t, 0
            elif y + 1 < rows and 0 <= x + d < cols and grid[y + 1, x + d] == 0:
                grid[y + 1, x + d], grid[y, x] = t, 0
            elif y + 1 < rows and 0 <= x - d < cols and grid[y + 1, x - d] == 0:
                grid[y + 1, x - d], grid[y, x] = t, 0
            elif t in (2, 4):  # Liquids spread horizontally
                if 0 <= x + d < cols and grid[y, x + d] == 0:
                    grid[y, x + d], grid[y, x] = t, 0
                elif 0 <= x - d < cols and grid[y, x - d] == 0:
                    grid[y, x - d], grid[y, x] = t, 0

last_x, last_y = None, None
running = True

while running:
    clock.tick(targetFps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_r:
                grid.fill(0)
                paused = False
            elif pygame.K_0 <= event.key <= pygame.K_4:
                DrawState = event.key - pygame.K_0
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            last_x, last_y = event.pos[0] // CellSize, event.pos[1] // CellSize

    if pygame.mouse.get_pressed()[0]:
        px, py = pygame.mouse.get_pos()
        cx, cy = px // CellSize, py // CellSize
        if last_x is None:
            last_x, last_y = cx, cy

        steps = max(abs(cx - last_x), abs(cy - last_y)) or 1
        for i in range(steps + 1):
            ix = int(last_x + (cx - last_x) * (i / steps))
            iy = int(last_y + (cy - last_y) * (i / steps))
            if 0 <= ix < cols and 0 <= iy < rows:
                grid[iy, ix] = DrawState
        last_x, last_y = cx, cy
    else:
        last_x, last_y = None, None

    screen.fill((0, 0, 0))
    if not paused:
        update()

    # Draw grid particles
    for x in range(cols):
        for y in range(rows):
            if grid[y, x] in COLORS:
                pygame.draw.rect(screen, COLORS[grid[y, x]], (x * CellSize, y * CellSize, CellSize, CellSize))

    # Render UI Text
    texts = [
        f"FPS: {clock.get_fps():.0f}",
        "Keybinds:",
        "Sand: 1 | Water: 2",
        "Stone: 3 | Acid: 4",
        "Eraser: 0 | Reset: R",
        f"Paused: {paused}"
    ]
    for i, text in enumerate(texts):
        color = (0, 255, 0) if i == 0 else (255, 255, 255)
        screen.blit(fontObj.render(text, True, color), (15, 10 + i * 27))

    pygame.display.flip()

pygame.quit()
sys.exit()
