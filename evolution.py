import sys
import pygame
import math
import random

# Window dimensions
w, h = 1200, 800
pygame.init()
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Gooblet Evolution")
clock = pygame.time.Clock()
targetFps = 60

fontObj = pygame.font.SysFont('Arial', 32, bold=True)

Gooblets = []
Gamount = 3
Debug = False

# Water and threshold parameters
waterPos = pygame.Vector2(300, 400)
waterRadius = 200
thirstThreshold = 35


class Gooblet:
    def __init__(self):
        self.size = 12
        self.normalSearchR = 160
        self.thirstySearchR = self.normalSearchR + 60  # Expanded search radius when thirsty
        self.searchR = self.normalSearchR

        self.normalSpeed = 175
        self.thirstySpeed = 210  # A tiny bit faster when thirsty
        self.speed = self.normalSpeed

        self.pos = pygame.Vector2(900, 400)
        self.color = (255, 255, 255)
        self.target = pygame.Vector2(0, 0)
        self.maxThirst = 100.0
        self.thirst = self.maxThirst
        self.waterFound = False
        self.pauseTimer = 0
        self.findTarget()

    def findTarget(self):
        # Dynamically adjust search radius and speed based on thirst state
        if self.thirst <= thirstThreshold:
            self.searchR = self.thirstySearchR
            self.speed = self.thirstySpeed

            # Check if the search circle and water circle are colliding (distance <= sum of radii)
            if (self.pos - waterPos).length() <= (self.searchR + waterRadius):
                self.waterFound = True
        else:
            self.searchR = self.normalSearchR
            self.speed = self.normalSpeed

        if not self.waterFound:
            # Keep wandering randomly using the current searchR
            temp = math.radians(random.randint(0, 360))
            self.target.x = self.pos.x + math.cos(temp) * self.searchR
            self.target.y = self.pos.y + math.sin(temp) * self.searchR
            if self.target.x <= 0 or self.target.x >= w or self.target.y >= h or self.target.y <= 0:
                self.findTarget()
            elif (waterPos - self.target).length() <= (1 + waterRadius):
                self.findTarget()
        else:
            # Water is in sight, target the water directly
            angle_radians = math.atan2((waterPos.y - self.pos.y), (waterPos.x - self.pos.x))
            self.target.x = self.pos.x + math.cos(angle_radians) * self.searchR
            self.target.y = self.pos.y + math.sin(angle_radians) * self.searchR

    def update(self, dt):
        if self.pauseTimer > 0:
            self.pauseTimer -= dt
            return

        # Move toward the target
        direction = self.target - self.pos
        distance = direction.length()

        if distance > 5:
            direction.normalize_ip()
            self.pos += direction * self.speed * dt
        else:
            # Reached target: tiny pause for wandering, then pick new target
            self.pauseTimer = 0.25
            self.findTarget()

        self.thirst -= 6 * dt

        # Check if it has reached the water to drink
        if self.waterFound and (self.pos - waterPos).length() <= (self.size + waterRadius):
            self.thirst = self.maxThirst
            self.waterFound = False
            self.searchR = self.normalSearchR  # Reset search radius back to normal
            self.speed = self.normalSpeed  # Reset speed back to normal
            self.pauseTimer = 1.25  # Resting/drinking pause at the water
            self.findTarget()


# Initialize Gooblets
for i in range(Gamount):
    Gooblets.append(Gooblet())

running = True
while running:
    deltaTime = clock.tick(targetFps) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Filter out dead Gooblets
    Gooblets = [gooblet for gooblet in Gooblets if gooblet.thirst > 0]

    # Update logic
    for gooblet in Gooblets:
        gooblet.update(deltaTime)

    # Render logic
    screen.fill((3, 22, 38))

    # Draw water source
    pygame.draw.circle(screen, (45, 110, 214), waterPos, waterRadius, width=0)

    for gooblet in Gooblets:
        if Debug:
            # Draw search radius circle (dynamically grows when thirsty)
            pygame.draw.circle(screen, (50, 50, 50), gooblet.pos, gooblet.searchR, width=1)
            # Draw target dot
            pygame.draw.circle(screen, (255, 0, 0), gooblet.target, 5, width=0)
        # Draw Gooblet body
        pygame.draw.circle(screen, gooblet.color, gooblet.pos, gooblet.size, width=0)

        # Thirst bar
        barWidth = 36
        barHeight = 5
        barX = gooblet.pos.x - (barWidth / 2)
        barY = gooblet.pos.y - gooblet.size - 14

        pct = max(0.0, gooblet.thirst / gooblet.maxThirst)
        fillWidth = barWidth * pct

        pygame.draw.rect(screen, (20, 30, 40), (barX, barY, barWidth, barHeight))
        pygame.draw.rect(screen, (0, 150, 255) if gooblet.thirst > thirstThreshold else (189, 6, 36), (barX, barY, fillWidth, barHeight))

    # Display FPS
    fps = clock.get_fps()
    fpsText = fontObj.render(f"FPS: {fps:.0f}", True, (255, 255, 255))
    screen.blit(fpsText, (15, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
