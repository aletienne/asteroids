import pygame

fire = thrust = bangSmall = bangLarge = extraShip = None;

def audio_safe(*, freq=44100, size=-16, channels=2, buffer=512) -> bool:
    # Try to initialize pygame.mixer. If audio isn't available, fall back to
    # SDL_AUDIODRIVER=dummy and try again. Returns True if audio is usable.
    try:
        if not pygame.get_init():
            pygame.init()
        # Best practice: call pre_init BEFORE mixer init (or before pygame.init()).
        pygame.mixer.pre_init(freq, size, channels, buffer)
        pygame.mixer.init()
        return True
    except pygame.error:
        # Headless / no device: fall back to dummy audio driver
        try:
            os.environ["SDL_AUDIODRIVER"] = "dummy"
            # Re-try init
            pygame.mixer.quit()
            pygame.mixer.pre_init(freq, size, channels, buffer)
            pygame.mixer.init()
            return pygame.mixer.get_init() is not None
        except pygame.error:
            return False

audio = audio_safe();

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