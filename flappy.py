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
pipeimage = 'images/pipe.png'
background_image = 'images/background.jpg'
birdplayer_image1 = 'images/bird1.png'  # Bird 1 image
birdplayer_image2 = 'images/bird2.png'  # Bird 2 image
sealevel_image = 'images/base.jfif'

def createPipe():
    """Creates stationary pipes with random gaps."""
    offset = window_height / 3
    pipeHeight = game_images['pipeimage'][0].get_height()
    y2 = offset + random.randrange(0, int(window_height - game_images['sea_level'].get_height() - 1.2 * offset))
    y1 = pipeHeight - y2 + offset
    return [
        {'x': window_width / 2, 'y': -y1},  # Upper Pipe
        {'x': window_width / 2, 'y': y2}   # Lower Pipe
    ]

def isGameOver(horizontal, vertical, up_pipes, down_pipes):
    """Check game over conditions."""
    if vertical >= elevation - game_images['flappybird1'].get_height():  # Bird hits the ground
        return True

    for pipe in up_pipes:
        if (vertical < game_images['pipeimage'][0].get_height() + pipe['y'] and
                abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width()):
            return True
    for pipe in down_pipes:
        if (vertical + game_images['flappybird1'].get_height() > pipe['y'] and
                abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width()):
            return True

    return False

def flappygame():
    """Main game loop for 2 players."""
    global high_score_p1, high_score_p2  # Use global high scores
    score_p1 = 0
    score_p2 = 0

    # Bird 1 (Player 1) starts from the left wall
    horizontal_p1 = 0
    vertical_p1 = int(window_width / 2)
    bird_velocity_x_p1 = 2
    bird_velocity_y_p1 = -9
    bird_flap_velocity_p1 = -8
    bird_flapped_p1 = False

    # Bird 2 (Player 2) starts from the right wall
    horizontal_p2 = window_width - game_images['flappybird2'].get_width()
    vertical_p2 = int(window_width / 2)
    bird_velocity_x_p2 = -2  # Starts moving left
    bird_velocity_y_p2 = -9
    bird_flap_velocity_p2 = -8
    bird_flapped_p2 = False

    pipes = createPipe()
    up_pipes = [pipes[0]]
    down_pipes = [pipes[1]]

    time_since_pipe_update = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:  # Player 1 controls
                    if vertical_p1 > 0:
                        bird_velocity_y_p1 = bird_flap_velocity_p1
                        bird_flapped_p1 = True
                if event.key == K_w:  # Player 2 controls
                    if vertical_p2 > 0:
                        bird_velocity_y_p2 = bird_flap_velocity_p2
                        bird_flapped_p2 = True

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
        elif horizontal_p1 + game_images['flappybird1'].get_width() >= window_width:  # Bird 1 hits right wall
            horizontal_p1 = window_width - game_images['flappybird1'].get_width()
            bird_velocity_x_p1 = -bird_velocity_x_p1

        if horizontal_p2 <= 0:  # Bird 2 hits left wall
            horizontal_p2 = 0
            bird_velocity_x_p2 = -bird_velocity_x_p2
        elif horizontal_p2 + game_images['flappybird2'].get_width() >= window_width:  # Bird 2 hits right wall
            horizontal_p2 = window_width - game_images['flappybird2'].get_width()
            bird_velocity_x_p2 = -bird_velocity_x_p2

        # Check game over conditions
        if isGameOver(horizontal_p1, vertical_p1, up_pipes, down_pipes):
            if score_p1 > high_score_p1:
                high_score_p1 = score_p1
            print("Player 1 Game Over!")
            return
        if isGameOver(horizontal_p2, vertical_p2, up_pipes, down_pipes):
            if score_p2 > high_score_p2:
                high_score_p2 = score_p2
            print("Player 2 Game Over!")
            return

        # Increment scores for passing pipes
        player1_mid_pos = horizontal_p1 + game_images['flappybird1'].get_width() / 2
        player2_mid_pos = horizontal_p2 + game_images['flappybird2'].get_width() / 2
        for pipe in up_pipes:
            pipe_mid_pos = pipe['x'] + game_images['pipeimage'][0].get_width() / 2
            if pipe_mid_pos <= player1_mid_pos < pipe_mid_pos + 4:
                score_p1 += 1
            if pipe_mid_pos <= player2_mid_pos < pipe_mid_pos + 4:
                score_p2 += 1

        # Reset pipes every 5 seconds
        time_since_pipe_update += framepersecond_clock.tick(framepersecond) / 1000.0
        if time_since_pipe_update >= 5:
            time_since_pipe_update = 0
            pipes = createPipe()
            up_pipes = [pipes[0]]
            down_pipes = [pipes[1]]

        # Render game
        window.blit(game_images['background'], (0, 0))
        for pipe in up_pipes:
            window.blit(game_images['pipeimage'][0], (pipe['x'], pipe['y']))
        for pipe in down_pipes:
            window.blit(game_images['pipeimage'][1], (pipe['x'], pipe['y']))

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

# Main program
if __name__ == "__main__":
    pygame.init()
    framepersecond_clock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird Game - 2 Players')

    game_images['flappybird1'] = pygame.image.load(birdplayer_image1).convert_alpha()
    game_images['flappybird2'] = pygame.image.load(birdplayer_image2).convert_alpha()
    game_images['sea_level'] = pygame.image.load(sealevel_image).convert_alpha()
    game_images['background'] = pygame.image.load(background_image).convert_alpha()
    game_images['pipeimage'] = (
        pygame.transform.rotate(pygame.image.load(pipeimage).convert_alpha(), 180),
        pygame.image.load(pipeimage).convert_alpha()
    )

    print("WELCOME TO FLAPPY BIRD - 2 PLAYERS")
    print("Player 1: SPACE to flap | Player 2: W to flap")
    print("Press SPACE or W to start!")

    while True:
        flappygame()
