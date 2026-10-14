import sys
import pygame
import numpy as np
from perlin_noise import PerlinNoise

size = 500
pygame.init()
screen = pygame.display.set_mode((size, size))
pygame.display.set_caption("2d Procedural World")
clock = pygame.time.Clock()
targetFps = 60
offset = 0.0

# Initialize noise and scale factor
noise = PerlinNoise(octaves=1, seed=1)
scale = size/10  # Controls how zoomed in/out the terrain is

# Pre-generate the noise grid efficiently using NumPy
print("Generating noise map...")
x_coords = np.arange(size) / scale
y_coords = np.arange(size) / scale

# Create a grid of values
world_array = np.zeros((size, size, 3), dtype=np.uint8)
for w in range(size):
    for h in range(size):
        val = noise([w / scale, h / scale])
        if val > 0.25:
            world_array[w, h] = (0, 85, 255)
        elif 0.25 > val > 0.1:
            world_array[w, h] = (0, 136, 255)
        elif 0.1 > val > 0.0:
            world_array[w, h] = (0, 166, 255)
        elif 0.0 > val > -0.1:
            world_array[w, h] = (255, 246, 82)
        else:
            # Normalize Perlin noise output (typically -0.5 to 0.5) to 0-255 and make it green land
            world_array[w, h] = (92, 189, 62)

running = True
while running:
    clock.tick(targetFps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                offset += 0.05
                for w in range(size):
                    for h in range(size):
                        val = noise([w / scale, h / scale])
                        if val > 0.25+offset:
                            world_array[w, h] = (0, 85, 255)
                        elif 0.25+offset > val > 0.1+offset:
                            world_array[w, h] = (0, 136, 255)
                        elif 0.1+offset > val > 0.0+offset:
                            world_array[w, h] = (0, 166, 255)
                        elif 0.0+offset > val > -0.1+offset:
                            world_array[w, h] = (255, 246, 82)
                        else:
                            # Normalize Perlin noise output (typically -0.5 to 0.5) to 0-255 and make it green land
                            world_array[w, h] = (92, 189, 62)
            elif event.key == pygame.K_a:
                offset -= 0.05
                for w in range(size):
                    for h in range(size):
                        val = noise([w / scale, h / scale])
                        if val > 0.25+offset:
                            world_array[w, h] = (0, 85, 255)
                        elif 0.25+offset > val > 0.1+offset:
                            world_array[w, h] = (0, 136, 255)
                        elif 0.1+offset > val > 0.0+offset:
                            world_array[w, h] = (0, 166, 255)
                        elif 0.0+offset > val > -0.1+offset:
                            world_array[w, h] = (255, 246, 82)
                        else:
                            # Normalize Perlin noise output (typically -0.5 to 0.5) to 0-255 and make it green land
                            world_array[w, h] = (92, 189, 62)

    # Blit the pre-calculated array onto the screen instantly
    pygame.surfarray.blit_array(screen, world_array)
    pygame.display.flip()

pygame.quit()
sys.exit()
