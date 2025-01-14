import pygame
import random
import sys
from pygame.locals import *

# Global Variables for the game
window_width = 600
window_height = 499

window = pygame.display.set_mode((window_width, window_height))
elevation = window_height * 0.8
game_images = {}
framepersecond = 32
pipeimage = 'images/pipe.png'
background_image = 'images/background.jpg'
birdplayer_image = 'images/bird.png'
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
    if vertical > elevation - 25 or vertical < 0:  # Bird hits top or bottom
        return True
    for pipe in up_pipes:
        if (vertical < game_images['pipeimage'][0].get_height() + pipe['y'] and
                abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width()):
            return True
    for pipe in down_pipes:
        if (vertical + game_images['flappybird'].get_height() > pipe['y'] and
                abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width()):
            return True
    return False

def flappygame():
    """Main game loop."""
    your_score = 0
    horizontal = int(window_width / 5)
    vertical = int(window_width / 2)
    bird_velocity_x = 2  # Horizontal speed of the bird
    bird_velocity_y = -9  # Bird's vertical velocity
    bird_Max_Vel_Y = 10
    bird_Min_Vel_Y = -8
    birdAccY = 1
    bird_flap_velocity = -8
    bird_flapped = False
    time_since_pipe_update = 0

    pipes = createPipe()
    up_pipes = [pipes[0]]
    down_pipes = [pipes[1]]

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    bird_velocity_y = bird_flap_velocity
                    bird_flapped = True

        # Update bird's vertical position
        if bird_velocity_y < bird_Max_Vel_Y and not bird_flapped:
            bird_velocity_y += birdAccY
        if bird_flapped:
            bird_flapped = False
        vertical = vertical + min(bird_velocity_y, elevation - vertical - game_images['flappybird'].get_height())

        # Update bird's horizontal position
        horizontal += bird_velocity_x

        # Check if the bird hits the left or right wall
        if horizontal <= 0:  # Left wall collision
            horizontal = 0
            bird_velocity_x = -bird_velocity_x
        elif horizontal + game_images['flappybird'].get_width() >= window_width:  # Right wall collision
            horizontal = window_width - game_images['flappybird'].get_width()
            bird_velocity_x = -bird_velocity_x

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
        window.blit(game_images['flappybird'], (horizontal, vertical))

        pygame.display.update()

# Main program
if __name__ == "__main__":
    pygame.init()
    framepersecond_clock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird Game')

    game_images['flappybird'] = pygame.image.load(birdplayer_image).convert_alpha()
    game_images['sea_level'] = pygame.image.load(sealevel_image).convert_alpha()
    game_images['background'] = pygame.image.load(background_image).convert_alpha()
    game_images['pipeimage'] = (
        pygame.transform.rotate(pygame.image.load(pipeimage).convert_alpha(), 180),
        pygame.image.load(pipeimage).convert_alpha()
    )

    print("WELCOME TO THE FLAPPY BIRD GAME")
    print("Press space or enter to start the game")

    while True:
        horizontal = int(window_width / 5)
        vertical = int((window_height - game_images['flappybird'].get_height()) / 2)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    flappygame()
                else:
                    window.blit(game_images['background'], (0, 0))
                    window.blit(game_images['flappybird'], (horizontal, vertical))
                    window.blit(game_images['sea_level'], (0, elevation))
                    pygame.display.update()
                    framepersecond_clock.tick(framepersecond)