import pygame
import random
import sys

pygame.init()

# Window setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Matcha Catcher 🍵")

# Colors
MATCHA_GREEN = (144, 238, 144)
WHITE = (255, 255, 255)
BROWN = (101, 67, 33)
BLACK = (0, 0, 0)

# Font and clock
font = pygame.font.SysFont("Comic Sans MS", 28)
clock = pygame.time.Clock()

# Player (tray)
player_width, player_height = 80, 20
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 6

# Cup
cup_width, cup_height = 30, 30
cup_x = random.randint(0, WIDTH - cup_width)
cup_y = 0
cup_speed = 3
squish = False
squish_timer = 0

# Score
score = 0
misses = 0
max_misses = 5

# Game loop
running = True
while running:
    screen.fill(MATCHA_GREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # Draw player (tray)
    pygame.draw.rect(screen, BROWN, (player_x, player_y, player_width, player_height), border_radius=10)

    # Animate cup fall
    if not squish:
        cup_y += cup_speed
        pygame.draw.ellipse(screen, WHITE, (cup_x, cup_y, cup_width, cup_height))
    else:
        # Cute squish effect
        pygame.draw.ellipse(screen, WHITE, (cup_x, cup_y, cup_width + 10, cup_height - 10))
        squish_timer += 1
        if squish_timer > 5:
            squish = False
            squish_timer = 0
            cup_x = random.randint(0, WIDTH - cup_width)
            cup_y = 0

    # Collision detection
    if (not squish and
        cup_y + cup_height >= player_y and
        player_x < cup_x + cup_width and
        cup_x < player_x + player_width):
        score += 1
        squish = True

    # Missed
    if cup_y > HEIGHT:
        misses += 1
        cup_x = random.randint(0, WIDTH - cup_width)
        cup_y = 0

    # Score display
    score_text = font.render(f"Score: {score}", True, BLACK)
    miss_text = font.render(f"Missed: {misses}/{max_misses}", True, (255, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(miss_text, (10, 40))

    # Game Over
    if misses >= max_misses:
        over_text = font.render("Game Over 💔", True, BLACK)
        screen.blit(over_text, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
