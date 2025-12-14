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
from sound import *

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
    pygame.mixer.init()
    sound.load_sounds()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    Clock = pygame.time.Clock()
    pygame.display.set_caption("Asteroids")
    dt=0
    player=Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    game_play = True
    font = pygame.font.SysFont("DejaVu Sans Mono", 32)


    while game_play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        # check for collision between bullet and asteroids
        for i in asteroids:
            for j in shots:
                if i.collision(j):
                    player.score += i.score
                    i.split()
                    j.kill()
        # check for collision between player and asteroids
        for i in asteroids:
            if player.collision(i) and not player.sheild and not player.invincible:
                player.start_explosion()


        dt=Clock.tick(60)/1000
        draw_screen(screen,dt,player,font)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_play = False
        if player.lives < 0:
            player.kill()
            draw_screen(screen,dt,player,font)
            draw_game_over(screen, font)
            pygame.display.flip()
            print("Game over!")
            pygame.time.delay(5000)
            game_play = False
            
    pygame.quit()

def draw_screen(screen,dt,player,font):
    screen.fill("black")
    updateable.update(dt)
    for i in drawable:
        i.draw(screen)
    draw_score(screen, player.score,font)
    pygame.display.flip()

def draw_score(screen, score, font):
    text = f"{score}"
    display_text = font.render(text, True, "white")
    screen.blit(display_text, (SCREEN_WIDTH/2 - display_text.get_width()/2, 10))

def draw_game_over(screen, font):
    font_large = pygame.font.SysFont(None, 128)
    display_text = font_large.render('GAME OVER', True, "white")
    screen.blit(display_text, (SCREEN_WIDTH/2 - display_text.get_width()/2, SCREEN_HEIGHT/2 - display_text.get_height()/2))

if __name__ == "__main__":
    main()
