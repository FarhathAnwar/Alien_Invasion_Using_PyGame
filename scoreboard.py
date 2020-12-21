import pygame.font

class Scoreboard():
    """ A class to report scoring information"""

    def __init__(self,ai_settings,screen,stats):
        """ Initialize score keeping attributes """

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        """ Font settings for scoring information """
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,48)

        """ Prepare the initial score images """
        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    def prep_score(self):
        """ Turn the score into a rendered image """
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        """ A string formatting directive tells Python to insert commas into
        numbers when converting a numerical value to a string—for example, to
        output 1,000,000 instead of 1000000 """

        self.score_image = self.font.render(score_str,True,self.text_color,self.ai_settings.bg_color)

        """ Display the score at the top right of the screen """
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

        """ In prep_score(), we fist turn the numerical value stats.score into a
        string u, and then pass this string to render(), which creates the image v.
        To display the score clearly onscreen, we pass the screen’s background color
        to render() as well as a text color.
        We’ll position the score in the upper-right corner of the screen and
        have it expand to the left as the score increases and the width of the number grows.
        To make sure the score always lines up with the right side of the
        screen, we create a rect called score_rect w and set its right edge 20 pixels
        from the right screen edge x. We then place the top edge 20 pixels
        down from the top of the screen y.
        Finally, we create a show_score() method to display the rendered score
        image: """

    def prep_high_score(self):
        """ Turn the high score into a rendered image """
        high_score = int(round(self.stats.high_score, -1))  # We round the high score to the nearest 10
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()

        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """ Turn the level into a rendered image """
        self.level_image = self.font.render(str(self.stats.level),True,self.text_color,self.ai_settings.bg_color)

        """ Position the level below the score """
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def show_score(self):
        """ Draw score and ships to the screen to the screen """
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)


