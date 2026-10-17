import sys
import random
import pygame
import math

pygame.init()
screen = pygame.display.set_mode((1728, 1000))
pygame.display.set_caption("Galaxy")
clock = pygame.time.Clock()
targetFps = 60

fontObj = pygame.font.Font('Arial Black.ttf', 32)
stars = []
M = 200000
G = 100
center = pygame.Vector2(864, 500)


class Star:
    def __init__(self):
        self.size = random.uniform(1, 2.2)
        self.x = random.randint(0, 1728)
        self.y = random.randint(0, 1000)
        self.grayValue = random.randint(150, 255)
        self.color = (self.grayValue, self.grayValue, self.grayValue)
        self.position = pygame.Vector2(self.x, self.y)

        # 1. Vector and Distance to center
        r_vec = center - self.position
        r = r_vec.length()

        # Avoid divide-by-zero if a star spawns exactly at (864, 500)
        if r < 10:
            r = 10

        # 2. Orbital Speed (Scalar)
        speed = math.sqrt((G * M) / r)

        # 3. Tangent Vector for 90-degree orbital motion
        tangent = pygame.Vector2(-r_vec.y, r_vec.x).normalize()
        self.velocity = tangent * speed

        self.acceleration = pygame.Vector2(0, 0)

    def update(self, delta_time):
        # Recalculate distance and direction dynamically every frame
        r_vec = center - self.position
        r = r_vec.length()

        # Softening factor to prevent infinite acceleration at core
        if r < 15:
            r = 15

        # Gravitational Acceleration Magnitude: a = (G * M) / r^2
        acc_magnitude = (G * M) / (r ** 2)

        # Vector acceleration pointing directly toward center
        self.acceleration = r_vec.normalize() * acc_magnitude

        # Update physics
        self.velocity += self.acceleration * delta_time
        self.position += self.velocity * delta_time
        if int(r/3) <= 255:
            self.color = (255-int(r/3), 255-int(r/3),255-int(r/3))
        else:
            self.color = (50,50,50)


for i in range(1000):
    stars.append(Star())

running = True
while running:
    deltaTime = clock.tick(targetFps) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Draw Central Black Hole / Galactic Core
    pygame.draw.circle(screen, (217, 79, 20), center, 20, width=2)

    for star in stars:
        star.update(deltaTime)
        pygame.draw.circle(screen, star.color, star.position, star.size, width=0)

    fps = clock.get_fps()
    fpsText = fontObj.render(f"FPS: {fps:.0f}", True, (255, 255, 255))
    screen.blit(fpsText, (15, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
