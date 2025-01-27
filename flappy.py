import pygame
import random
import sys
from pygame.locals import *

# Global Variables for the game
window_width = 600
window_height = 499
high_score_p1 = 0  # Player 1 high score
high_score_p2 = 0  # Player 2 high score

window = pygame.display.set_mode((window_width, window_height))
elevation = window_height * 0.8
game_images = {}
framepersecond = 32
pipeimage = 'images/bamboo.png'
background_image = 'images/sky.png'
start_image = 'images/start_background.png'
birdplayer_image1 = 'images/bird1.png'  # Bird 1 image
birdplayer_image2 = 'images/bird2.png'  # Bird 2 image
sealevel_image = 'images/base.jpg'

def createPipes():
    """Creates pipes with random horizontal and vertical positions."""
    offset = window_height / 2.5
    pipeHeight = game_images['pipeimage'][0].get_height()
    pipes = []
    max_spacing = window_width / 4  # Maximum spacing between pipes
    min_spacing = window_width / 6  # Minimum spacing between pipes

    x_position = window_width / 10  # Starting x-position

    for i in range(3):  # Create 3 pipes
        y2 = offset + random.randrange(0, int(window_height - game_images['sea_level'].get_height() - 1.2 * offset))
        y1 = pipeHeight - y2 + offset

        # Randomize horizontal spacing between pipes
        x_position += random.randint(int(min_spacing), int(max_spacing))

        pipes.append([
            {'x': x_position, 'y': -y1},  # Upper Pipe
            {'x': x_position, 'y': y2}   # Lower Pipe
        ])
    return pipes

def isGameOver(horizontal, vertical, pipes):
    """Check game over conditions."""

    # 1. Bird hits the ground
    if vertical >= elevation - game_images['flappybird1'].get_height():  
        return True

    # 2. Bird hits upper wall
    if vertical <= 0:
        return True
    
    for pipe_pair in pipes:
        upper_pipe, lower_pipe = pipe_pair

        # 3. Bird hits upper pipe
        if (vertical < game_images['pipeimage'][0].get_height() - 5 + upper_pipe['y'] and
                abs(horizontal - upper_pipe['x']) < game_images['pipeimage'][0].get_width() - 25):
            return True
        
        # 4. Bird hits lower pipe
        if (vertical + game_images['flappybird1'].get_height() - 5 > lower_pipe['y'] and
                abs(horizontal - lower_pipe['x']) < game_images['pipeimage'][0].get_width() - 25):
            return True

    return False

def flappygame():
    """Main game loop"""
    global high_score_p1, high_score_p2  # Use global high scores
    score_p1 = 0
    score_p2 = 0

    # Bird 1 (Player 1) starts from the left wall
    horizontal_p1 = 0
    vertical_p1 = int(window_width / 2)
    bird_velocity_x_p1 = 4  # Increased horizontal speed
    bird_velocity_y_p1 = -9
    bird_flap_velocity_p1 = -8
    bird_flapped_p1 = False

    # Bird 2 (Player 2) starts from the right wall
    horizontal_p2 = window_width - game_images['flappybird2'].get_width()
    vertical_p2 = int(window_width / 2)
    bird_velocity_x_p2 = -4  # Increased horizontal speed (moving left)
    bird_velocity_y_p2 = -9
    bird_flap_velocity_p2 = -8
    bird_flapped_p2 = False

    pipes = createPipes()
    time_since_pipe_update = 0

    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_r:
                start()
            
            if game_over:  # If game over, wait for button to restart
                if event.type == KEYDOWN and event.key == K_SPACE:
                    flappygame()  # Restart the game
                continue

            # Normal gameplay inputs
            if event.type == KEYDOWN:
                if event.key == K_SPACE:  # Player 1 controls
                    bird_velocity_y_p1 = bird_flap_velocity_p1
                    bird_flapped_p1 = True
                if event.key == K_w:  # Player 2 controls
                    bird_velocity_y_p2 = bird_flap_velocity_p2
                    bird_flapped_p2 = True

            # Left-right inputs
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if(pos[0] < window_width / 2):
                    bird_velocity_y_p1 = bird_flap_velocity_p1
                    bird_flapped_p1 = True
                else:
                    bird_velocity_y_p2 = bird_flap_velocity_p2
                    bird_flapped_p2 = True

        if game_over:  # Skip game updates if game is over
            continue

        # Update Bird 1 (Player 1)
        if bird_velocity_y_p1 < 10 and not bird_flapped_p1:
            bird_velocity_y_p1 += 1
        if bird_flapped_p1:
            bird_flapped_p1 = False
        vertical_p1 = vertical_p1 + min(bird_velocity_y_p1, elevation - vertical_p1 - game_images['flappybird1'].get_height())
        horizontal_p1 += bird_velocity_x_p1

        # Update Bird 2 (Player 2)
        if bird_velocity_y_p2 < 10 and not bird_flapped_p2:
            bird_velocity_y_p2 += 1
        if bird_flapped_p2:
            bird_flapped_p2 = False
        vertical_p2 = vertical_p2 + min(bird_velocity_y_p2, elevation - vertical_p2 - game_images['flappybird2'].get_height())
        horizontal_p2 += bird_velocity_x_p2

        # Handle wall collisions
        if horizontal_p1 <= 0:  # Bird 1 hits left wall
            horizontal_p1 = 0
            bird_velocity_x_p1 = -bird_velocity_x_p1
            game_images['flappybird1'] = pygame.image.load('images/bird1.png').convert_alpha()
        elif horizontal_p1 + game_images['flappybird1'].get_width() >= window_width:  # Bird 1 hits right wall
            horizontal_p1 = window_width - game_images['flappybird1'].get_width()
            bird_velocity_x_p1 = -bird_velocity_x_p1
            game_images['flappybird1'] = pygame.image.load('images/bird1-flipped.png').convert_alpha()

        if horizontal_p2 <= 0:  # Bird 2 hits left wall
            horizontal_p2 = 0
            bird_velocity_x_p2 = -bird_velocity_x_p2
            game_images['flappybird2'] = pygame.image.load('images/bird2-flipped.png').convert_alpha()
        elif horizontal_p2 + game_images['flappybird2'].get_width() >= window_width:  # Bird 2 hits right wall
            horizontal_p2 = window_width - game_images['flappybird2'].get_width()
            bird_velocity_x_p2 = -bird_velocity_x_p2
            game_images['flappybird2'] = pygame.image.load('images/bird2.png').convert_alpha()

        # Check game over conditions
        if isGameOver(horizontal_p1, vertical_p1, pipes) or isGameOver(horizontal_p2, vertical_p2, pipes):
            game_over = True

            # Update high scores
            if score_p1 > high_score_p1:
                high_score_p1 = score_p1
            if score_p2 > high_score_p2:
                high_score_p2 = score_p2

            # Calculate winner
            if isGameOver(horizontal_p1, vertical_p1, pipes):
                print("Player 2 Wins")
                winner = "Player 2 Wins"
            else:
                print("Player 1 Wins")
                winner = "Player 1 Wins"

            game_over_surface = font_medium.render("GAME OVER", True, (255, 128, 0))
            win_surface = font_large.render(winner, True, (255, 0, 0))
            restart_surface = font_small.render("Press button to Restart", True, (255, 255, 255))

            game_over_rect = game_over_surface.get_rect(center=(window_width / 2, window_height / 5))
            win_rect = win_surface.get_rect(center=(window_width - 300, window_height - 300))
            restart_rect = restart_surface.get_rect(center=(window_width / 2, window_height - 175))

            window.blit(game_over_surface, game_over_rect)
            window.blit(win_surface, win_rect)
            window.blit(restart_surface, restart_rect)
            
            pygame.display.update()

            # Reset bird images
            game_images['flappybird1'] = pygame.image.load('images/bird1.png').convert_alpha()
            game_images['flappybird2'] = pygame.image.load('images/bird2.png').convert_alpha()
            continue

        # Increment scores for passing pipes
        player1_mid_pos = horizontal_p1 + game_images['flappybird1'].get_width() / 2
        player2_mid_pos = horizontal_p2 + game_images['flappybird2'].get_width() / 2
        for pipe_pair in pipes:
            upper_pipe, lower_pipe = pipe_pair
            pipe_mid_pos = upper_pipe['x'] + game_images['pipeimage'][0].get_width() / 2
            if pipe_mid_pos <= player1_mid_pos < pipe_mid_pos + 4:
                score_p1 += 1
            if pipe_mid_pos <= player2_mid_pos < pipe_mid_pos + 4:
                score_p2 += 1

        # Reset pipes every 5 seconds
        time_since_pipe_update += framepersecond_clock.tick(framepersecond) / 1000.0
        if time_since_pipe_update >= 5:
            time_since_pipe_update = 0
            pipes = createPipes()

        # Render game
        window.blit(game_images['background'], (0, 0))
        for pipe_pair in pipes:
            upper_pipe, lower_pipe = pipe_pair
            window.blit(game_images['pipeimage'][0], (upper_pipe['x'], upper_pipe['y']))
            window.blit(game_images['pipeimage'][1], (lower_pipe['x'], lower_pipe['y']))

        window.blit(game_images['sea_level'], (0, elevation))
        window.blit(game_images['flappybird1'], (horizontal_p1, vertical_p1))
        window.blit(game_images['flappybird2'], (horizontal_p2, vertical_p2))

        # Display scores and high scores
        font = pygame.font.Font(None, 36)
        score_p1_surface = font.render(f"P1 Score: {score_p1}", True, (255, 255, 255))
        high_score_p1_surface = font.render(f"P1 High Score: {high_score_p1}", True, (255, 255, 255))
        score_p2_surface = font.render(f"P2 Score: {score_p2}", True, (255, 255, 255))
        high_score_p2_surface = font.render(f"P2 High Score: {high_score_p2}", True, (255, 255, 255))

        window.blit(score_p1_surface, (10, 10))
        window.blit(high_score_p1_surface, (10, window_height - 40))
        window.blit(score_p2_surface, (window_width - 200, 10))
        window.blit(high_score_p2_surface, (window_width - 200, window_height - 40))

        pygame.display.update()

def start():
    window.blit(game_images['start_image'], (0, 0))
    window.blit(game_images['sea_level'], (0, elevation))

    game_images['flappybird1'] = pygame.image.load(birdplayer_image1).convert_alpha()
    game_images['flappybird2'] = pygame.image.load(birdplayer_image2).convert_alpha()
    window.blit(game_images['flappybird1'], (40, 435))
    window.blit(game_images['flappybird2'], (505, 437.5))
    
    title_surface = font_large.render("Flappy Bird 2P", True, (255, 255, 255))
    title_rect = title_surface.get_rect(center=(window_width / 2, window_height / 2))
    window.blit(title_surface, title_rect)

    start_surface = font_medium.render("Press button to start", True, (255, 255, 255))
    start_rect = start_surface.get_rect(center=(window_width / 2, window_height - 50))
    window.blit(start_surface, start_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                    flappygame()

    
  
# Main program
if __name__ == "__main__":
    pygame.init()
    framepersecond_clock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird Game - 2 Players')

    game_images['flappybird1'] = pygame.image.load(birdplayer_image1).convert_alpha()
    game_images['flappybird2'] = pygame.image.load(birdplayer_image2).convert_alpha()
    game_images['sea_level'] = pygame.image.load(sealevel_image).convert_alpha()
    game_images['background'] = pygame.image.load(background_image).convert_alpha()
    game_images['start_image'] = pygame.image.load(start_image).convert_alpha()
    game_images['pipeimage'] = (
        pygame.transform.rotate(pygame.image.load(pipeimage).convert_alpha(), 180),
        pygame.image.load(pipeimage).convert_alpha()
    )

    # Initialize fonts
    font_large = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 36)

    print("FLAPPY BIRD - 2 PLAYERS")
    print("Player 1: SPACE to flap | Player 2: W to flap")
    print("Press SPACE or W to start!")

    start()
