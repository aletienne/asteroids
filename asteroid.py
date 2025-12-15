import pygame
import random
import math
from constants import *
from circleshape import CircleShape
import sound

asteroid_val=[ASTEROID_SCORE_SMALL, ASTEROID_SCORE_MEDIUM, ASTEROID_SCORE_LARGE]

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.points = self.generate_asteroid_points(radius)
        self.score = asteroid_val[max(0, int(self.radius / 20)-1)]
        self.rate = random.uniform(-1,1)
        self.angle = 0

    def generate_asteroid_points(self, radius, irregularity=0.1, point_count=6):
        # radius: base radius
        # irregularity: how jagged (0.0 = circle, 0.5 = pretty lumpy)
        # point_count: number of vertices
        
        points = []
        for i in range(point_count):
            angle = (2 * math.pi / point_count) * i
            # random radius between (1 - irregularity) and (1 + irregularity) times base
            offset = 1 + random.uniform(-irregularity, irregularity)
            r = radius * offset
            x = math.cos(angle) * r
            y = math.sin(angle) * r
            points.append((x, y))
        return points
    
    def draw(self, screen):
        cx, cy = self.position
        # shift local points to screen coordinates
        world_points = [(cx + x, cy + y) for (x, y) in self.points]
        self.angle += self.rate
        self.angle %= 360
        rotated_points = self.rotate(world_points, self.position, self.angle)
        thickness = max(1, int(self.radius / 20))
        pygame.draw.polygon(screen, "white", rotated_points, thickness)
        #pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap()

    def split(self):
        if self.radius > ASTEROID_MIN_RADIUS:
            angle = random.uniform(20,50)
            vector1 = self.velocity.rotate(angle)
            vector2 = self.velocity.rotate(-angle)
            asteroid1 = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
            asteroid2 = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
            asteroid1.velocity = vector1
            asteroid2.velocity = vector2
            if sound.audio:
                sound.bangSmall.play()
            self.kill()
        else:
            if sound.audio:
               sound.bangSmall.play()
            self.kill()
            return

    def rotate(self, points, pivot, angle):
        # Rotates a list of points (tuples/lists) around a given pivot point by an angle in degrees.
        # Convert the pivot to a Vector2
        pp = pygame.math.Vector2(pivot)
        rotated_points = []
        for point in points:
            # Calculate the vector from the pivot to the point
            vector = pygame.math.Vector2(point) - pp
            # Rotate the vector
            rotated_vector = vector.rotate(angle)
            # Add the pivot back to the rotated vector to get the final position
            rotated_point = rotated_vector + pp
            rotated_points.append((rotated_point.x, rotated_point.y))
        return rotated_points