# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
import sys
from constants import *
from player import *
from circleshape import *
from asteroid import *
from asteroidfield import *
from shot import *

updateable = pygame.sprite.Group()
drawable = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
shots = pygame.sprite.Group()

Player.containers = (updateable, drawable)
Asteroid.containers = (asteroids, updateable, drawable)
AsteroidField.containers = (updateable,)
Shot.containers = (shots, updateable, drawable)
asteroid_field = AsteroidField()


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    Clock = pygame.time.Clock()
    pygame.display.set_caption("Asteroids")
    dt=0
    player=Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        screen.fill("black")
        updateable.update(dt)
        # check for collision between bullet and asteroids
        for i in asteroids:
            for j in shots:
                if i.collision(j):
                    i.kill()
                    j.kill()
        # check for collision between player and asteroids
        for i in asteroids:
            if player.collision(i):
                print("Game over!")
                sys.exit(0)
        for i in drawable:
            i.draw(screen)
        pygame.display.flip()
        dt=Clock.tick(60)/1000

if __name__ == "__main__":
    main()
