import sys
import random
import pygame
import math
import numpy as np

pygame.init()
w = 1920
h = 930
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Flock of Birds")
clock = pygame.time.Clock()
targetFps = 60
fontObj = pygame.font.SysFont('Arial Black', 24)
paused = False

running = True
while running:
    deltaTime = clock.tick(targetFps) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                paused = not paused

    screen.fill((0, 0, 0))

    fps = clock.get_fps()
    fpsText = fontObj.render(f"FPS: {fps:.0f}", True, (255, 255, 255))
    screen.blit(fpsText, (15, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
