import pygame

fire = None;
thrust = None;

def load_sounds():
    global fire, thrust
    fire = pygame.mixer.Sound("sound/fire.wav")
    thrust = pygame.mixer.Sound("sound/thrust.wav")