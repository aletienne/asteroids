import pygame
import random
from constants import *
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0  # in degrees
        self.timer = 0
        self.velocity = pygame.Vector2(0, 0)
        self.thrust_power = 200         # tweak to taste
        self.friction = 0.99            # 1.0 = no friction
        self.thrusting = False
    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        points = self.triangle()
        pygame.draw.polygon(screen, "white", points, 2)

        # --- draw flame only when thrusting ---
        if self.thrusting:
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
            # small random flicker in length
            flame_len = self.radius * random.uniform(1.2, 1.8)

            # base of flame is slightly behind the ship base
            base_center = self.position - forward * self.radius * 1.1

            # two base corners are near the ship's back
            base_left  = base_center - right * 0.4
            base_right = base_center + right * 0.4

            # tip goes further back (opposite forward)
            tip = base_center - forward * flame_len

            flame_points = [base_left, tip, base_right]

            # thin filled flame
            pygame.draw.polygon(screen, "white", flame_points, 2)  # orange-ish

    def rotate(self,dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def thrust(self, dt, direction=1):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * self.thrust_power * dt * direction
        
    def update(self, dt):
        self.timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_UP]:
            self.thrust(dt, direction=1)
            self.thrusting = True
        else:
            self.thrusting = False    
        #if keys[pygame.K_DOWN]:
        #    self.thrust(dt, direction=-1)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit()

        self.velocity *= self.friction
        self.position += self.velocity * dt
        self.wrap()

    def move(self,dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.timer > 0:
            return
        self.timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        #shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = forward * PLAYER_SHOOT_SPEED + self.velocity