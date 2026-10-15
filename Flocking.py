import sys
import random
import pygame
import math

pygame.init()
w = 1920
h = 930
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Flock of Birds")
clock = pygame.time.Clock()
targetFps = 60
fontObj = pygame.font.SysFont('Arial Black', 24)
paused = False
flock = []
amount = 50
speed = 3
radius = 5
searchR = 80
personal_space = 35  # Distance at which boids start trying to push apart


class Boid:
    def __init__(self):
        self.pos = pygame.Vector2(random.randint(0, w), random.randint(0, h))
        self.direction = random.uniform(0, 2 * math.pi)
        self.steer_direction = self.direction

    def selfUpdate(self):
        # 1. Smoothly interpolate current angle toward the target steering angle
        diff = (self.steer_direction - self.direction + math.pi) % (2 * math.pi) - math.pi
        self.direction += diff * 0.1  # Turning speed

        # 2. Move forward at constant speed
        self.pos.x += math.cos(self.direction) * speed
        self.pos.y += math.sin(self.direction) * speed

        # 3. Screen wrapping
        if self.pos.x < 0:
            self.pos.x = w
        elif self.pos.x > w:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = h
        elif self.pos.y > h:
            self.pos.y = 0


def update(bird, flock):
    sum_cos = 0
    sum_sin = 0
    center_x = 0
    center_y = 0
    separation_vec = pygame.Vector2(0, 0)
    count = 0

    for other in flock:
        if other != bird:
            dist = (other.pos - bird.pos).magnitude()
            if dist <= searchR:
                # 1. Alignment data
                sum_cos += math.cos(other.direction)
                sum_sin += math.sin(other.direction)

                # 2. Cohesion data (summing neighbor positions)
                center_x += other.pos.x
                center_y += other.pos.y

                # 3. Separation data (if too close, push away)
                if 0 < dist < personal_space:
                    # Vector pointing away from neighbor, divided by dist so closer = stronger push
                    push_away = (bird.pos - other.pos) / dist
                    separation_vec += push_away

                count += 1

    if count > 0:
        # Build individual rule vectors
        align_vec = pygame.Vector2(sum_cos / count, sum_sin / count)

        center_of_mass = pygame.Vector2(center_x / count, center_y / count)
        cohesion_vec = center_of_mass - bird.pos
        if cohesion_vec.length_squared() > 0:
            cohesion_vec = cohesion_vec.normalize()

        if separation_vec.length_squared() > 0:
            separation_vec = separation_vec.normalize()

        # Combine all three forces! (You can tweak weights to change behavior)
        # e.g., Giving separation a bit more weight makes them look very organic
        combined_vec = (align_vec * 1.0) + (cohesion_vec * 1.0) + (separation_vec * 1.5)

        if combined_vec.length_squared() > 0:
            bird.steer_direction = math.atan2(combined_vec.y, combined_vec.x)


for i in range(amount):
    flock.append(Boid())

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

    if not paused:
        for boid in flock:
            update(boid, flock)
            boid.selfUpdate()

    for boid in flock:
        pygame.draw.circle(screen, (255, 255, 255), (int(boid.pos.x), int(boid.pos.y)), radius=radius)

    fps = clock.get_fps()
    fpsText = fontObj.render(f"FPS: {fps:.0f}", True, (255, 255, 255))
    screen.blit(fpsText, (15, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
