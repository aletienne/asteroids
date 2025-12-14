import pygame

fire = thrust = bangSmall = bangLarge = extraShip = None;
audio = False;

def load_sounds():
    global fire, thrust, bangSmall, bangLarge, extraShip
    fire = pygame.mixer.Sound("sound/fire.wav")
    fire.set_volume(0.25)
    thrust = pygame.mixer.Sound("sound/thrust.wav")
    thrust.set_volume(0.25)
    bangSmall = pygame.mixer.Sound("sound/bangSmall.wav")
    bangSmall.set_volume(0.25)
    bangLarge = pygame.mixer.Sound("sound/bangLarge.wav")
    extraShip = pygame.mixer.Sound("sound/extraShip.wav")