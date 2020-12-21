import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """ A class to manage bullets fired from the ships"""

    def __init__(self,ai_settings,screen,ship):
        """ Create a bullet object at the ship's current position"""
        super().__init__()
        self.screen = screen

        """ Create a bullet rect at (0,0) and then set correct position"""

        #Creating a bullet manually
        self.rect = pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
        # pygame.Rect(Coordinates of top-left corner x,y,width of the rect,height of the rect)

        #Setting the correct position
        self.rect.centerx = ship.rect.centerx  # bullet er center hobe ship er center e
        self.rect.top = ship.rect.top

        """ Store bullet's position as a decimal value"""
        self.y = float(self.rect.y)  # rect.y beacuse bullet will go upward hence y-axis

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """ Move the bullet up the screen"""

        """ Update the decimal position of the bullet"""
        self.y -= self.speed_factor     # y is just a variable

        """ Update the position of the rect"""
        self.rect.y = self.y

    def draw_bullet(self):
        """ Draw the bullet to the screen"""

        """ draw.rect() takes 3 parameters: the screen, color of the rect, the rect"""
        pygame.draw.rect(self.screen,self.color,self.rect)

    """The update() method manages the bullet’s position. When a bullet
    is fired, it moves up the screen, which corresponds to a decreasing
    y-coordinate value; so to update the position, we subtract the amount
    stored in self.speed_factor from self.y. We then use the value of self.y
    to set the value of self.rect.y v. The speed_factor attribute allows us to
    increase the speed of the bullets as the game progresses or as needed to
    refine the game’s behavior. Once fired, a bullet’s x-coordinate value never
    changes, so it will only travel vertically in a straight line.
    When we want to draw a bullet, we’ll call draw_bullet(). The draw.rect()
    function fils the part of the screen defied by the bullet’s rect with the
    color stored in self.color """