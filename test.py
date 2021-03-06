import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    """Initialize game and create a screen object"""

    """ Initialize pygame, settings, and screen object. """
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    """ Make the play button """
    play_button = Button(ai_settings,screen,"Play")

    """ Create an instance to store game statistics and create a scoreboard """
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)

    """ Make a ship """
    ship = Ship(screen,ai_settings)

    """ Make a group to store the bullets in. """
    bullets = Group()   # A group is initialized, currently it is empty.

    """ Make an alien """
    aliens = Group()
    gf.create_fleet(ai_settings,screen,ship,aliens)

    """ Make a fireball """
    fireball = Group()
    #fireball = Fireball(ai_settings,screen,aliens)

    """ Start the main loop for the game """
    while True:

        #Watch for keyboard and mouse events
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)  #contains the event loop and responds to events
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,stats,screen,ship,aliens,bullets,fireball)
            gf.update_fireball(ai_settings,stats,screen,ship,aliens,bullets,fireball)
            gf.fire_fireball(ai_settings,screen,aliens,bullets,fireball)

        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button,fireball)

run_game()
