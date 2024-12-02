import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (0, 128, 255)
PLATFORM_COLOR = (0, 255, 0)
STAR_COLOR = (255, 255, 0)
GREEN = (0,128,0)
RED = (255,0,0)

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game")
clock = pygame.time.Clock()

# Player Setup
player_size = (50, 50)
player_pos = [WIDTH // 2, HEIGHT - 100]
player_speed = 5
player_jump = -15
player_velocity_y = 0
is_jumping = False
gravity = 0.5

# Platform Setup
platforms = [pygame.Rect(100, 500, 600, 20), pygame.Rect(300, 350, 200, 20), pygame.Rect(50, 200, 200, 20), pygame.Rect(500, 200, 200, 20)]
star = pygame.Rect(380, 50, 30, 30)

def reset_game():
    global player_pos, player_velocity_y, is_jumping, running
    player_pos = [WIDTH // 2, HEIGHT - 100]
    player_velocity_y = 0
    is_jumping = False
    running = True

# Main Game Loop Function
def main_game_loop():
    global running, player_velocity_y, is_jumping
    running = True
    while running:
        clock.tick(FPS)
        screen.fill(WHITE)
        
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT]:
            player_pos[0] += player_speed
        
        # Jumping
        if not is_jumping and keys[pygame.K_SPACE]:
            player_velocity_y = player_jump
            is_jumping = True
        
        # Apply Gravity
        player_velocity_y += gravity
        player_pos[1] += player_velocity_y
        
        # Collisions with Platforms
        player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size[0], player_size[1])
        for platform in platforms:
            if player_rect.colliderect(platform) and player_velocity_y > 0:
                player_pos[1] = platform.top - player_size[1]
                player_velocity_y = 0
                is_jumping = False
        
        # Collisions with Star
        if player_rect.colliderect(star):
            game_finished_screen()

        # Prevent Player from Going Off-Screen
        if player_pos[0] < 0:
            player_pos[0] = 0
        if player_pos[0] > WIDTH - player_size[0]:
            player_pos[0] = WIDTH - player_size[0]
        if player_pos[1] > HEIGHT - player_size[1]:
            # Trigger Game Over
            running = False

        # Draw Player, Platforms, and Star
        pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
        for platform in platforms:
            pygame.draw.rect(screen, PLATFORM_COLOR, platform)
        pygame.draw.rect(screen, STAR_COLOR, star)

        # Update Screen
        pygame.display.flip()

# Game Over Screen Function
def game_over_screen():
    while True:
        screen.fill(BLACK)
        font = pygame.font.Font(None, 74)
        game_over_text = font.render("Game Over!", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        restart_text = font.render("Press R to Restart", True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.flip()

        # Event Handling for Restart
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            reset_game()
            return

# Game Finished Screen Function
def game_finished_screen():
    while True:
        screen.fill(BLACK)
        font = pygame.font.Font(None, 74)
        finished_text = font.render("You Win!", True, GREEN)
        screen.blit(finished_text, (WIDTH // 2 - finished_text.get_width() // 2, HEIGHT // 2 - finished_text.get_height() // 2))
        restart_text = font.render("Press R to Restart", True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.flip()

        # Event Handling for Restart
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            reset_game()
            return

# Start the Game
while True:
    main_game_loop()
    game_over_screen()
