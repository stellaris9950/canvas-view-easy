import pygame

class Square:
    def __init__(self, position, size, speed):
        self.position = pygame.Vector2(position)
        self.size = size
        self.speed = speed
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = False

    def move(self, platforms, canvas_height):
        # Apply gravity
        self.velocity.y += gravity
        new_position = self.position + self.velocity

        # Check collisions with platforms
        self.on_ground = False
        square_rect = pygame.Rect(new_position.x, new_position.y, self.size, self.size)
        for platform in platforms:
            if square_rect.colliderect(platform):
                if self.velocity.y > 0:  # Falling down
                    new_position.y = platform.top - self.size
                    self.velocity.y = 0
                    self.on_ground = True
                break

        # Check if the square is on the ground (canvas bottom edge)
        if new_position.y + self.size > canvas_height:
            new_position.y = canvas_height - self.size
            self.velocity.y = 0
            self.on_ground = True

        # Update square position
        self.position = new_position
        self.position.x = max(0, min(canvas_width - self.size, self.position.x))

    def draw(self, window, offset_x):
        pygame.draw.rect(window, BLUE, (self.position.x - offset_x, self.position.y, self.size, self.size))

# Initialize Pygame
pygame.init()

# Constants
window_width, window_height = 800, 600
canvas_width, canvas_height = 1200, 600
gravity = 0.75
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set up the window
window = pygame.display.set_mode((window_width, window_height))

# Create a square
square = Square((300, 300), 50, 10)

# Platforms
platforms = [
    pygame.Rect(200, 200, 200, 50),
    pygame.Rect(600, 400, 300, 50),
    # Removed ground platform
]

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_w and square.on_ground:
        #         square.velocity.y = -20  # Jump strength

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        square.position.x -= square.speed
    if keys[pygame.K_d]:
        square.position.x += square.speed
    if keys[pygame.K_w] and square.on_ground:
        square.velocity.y = -20  # Jump strength


    # Move and draw the square
    square.move(platforms, canvas_height)
    offset_x = min(max(square.position.x - window_width // 2, 0), canvas_width - window_width)

    # Draw
    window.fill(WHITE)
    for platform in platforms:
        pygame.draw.rect(window, RED, (platform.x - offset_x, platform.y, platform.width, platform.height))
    square.draw(window, offset_x)


    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
