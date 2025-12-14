import pygame
import random
from constants import *
from circleshape import CircleShape
from shot import Shot
from sound import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0  # in degrees
        self.timer = 0
        self.velocity = pygame.Vector2(0, 0)
        self.thrust_power = PLAYER_THRUST_POWER     # tweak to taste
        self.friction = 0.99                        # 1.0 = no friction
        self.thrusting = False
        self.sheild = False
        self.sheild_lifetime = PLAYER_SHEILD_LIFETIME
        self.sheild_timeoute = 0
        self.exploding = False
        self.explosion_time = 0.0
        self.explosion_duration = 3  # seconds 0.7
        self.explosion_segments = []   # list of {p1, p2, dir, speed}
        self.grace_period = 2.0  # seconds of invulnerability after respawn
        self.invincible = False
        self.blinking = False
        self.visible = True
        self.blink_duration = 0.0     # total blink time
        self.blink_elapsed = 0.0
        self.blink_interval = 0.1     # how fast it flickers (seconds)
        self._blink_accum = 0.0
        self.lives = 2
        self.score = 0
    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        d = a + (b -a) * 1.2
        e = a + (c -a) * 1.2
        return [a, b, c, d, e]
    
    def draw(self, screen):
        if self.exploding:
            # draw exploding segments
            t = self.explosion_time
            for seg in self.explosion_segments:
                offset = seg["dir"] * seg["speed"] * t
                p1 = seg["p1"] + offset
                p2 = seg["p2"] + offset
                pygame.draw.line(screen, "white", p1, p2, 2)
            self.draw_icons(screen, self.lives)
            return
        points = self.triangle()
        #pygame.draw.polygon(screen, "white", points, 2)
        
        self.draw_icons(screen, self.lives)

        if self.blinking and not self.visible:
            return  # skip drawing this frame
        
        pygame.draw.line(screen, "white", points[0], points[3], 2)
        pygame.draw.line(screen, "white", points[0], points[4], 2)
        pygame.draw.line(screen, "white", points[1], points[2], 2)

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
            # flame
            pygame.draw.polygon(screen, "white", flame_points, 2)

        if self.sheild:
            thickness = max(1, int((self.sheild_lifetime + 1) / 1))
            pygame.draw.circle(screen, "white", self.position, self.radius+18,thickness*2)

    def rotate(self,dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def thrust(self, dt, direction=1):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * self.thrust_power * dt * direction
        
    def update(self, dt):
        if self.exploding:
            # advance explosion time and end when done
            self.explosion_time += dt
            if self.explosion_time >= self.explosion_duration:
                self.exploding = False
                self.position = pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
                self.velocity = pygame.Vector2(0, 0)
                self.invincible = True
                self.grace_period = 1
                self.start_blinking()
                self.lives -= 1
                # self.kill()  # remove the player sprite entirely
            return  # skip normal movement & input while exploding
        self.timer -= dt
        self.grace_period -= dt

        if self.blinking:
            self.blink_elapsed += dt
            self._blink_accum += dt

            # toggle visibility every blink_interval
            if self._blink_accum >= self.blink_interval:
                self._blink_accum -= self.blink_interval
                self.visible = not self.visible

            # stop blinking after duration
            if self.blink_elapsed >= self.blink_duration:
                self.blinking = False
                self.invincible = False
                self._visible = True

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
        if keys[pygame.K_DOWN]:
            if self.sheild == False and self.sheild_timeoute <= 0:
                self.sheild_lifetime = PLAYER_SHEILD_LIFETIME
                
            if self.sheild_timeoute <= 0 and self.sheild_lifetime > 0:
                self.sheild_lifetime -= dt
                self.sheild = True
            else:
                self.sheild = False
                if self.sheild_timeoute <= 0:
                    self.sheild_timeoute = PLAYER_SHEILD_TIMEOUT
        else:
            self.sheild = False
        if keys[pygame.K_SPACE]:
            self.shoot()
        
        
        if self.sheild == False and self.sheild_timeoute > 0:
            self.sheild_timeoute -= dt

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
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        nose_center = self.position + forward * self.radius * 1.1
        #shot = Shot(self.position.x, self.position.y)
        sound.shot.play()
        shot = Shot(nose_center.x, nose_center.y)
        #shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = forward * PLAYER_SHOOT_SPEED + self.velocity
    
    def start_explosion(self):
        #Capture the current ship lines and give them outward velocities.
        if self.exploding:
            return  # already exploding
        
        self.exploding = True
        self.explosion_time = 0.0
        self.explosion_segments.clear()

        points = self.triangle()  # [a, b, c, d, e]

        # The three lines you currently draw:
        lines = [
            (points[0], points[3]),  # nose to left leg
            (points[0], points[4]),  # nose to right leg
            (points[1], points[2]),  # base
        ]

        for p1, p2 in lines:
            # use the segment midpoint to decide direction away from center
            mid = (p1 + p2) / 2
            dir_vec = mid - self.position
            if dir_vec.length_squared() == 0:
                dir_vec = pygame.Vector2(1, 0)  # fallback

            # add a bit of random jitter in direction
            dir_vec = dir_vec.rotate(random.uniform(-20, 20)).normalize()

            speed = random.uniform(150, 300)  # pixels per second

            self.explosion_segments.append({
                "p1": p1,
                "p2": p2,
                "dir": dir_vec,
                "speed": speed,
            })

    def start_blinking(self, duration=2, interval=0.1):
        self.blinking = True
        self.blink_duration = duration
        self.blink_elapsed = 0.0
        self.blink_interval = interval
        self._blink_accum = 0.0
        self.visible = True

    def draw_icons(self, screen, lives):
        # size + spacing of icons
        icon_radius = 10
        spacing = 5

        # where to start (top-right corner)
        x = SCREEN_WIDTH - 20
        y = 20

        for i in range(lives):
            # shift each icon to the left
            pos = pygame.Vector2(x - i * (icon_radius * 2 + spacing), y)

            # draw a small upward-pointing ship
            rotation = 0  # pointing up
            forward = pygame.Vector2(0, -1).rotate(rotation)  # up on screen
            right = pygame.Vector2(1, 0).rotate(rotation) * icon_radius / 1.5

            a = pos + forward * icon_radius
            b = pos - forward * icon_radius - right
            c = pos - forward * icon_radius + right

            pygame.draw.line(screen, "white", a, b, 2)
            pygame.draw.line(screen, "white", a, c, 2)
            pygame.draw.line(screen, "white", b, c, 2)