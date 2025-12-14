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
import sound

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
    pygame.mixer.set_num_channels(16)
    sound.load_sounds()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    Clock = pygame.time.Clock()
    pygame.display.set_caption("Asteroids")
    dt=0
    player=Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    game_play = True
    font = pygame.font.SysFont("DejaVu Sans Mono", 32)
    goal_score = 1000 #GOAL_SCORE
    goal_increment = GOAL_INCREMENT

    while game_play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:            
                    player.pause = not player.pause
                if event.key == pygame.K_ESCAPE:
                    game_play = False

        if player.pause:
            draw_message(screen, font, "PAUSED")
            pygame.display.flip()
            Clock.tick(15)
            continue

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
        if player.lives < 0:
            player.kill()
            draw_screen(screen,dt,player,font)
            draw_message(screen, font, "GAME OVER")
            pygame.display.flip()
            print("Game over!")
            pygame.time.delay(5000)
            game_play = False

        if player.score >= goal_score:
            player.lives += 1
            sound.extraShip.play()
            goal_score += goal_increment

    pygame.quit()

def draw_screen(screen,dt,player,font):
    screen.fill("black")
    updateable.update(dt)
    for i in drawable:
        i.draw(screen)
    draw_score(screen, player.score,font)
    draw_icons(player, screen, player.lives)
    pygame.display.flip()

def draw_score(screen, score, font):
    text = f"{score}"
    display_text = font.render(text, True, "white")
    screen.blit(display_text, (SCREEN_WIDTH/2 - display_text.get_width()/2, 10))

def draw_message(screen, font, text):
    font_large = pygame.font.SysFont(None, 128)
    display_text = font_large.render(text, True, "white")
    screen.blit(display_text, (SCREEN_WIDTH/2 - display_text.get_width()/2, SCREEN_HEIGHT/2 - display_text.get_height()/2))

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


if __name__ == "__main__":
    main()
