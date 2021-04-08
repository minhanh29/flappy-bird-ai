from pygame.draw import circle
from pygame import Rect, Color
from pygame.image import load
from pygame.transform import scale
from math import sqrt
import time
from neural_network import NeuralNetWork


class Player():
    def __init__(self, x, y, radius, gravity, jump, pipes,
                 s_width, s_height, brain=None, mutate_rate=0.01):
        self.x = x
        self.y = y
        self.radius = radius
        self.jump = jump
        self.pipes = pipes
        self.s_width = s_width
        self.s_height = s_height
        self.color = Color(0, 0, 0, a=0.1)

        # acceleration
        self.acc = gravity
        self.vel = 0
        self.vel_max = sqrt(s_height)

        # check jumping
        self.is_jump = False
        self.jump_count = 0

        # check alive
        self.dead = False

        # image
        self.img = scale(load('bird.png'),
                         (self.radius * 2 + 10, self.radius * 2 + 10))

        # neural network
        # input: x, velocity, pipe.x, pipe.y, pipe.gap,
        if brain is None:
            self.brain = NeuralNetWork(4, 3, 2, mutate_rate=mutate_rate)
            # self.brain = tf.keras.Sequential([
            #     tf.keras.layers.Input(shape=(5,)),
            #     tf.keras.layers.Dense(
            #         units=5,
            #         activation='sigmoid',
            #     ),
            #     tf.keras.layers.Dense(
            #         units=2,
            #         activation='softmax'
            #     )
            # ])
        else:
            self.brain = brain

        # self.brain.compile(optimizer='adam',
        #                    loss="categorical_crossentropy",
        #                    metrics=['accuracy'])

        # genetic algorithm
        self.fitness = 0
        self.score = 0
        self.lifetime = time.time()
        self.prev_pipe_y = None

    def draw(self, window):
        if self.dead:
            return

        # circle(window, self.color, (self.x, self.y), self.radius)
        window.blit(self.img, (self.x - self.radius - 5,
                               self.y - self.radius - 5))
        self.vel += self.acc
        self.y += self.vel
        if self.vel > 0 and self.is_jump:
            self.is_jump = False

        # check collisions with pipes
        if self.is_collide_pipe(self.next_pipe()):
            self.dead = True
            self.cal_fitness()

        # check ceiling and floor
        if self.y + self.radius > self.s_height or\
                self.y - self.radius < 0:
            self.dead = True
            self.cal_fitness()

    # check collision with a pipe
    def is_collide_pipe(self, pipe):
        if pipe is None:
            return False

        my_collider = self.get_collider()
        p_upper = pipe.get_upper_collider()
        p_lower = pipe.get_lower_collider()

        return my_collider.colliderect(p_upper) or\
            my_collider.colliderect(p_lower)

    # return the box collider
    def get_collider(self):
        return Rect(self.x - self.radius, self.y - self.radius,
                    self.radius * 2, self.radius * 2)

    def up(self):
        if self.is_jump:
            return

        self.vel = -self.jump
        self.is_jump = True

    # find the next pipe
    def next_pipe(self):
        for pipe in self.pipes:
            if pipe.x + pipe.width - self.x > 0:
                if self.prev_pipe_y is not None and self.prev_pipe_y != pipe.y:
                    d1 = abs(self.y - self.prev_pipe_y)
                    d2 = abs(self.y - (self.prev_pipe_y + pipe.gap))
                    d = abs(d1 - d2) / pipe.gap + 0.01
                    self.score += 100 + 10/d
                self.prev_pipe_y = pipe.y
                return pipe
        return None

    # brain decide whether player should jump
    def think(self):
        # get the next pipe
        pipe = self.next_pipe()
        if pipe is None:
            return

        # normalize the inputs
        inputs = [self.y / self.s_height,
                  self.vel/self.vel_max,
                  (pipe.x + pipe.width)/self.s_width,
                  pipe.y/self.s_height]
        output = self.brain.predict(inputs)

        if output[0][0] > output[1][0]:
            self.up()

    # GENETIC ALGORITHM
    # copy the brain
    def copy_brain(self):
        return self.brain.copy()

    # crossover
    def crossover_brain(self, other_brain):
        return self.brain.crossover(other_brain)

    # mutation
    def mutate(self):
        self.brain.mutate()
        # for layer in self.brain.layers:
        #     weights = layer.get_weights()  # numpy array
        #     w = weights[0]  # array
        #     for i in range(len(w)):
        #         for j in range(len(w[i])):
        #             if random() < rate:
        #                 w[i][j] += gauss(0, 0.1)
        #     layer.set_weights(weights)

    # calculate the fitness
    def cal_fitness(self):
        self.lifetime = time.time() - self.lifetime
        self.fitness = self.score + self.lifetime * 5

    # MANUAL TRAINING
    def train(self, answer):
        # get the next pipe
        pipe = self.next_pipe()
        if pipe is None:
            return

        # normalize the inputs
        inputs = [self.y / self.s_height,
                  self.vel/self.vel_max,
                  (pipe.x + pipe.width)/self.s_width,
                  pipe.y/self.s_height]

        self.brain.train(inputs, answer)
