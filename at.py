import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600  # Default window size
TARGET_RADIUS = 30
FAKE_RADIUS = 25
TARGET_COLOR = (0, 255, 0)  # Green (Correct Target)
FAKE_COLOR = (255, 0, 0)  # Red (Fake Prop)
TEXT_COLOR = (255, 255, 255)
SPAWN_INTERVAL = 1000  # 1 second = 1000ms
FULLSCREEN = False  # Fullscreen toggle state

# Load Background Image (Black Smoke Gradient)
background = pygame.image.load("black_smoke_gradient.jpg")

# Game Variables
score = 0
lives = 5
total_clicks = 0
level = 1
game_over = False
last_spawn_time = pygame.time.get_ticks()
green_targets = []
red_targets = []

# Setup Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fast-Paced Aim Trainer")

# Fonts
font = pygame.font.Font(None, 36)

def spawn_target():
    """Returns a new random position for the green target."""
    return random.randint(TARGET_RADIUS, WIDTH - TARGET_RADIUS), random.randint(TARGET_RADIUS, HEIGHT - TARGET_RADIUS)

def spawn_fake_target():
    """Returns a new random position for the red fake target."""
    return random.randint(FAKE_RADIUS, WIDTH - FAKE_RADIUS), random.randint(FAKE_RADIUS, HEIGHT - FAKE_RADIUS)

def is_hit(mx, my, tx, ty, radius):
    """Check if the mouse click hit the target."""
    return ((mx - tx) ** 2 + (my - ty) ** 2) ** 0.5 < radius

def update_score():
    """Increase score and adjust difficulty by adding more targets."""
    global score, level, green_targets, red_targets
    score += 0.5  # Green target gives +0.5 points
    
    # Increase difficulty: More targets per level
    if score % 5 == 0:
        level += 1  # Increase level every 5 points
        green_targets.append(spawn_target())  # Add more green balls
        red_targets.append(spawn_fake_target())  # Add more red balls

def restart_game():
    """Reset game variables for a fresh start."""
    global score, lives, total_clicks, level, game_over, green_targets, red_targets
    score = 0
    lives = 5
    total_clicks = 0
    level = 1
    game_over = False
    green_targets = [spawn_target()]  # Reset to 1 green target
    red_targets = [spawn_fake_target()]  # Reset to 1 red target

def toggle_fullscreen():
    """Toggle fullscreen mode."""
    global screen, WIDTH, HEIGHT, FULLSCREEN, background
    FULLSCREEN = not FULLSCREEN
    if FULLSCREEN:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        WIDTH, HEIGHT = screen.get_size()  # Get new screen size
    else:
        screen = pygame.display.set_mode((800, 600))  # Return to windowed mode
        WIDTH, HEIGHT = 800, 600  # Reset dimensions
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Resize background

# Start with 1 green and 1 red ball
green_targets.append(spawn_target())
red_targets.append(spawn_fake_target())

# Main Game Loop
running = True
clock = pygame.time.Clock()

while running:
    screen.blit(background, (0, 0))  # Draw the background

    if game_over:
        # Display "Game Over" screen
        game_over_text = font.render(f"Game Over! Final Score: {score:.1f}", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 3, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(2000)  # Show Game Over message for 2 seconds
        restart_game()

    else:
        # Auto-spawn new positions for all targets every 1 second
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time > SPAWN_INTERVAL:
            green_targets = [spawn_target() for _ in range(level)]  # Increase green targets
            red_targets = [spawn_fake_target() for _ in range(level)]  # Increase red targets
            last_spawn_time = current_time  # Reset timer

        # Draw all Green Targets
        for g_x, g_y in green_targets:
            pygame.draw.circle(screen, TARGET_COLOR, (g_x, g_y), TARGET_RADIUS)

        # Draw all Fake Red Targets
        for r_x, r_y in red_targets:
            pygame.draw.circle(screen, FAKE_COLOR, (r_x, r_y), FAKE_RADIUS)

        # Display Score & Accuracy
        accuracy = (score / total_clicks * 100) if total_clicks > 0 else 100
        score_text = font.render(f"Score: {score:.1f} | Accuracy: {accuracy:.2f}% | Level: {level}", True, TEXT_COLOR)
        screen.blit(score_text, (20, 20))

        # Display Lives
        lives_text = font.render(f"Lives: {lives} / 5", True, TEXT_COLOR)
        screen.blit(lives_text, (WIDTH - 180, 20))

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:  # Press 'F' to toggle fullscreen
                toggle_fullscreen()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            total_clicks += 1
            mouse_x, mouse_y = event.pos

            hit_target = False
            for g_x, g_y in green_targets:
                if is_hit(mouse_x, mouse_y, g_x, g_y, TARGET_RADIUS):
                    update_score()  # Increase score but do not remove instantly
                    hit_target = True
                    break  # Only count one hit per click

            if not hit_target:  # If not a green target, check red targets
                for r_x, r_y in red_targets:
                    if is_hit(mouse_x, mouse_y, r_x, r_y, FAKE_RADIUS):
                        lives -= 1  # Clicking a fake prop removes a heart
                        break  # Only deduct once per click

            # Restart when all lives are lost
            if lives <= 0:
                game_over = True

    pygame.display.flip()
    clock.tick(120)  # Fast-paced gameplay

pygame.quit()
