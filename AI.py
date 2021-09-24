import pygame
import math
import random


class AI:
    shot_chance = 6  # static variable
    x = 0
    y = 0
    speed = 0
    AI_width = 0
    AI_height = 0
    type = 0
    health = 0
    img = None
    angle = 0
    dis_width = 504  # static variable
    dis_height = 648  # static variable

    # determines which enemy to display
    def setup(self):
        # strongest enemy, Alice
        if self.type == 1:
            self.health = 2
            self.speed = 3   # fix later
            self.img = pygame.image.load("assets/Alice.png")
            self.img = pygame.transform.rotozoom(self.img, 0, 0.1)
            self.AI_width = 73.6
            self.AI_height = 92
        # jeroo, mid tier
        elif self.type == 2:
            self.health = 1
            self.speed = 6
            self.img = pygame.image.load("assets/jeroo.png")
            self.img = pygame.transform.rotozoom(self.img, 0, 0.05)
            self.AI_width = 124
            self.AI_height = 175.4
        # everything else is Dino
        else:
            self.health = 1
            self.speed = 2
            self.img = pygame.image.load("assets/Dino.png")
            self.img = pygame.transform.rotozoom(self.img, 0, 0.5)
            self.AI_width = 91
            self.AI_height = 117.5

    def hurt(self):
        self.health -= 1

    # translate overall speed into two directional velocities that add up to the same velocity
    # child algorithm (in the AI class)
    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

    # randomly chooses which direction to turn (bias for turning clockwise)
    def turn(self):
        d_angle = None
        rand_num = random.randint(1, 5)

        if rand_num == 1:
            d_angle = 22.5
        elif 2 <= rand_num <= 4:
            d_angle = -22.5
        else:
            d_angle = 0

        self.angle += d_angle
        return d_angle

    # checks how to handle enemy according to screen boundaries
    # child algorithm (in AI class)
    def bounds(self):
        # horizontal boundary
        if self.x < 0:
            self.x += self.speed
        elif self.x > AI.dis_width-self.AI_width:
            self.x -= self.speed

        # vertical boundary
        if self.y > AI.dis_height:
            self.y = 0
        elif self.y < self.AI_height:
            self.y += self.speed

    # randomly shoots
    # returns true if shooting
    @staticmethod
    def shoot():
        chance = random.randint(1, 10)
        if chance > AI.shot_chance:  # chance to shoot = 100 - (10*shot_chance)
            return True
        else:
            return False

    # constructor
    def __init__(self, AI_type=0, x_strt=0, y_strt=0):
        self.type = AI_type
        self.setup()
        self.x = x_strt
        self.y = y_strt

