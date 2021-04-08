import pygame
# from tensorflow import constant
from Pipe import Pipe
from Player import Player
from Button import Button
import random
import numpy as np
import pickle

pygame.init()

# initialize
s_width = 900
s_height = 600
window_size = (s_width, s_height)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("My Flappy Bird")
clock = pygame.time.Clock()

# config
fps = 50

# colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)

# pipes
pipes = []
p_width = 100
p_gap = 150  # gap between upper and lower pipe
p_space = 250  # space between pairs of pipes
p_vel = 4
first_pipe_x = 650
max_h = 400
min_h = 200
while first_pipe_x < s_width:
    pipes.append(Pipe(first_pipe_x, random.randrange(min_h, 300),
                      p_width, p_gap, s_width, s_height, p_vel))
    first_pipe_x += p_width + p_space


# player
radius = 25
gravity = 0.5
jump_vel = 6
# player = Player(300, s_height/3, radius, gravity,
#                 jump_vel, pipes, s_width, s_height)

# genetic algorithm
mutation_rate = 0.02
generations = 1
print("Generations", generations)

# training methods
using_genetic = True
press_count = 0

players = []
pop_size = 500
# players.append(Player(300, s_height/3, radius, gravity,
#                       jump_vel, pipes, s_width, s_height))
for _ in range(pop_size):
    player = Player(300, s_height/3, radius, gravity,
                    jump_vel, pipes, s_width, s_height,
                    mutate_rate=mutation_rate)
    players.append(player)


def natural_selection(players):
    # calculate fitness
    s = 0
    for player in players:
        s += player.fitness

    # normalize the fitnesses
    for player in players:
        player.fitness /= s


# generate a new population
def reproduce():
    global players, generations
    new_pop = []
    # probability list
    prob = [player.fitness for player in players]
    for _ in range(pop_size):
        parent = np.random.choice(players, p=prob)
        brain = parent.copy_brain()
        child = Player(300, s_height/3, radius, gravity, jump_vel,
                       pipes, s_width, s_height, brain, mutation_rate)
        child.mutate()
        new_pop.append(child)

    players = new_pop
    generations += 1
    print("Generations", generations)


# restart the game
def restart():
    global pipes, players
    pipes = []
    # player = Player(300, s_height/3, radius, gravity,
    #                 jump_vel, pipes, s_width, s_height)

    first_pipe_x = 500
    while first_pipe_x < s_width:
        pipes.append(Pipe(first_pipe_x, random.randrange(min_h, 300),
                          p_width, p_gap, s_width, s_height, p_vel))
        first_pipe_x += p_width + p_space

    if using_genetic:
        natural_selection(players)
        reproduce()
    else:
        parent = players[0]
        brain = parent.copy_brain()
        child = Player(300, s_height/3, radius, gravity, jump_vel,
                       pipes, s_width, s_height, brain)
        players[0] = child


bg = pygame.image.load('bg.jpg')

# button
save_button = Button(10, 10, 150, 50, "Save Model")
load_button = Button(10, 70, 150, 50, "Load Model")


def save_model():
    # find the best one
    best = None
    m = 0
    for i, player in enumerate(players):
        if player.fitness == 0:
            player.cal_fitness()
        if player.fitness >= m:
            m = player.fitness
            best = i

    with open('model.pkl', 'wb') as f:
        pickle.dump(players[best].brain, f, pickle.HIGHEST_PROTOCOL)
    print("Model is saved to model.pkl")


def load_model():
    global players, using_genetic
    brain = None
    with open('model.pkl', 'rb') as f:
        brain = pickle.load(f)
    players = [Player(300, s_height/3, radius, gravity, jump_vel,
                      pipes, s_width, s_height, brain)]
    using_genetic = False


def draw():
    # background
    window.blit(bg, (0, 0))

    # draw pipes
    for pipe in pipes:
        pipe.draw(window)

    # delete offscreen pipes
    if len(pipes) > 0 and pipes[0].offscreen():
        pipes.pop(0)

    # draw player
    for player in players:
        player.draw(window)

    # buttons
    save_button.draw(window)
    load_button.draw(window)

    pygame.display.update()


answer = [[0], [1]]
player_count = 0
train_count = 0
is_drawing = True
run = True
while run:
    clock.tick(fps)

    mouse_pos = pygame.mouse.get_pos()

    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if save_button.is_over(mouse_pos):
                save_model()
            if load_button.is_over(mouse_pos):
                load_model()

        if event.type == pygame.MOUSEMOTION:
            if save_button.is_over(mouse_pos):
                save_button.color = (200, 200, 200)
            else:
                save_button.color = (255, 255, 255)

            if load_button.is_over(mouse_pos):
                load_button.color = (200, 200, 200)
            else:
                load_button.color = (255, 255, 255)

    if is_drawing:
        r = 1
    else:
        r = 1000

    for _ in range(r):
        # add new pipe if there are no pipes
        # or the p_space has passed
        if len(pipes) == 0 or (pipes[-1].x + p_width + p_space - s_width) < 0:
            pipes.append(Pipe(s_width, random.randrange(min_h, max_h),
                              p_width, p_gap, s_width, s_height, p_vel))

        # check if player is dead - hits a pipe
        if all([p.dead for p in players]):
            restart()

        # check key pressed
        keys = pygame.key.get_pressed()

        answer = [0.0, 1.0]
        # answer = [[0], [1]]
        if keys[pygame.K_SPACE]:
            for player in players:
                player.up()
            # answer = [[1], [0]]
            answer = [1.0, 0.0]

        # AI
        for player in players:
            if not player.dead:
                player.think()
        # if using_genetic:
        #     for player in players:
        #         if not player.dead:
        #             player.think()
        #     # if player_count >= len(players):
        #     #     think_count = 0
        #     # players[player_count % len(players)].think()
        #     # player_count += 1
        # else:
        #     players[0].train(answer)
        is_drawing = True

    # switch to genetic
    if keys[pygame.K_s] and press_count > 50:
        using_genetic = not using_genetic
        print('s')
        press_count = 0

    if keys[pygame.K_d] and press_count > 50:
        is_drawing = not is_drawing
        press_count = 0
    press_count += 1

    if keys[pygame.K_ESCAPE]:
        run = False

    # update drawing
    draw()


pygame.quit()
