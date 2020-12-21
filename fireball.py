import pygame
from pygame.sprite import Sprite

class Fireball(Sprite):
    """ A class to manage fireballs fired by the aliens """

    def __init__(self,ai_settings,screen,alien):
        super().__init__()
        self.screen = screen

        """ Create a fireball rect and set it's position """
        self.rect = pygame.Rect(0,0,ai_settings.fireball_width,ai_settings.fireball_height)

        # Setting it in the correct position
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.top

        """ Store fireball's position in a decimal value """
        self.y = float(self.rect.y)

        self.color = ai_settings.fireball_color
        self.speed_factor = ai_settings.fireball_speed_factor

    def update(self):
        """ Move the fireball down the screen """

        """ Update the decimal position of the fireball """
        self.y += self.speed_factor

        """ Update the position of the rect """
        self.rect.y = self.y

    def draw_fireball(self):
        pygame.draw.rect(self.screen,self.color,self.rect)
