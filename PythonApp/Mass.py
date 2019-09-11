import numpy as np
import math
import matplotlib.pyplot as plt
import random
import pygame

# Gravitational constant
grav_const = 6.674 * 10**(-11)
# Global list of objects
list_of_objects = np.empty(0, dtype = object)
# Timestamp
timestamp = 600
# Screen max width and height (screen is square)
screen_size = 1000
max_dist = 10 ** 12
# Orbits (0 -> off, 1 -> on)
orbits = 1

class mass:
    """Mass"""

    def __init__(self, mass, xcor, ycor, xvel, yvel, xacc, yacc):
        self.mass = mass
        self.xcor = xcor
        self.ycor = ycor
        self.xvel = xvel
        self.yvel = yvel
        self.xacc = xacc
        self.yacc = yacc

    def calc_radius(self, obj):
        radius_x = obj.xcor - self.xcor
        radius_y = obj.ycor - self.ycor
        radius = math.sqrt(radius_x ** 2 + radius_y ** 2)
        return [radius_x, radius_y, radius]

    def calc_force(self, obj):

        [radius_x, radius_y, radius] = self.calc_radius(obj)
        force = grav_const * self.mass * obj.mass / (radius ** 2)
        force_x = force * (radius_x / radius)
        force_y = force * (radius_y / radius)
        return [force_x, force_y]

    def calc_acceleration(self):
        sum_force_x = 0
        sum_force_y = 0
        for obj in list_of_objects:
            if obj is self:
                continue
            [force_x, force_y] = self.calc_force(obj)
            sum_force_x = sum_force_x + force_x
            sum_force_y = sum_force_y + force_y
        self.xacc = sum_force_x / self.mass
        self.yacc = sum_force_y / self.mass


    def update_velocity_and_coordinates(self):
        self.xvel = self.xvel + self.xacc * timestamp
        self.yvel = self.yvel + self.yacc * timestamp
        self.xcor = self.xcor + self.xvel * timestamp
        self.ycor = self.ycor + self.yvel * timestamp

def norm_coords(coord):
    if coord == 0:
        coord = screen_size/2
    elif coord >= 0:
        coord = screen_size/2 + coord/max_dist*screen_size/2
    else:
       coord = screen_size/2 - abs(coord)/max_dist*screen_size/2
    return int(round(coord))

earth = mass(5.972 * (10 ** 24), 149600000000, 0, 0, 30000, 0, 0)
sun = mass(1.989 * (10 ** 30), 0, 0, 0, 0, 0, 0)

# Add Sun and Earth
list_of_objects = np.append(list_of_objects, [sun, earth])

# Add random objects
for i in range(2):
    list_of_objects = np.append(list_of_objects, mass(random.randint(10 ** 15,10 ** 20), random.randint(-10 ** 11,10 ** 11), random.randint(-10 ** 11,10 ** 11), random.randint(-10 ** 4,10 ** 4), random.randint(-10 ** 4,10 ** 4), 0, 0))

# Animation
pygame.init()
screen = pygame.display.set_mode((1000,1000))
pygame.display.update()

iter = 0
for time in range(0, timestamp*365*24*6*2, timestamp):
    if iter == 20:
        iter = 0
    iter = iter + 1
    # Refresh screen
    if iter == 15 and orbits == 0:
        screen.fill((0,0,0))
    for obj in list_of_objects:
        # Calculate accelerartions
        obj.calc_acceleration()
        # Update properties of each planet
        obj.update_velocity_and_coordinates()
        # Update screen every 10 iterations
        if iter == 15:
            if obj == sun:
                pygame.draw.circle(screen, (255,255,0), (norm_coords(sun.xcor),norm_coords(sun.ycor)), 10)
            elif obj == earth:
                pygame.draw.circle(screen, (0,255,0), (norm_coords(obj.xcor),norm_coords(obj.ycor)), 4)
            else:
                pygame.draw.circle(screen, (255,255,255), (norm_coords(obj.xcor),norm_coords(obj.ycor)), 3)
            pygame.display.update()
    