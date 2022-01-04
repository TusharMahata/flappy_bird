import pygame
import sys
import random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 540))
    screen.blit(floor_surface, (floor_x_pos + 500, 540))


def create_pipe():
    pipe_y_pos = random.choice(pipe_height)
    botom_pipe = pipe_surface.get_rect(midtop=(600, pipe_y_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(600, pipe_y_pos - 300))

    return botom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 4

    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 545:
        return False
    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 4, 1.5)
    return new_bird


def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display():
    score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(250, 20))
    screen.blit(score_surface, score_rect)


def change_bird():
    bird_upflap = pygame.image.load('flappy-bird-assets-master/sprites/redbird-upflap.png').convert_alpha()
    bird_midflap = pygame.image.load('flappy-bird-assets-master/sprites/redbird-midflap.png').convert_alpha()
    bird_downflap = pygame.image.load('flappy-bird-assets-master/sprites/redbird-downflap.png').convert_alpha()


pygame.init()
screen = pygame.display.set_mode((500, 600))
clock = pygame.time.Clock()
game_font = pygame.font.SysFont('Roboto', 35)

bg_surface = pygame.image.load('flappy-bird-assets-master/sprites/background-day.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (500, 600))

bgnignt_surface = pygame.image.load('flappy-bird-assets-master/sprites/background-night.png').convert()
bgnignt_surface = pygame.transform.scale(bgnignt_surface, (500, 600))

floor_surface = pygame.image.load('flappy-bird-assets-master/sprites/base.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (500, 100))
floor_x_pos = 0
bg_x_pos = 0
game_active = True

bird_upflap = pygame.image.load('flappy-bird-assets-master/sprites/bluebird-upflap.png').convert_alpha()
bird_midflap = pygame.image.load('flappy-bird-assets-master/sprites/bluebird-midflap.png').convert_alpha()
bird_downflap = pygame.image.load('flappy-bird-assets-master/sprites/bluebird-downflap.png').convert_alpha()
bird_list = [bird_upflap, bird_midflap, bird_downflap]
bird_index = 0
bird_surface = bird_list[bird_index]
BIRD_FLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRD_FLAP, 100)

# bird_surface = pygame.transform.scale2x(bg_surface)
bird_rect = bird_surface.get_rect(center=(100, 250))
pipe_surface = pygame.image.load('flappy-bird-assets-master/sprites/pipe-green.png').convert_alpha()
# pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 550, 480, 340, 600, 440, 500, 380]

gravity = .15
bird_movement = 0
score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 5
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and game_active is False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 250)
                bird_movement = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            # print(pipe_list)

        if event.type == BIRD_FLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    # bg_x_pos -= .0001
    if score < 20 or score > 50:
        screen.blit(bg_surface, (0, 0))
        pipe_surface = pygame.image.load('flappy-bird-assets-master/sprites/pipe-green.png')

    else:
        screen.blit(bgnignt_surface, (0, 0))
        pipe_surface = pygame.image.load('flappy-bird-assets-master/sprites/pipe-red.png')
        change_bird()

    if game_active:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotate_birds = rotate_bird(bird_surface)
        screen.blit(rotate_birds, bird_rect)
        game_active = check_collision(pipe_list)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01
        score_display()

    floor_x_pos -= 4
    # screen.blit(floor_surface, (floor_x_pos, 540))
    draw_floor()
    if floor_x_pos <= -500:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)
