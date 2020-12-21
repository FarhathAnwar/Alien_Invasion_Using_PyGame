import pygame


class Ship():

    def __init__(self,screen,ai_settings):
        """Initialize the ship and set its starting position."""
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()     #Stores the images's rect object through which we can change it's position
        self.screen_rect = screen.get_rect()  #Stores the screen's rect object through which we can change it's position

        # Start each new ship at the bottom centre of the screen

        # The x-coordinate of the ship's center matches the 'centerx' attribute of the screen's rect
        self.rect.centerx = self.screen_rect.centerx

        # Make the y-coordinate the ship's bottom equal to the value of the screen rect’s bottom attribute
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center
        self.center = float(self.rect.centerx)

        # Movement flag
        """The ship class controls all attributes of the ship, so we’ll give it an attribute called moving_right
        and an update() method to check the status of the moving_right flag.The update() method will change
        the position of the ship if the flag is set to True. We’ll call this method any time we want to update
        the position of the ship."""

        self.moving_right = False
        self.moving_left = False

    def update(self):
        """ Update the ship's position based on the movement flag"""
        """ Update the ship's center value not the rect beacuse rect attributes can only deal with integers """

        if self.moving_right and self.rect.right < self.screen_rect.right:  #rect.right returns the x-coordinate value of the right edge of the ship's rect,
            #self.rect.centerx += 1                                       #if this value < than self.screen_rect.right then the ship hasnt reached the right edge.
            self.center += self.ai_settings.ship_speed_factor

        if self.moving_left and self.rect.left > 0:                    #if the value of the left side of the rect is greater than zero,
            #self.rect.centerx -= 1                                      #the ship hasn’t reached the left edge of the screen.
            self.center -= self.ai_settings.ship_speed_factor

        """ Update the rect object from self.center """
        """ Only the integer portion of self.center will be stored in self.rect.centerx,
            but that’s fine for displaying the ship."""
        self.rect.centerx = self.center

    def blitme(self):
        """Draw the ship at its current location."""
        #draw the image to the screen at the position specifid by self.rect.
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx
