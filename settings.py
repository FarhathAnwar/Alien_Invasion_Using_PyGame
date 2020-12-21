class Settings():
    """ A class to store all the settings for alien invasion """

    def __init__(self):
        """ Initialize the game's static settings """

        """ Screen settings"""
        self.screen_width = 1200
        self.screen_height = 680
        self.bg_color = (230,230,230)

        """ Ship settings """
        self.ship_speed_factor = 1.5
        self.ship_limit = 2

        """ Bullet settings"""
        self.bullet_speed_factor = 3  # Means 1 pixel per strike
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullets_allowed = 3

        """ Alien settings """
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        """ How quickly the game speeds up """
        self.speedup_scale = 1.1

        """ How quickly the alien point values increase """
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

        """ To write a live score to the screen, we update the value of stats.score whenever
        an alien is hit, and then call prep_score() to update the score image.
        But fist, let’s determine how many points a player gets each time they shoot
        down an alien: """

        """ Scoring """
        self.alien_points = 50

        """ Alien's fireballs """
        self.fireball_speed_factor = 2  # Means 1 pixel per strike
        self.fireball_width = 6
        self.fireball_height = 17
        self.fireball_color = 232,76,9
        self.fireball_allowed = 2

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.fleet_direction = 1

    def increase_speed(self):
        """ Increase speed settings and alien point values """
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)