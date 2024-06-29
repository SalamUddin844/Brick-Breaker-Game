import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gray = (200, 200, 200)

# Game settings
paddle_width = 100
paddle_height = 10
paddle_x = screen_width // 2 - paddle_width // 2
paddle_y = screen_height - paddle_height - 20
paddle_velocity = 8

ball_radius = 10
ball_x = screen_width // 2
ball_y = screen_height // 2
ball_velocity_x = random.choice([-4, -3, 3, 4])
ball_velocity_y = -4

brick_width = 60
brick_height = 20
brick_gap = 5
brick_rows = 5
brick_cols = screen_width // (brick_width + brick_gap)
bricks = []

# Font settings
font = pygame.font.SysFont("comicsansms", 35)

# Game variables
score = 0
lives = 3
running = True
clock = pygame.time.Clock()

# Create bricks
for row in range(brick_rows):
    for col in range(brick_cols):
        brick_x = col * (brick_width + brick_gap) + brick_gap
        brick_y = row * (brick_height + brick_gap) + brick_gap + 50
        bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))

# Function to draw the paddle
def draw_paddle(x, y):
    pygame.draw.rect(screen, blue, (x, y, paddle_width, paddle_height))

# Function to draw the ball
def draw_ball(x, y):
    pygame.draw.circle(screen, red, (x, y), ball_radius)

# Function to draw bricks
def draw_bricks(bricks):
    for brick in bricks:
        pygame.draw.rect(screen, green, brick)

# Function to display text
def display_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Main game loop
while running:
    screen.fill(white)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_velocity
    if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width:
        paddle_x += paddle_velocity
    
    # Update ball position
    ball_x += ball_velocity_x
    ball_y += ball_velocity_y
    
    # Collisions with walls
    if ball_x <= ball_radius or ball_x >= screen_width - ball_radius:
        ball_velocity_x = -ball_velocity_x
    if ball_y <= ball_radius:
        ball_velocity_y = -ball_velocity_y
    
    # Collision with paddle
    if ball_y >= paddle_y - ball_radius and paddle_x <= ball_x <= paddle_x + paddle_width and ball_velocity_y > 0:
        ball_velocity_y = -ball_velocity_y
    
    # Collision with bricks
    for brick in bricks:
        if brick.colliderect(pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, 2 * ball_radius, 2 * ball_radius)):
            bricks.remove(brick)
            ball_velocity_y = -ball_velocity_y
            score += 1
            break
    
    # Game over if ball falls below paddle
    if ball_y >= screen_height:
        lives -= 1
        if lives <= 0:
            running = False
        ball_x = screen_width // 2
        ball_y = screen_height // 2
        ball_velocity_x = random.choice([-4, -3, 3, 4])
        ball_velocity_y = -4
    
    # Draw game elements
    draw_paddle(paddle_x, paddle_y)
    draw_ball(ball_x, ball_y)
    draw_bricks(bricks)
    display_text(f"Score: {score}", black, 10, 10)
    display_text(f"Lives: {lives}", black, screen_width - 120, 10)
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
