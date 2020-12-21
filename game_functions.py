import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from fireball import Fireball

''' In this section we’ll create a new module called game_functions, which will store a number
    of functions that make Alien Invasion work. '''

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    """ Respond to keypress and mouse events """
    for event in pygame.event.get():        # This is the event loop
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb, play_button,ship,aliens,bullets, mouse_x, mouse_y)

            """ Pygame detects a MOUSEBUTTONDOWN event when the player clicks anywhere
            on the screen u, but we want to restrict our game to respond to mouse clicks
            only on the Play button. To accomplish this, we use pygame.mouse.get_pos(),
            which returns a tuple containing the x- and y-coordinates of the mouse
            cursor when the mouse button is clicked v. We send these values to the
            function check_play_button() w, which uses collidepoint() to see if the point
            of the mouse click overlaps the region defied by the Play button’s rect x.
            If so, we set game_active to True, and the game begins! """

        elif event.type == pygame.KEYDOWN:   #KEYDOWN is when the buttons are pressed
            check_keydown_events(event,ai_settings,screen,ship,bullets)

        elif event.type == pygame.KEYUP:     #KEYUP is when the buttons are released
            check_keyup_events(event,ship)

def check_play_button(ai_settings,screen,stats,sb, play_button,ship,aliens,bullets, mouse_x, mouse_y):
    """ Start a new game when the player clicks play """
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        """ Reset the game settings """
        ai_settings.initialize_dynamic_settings()
        """ Hide mouse cursor """
        pygame.mouse.set_visible(False)

        """ Reset the game statistics """
        stats.reset_stats()
        stats.game_active = True

        """ Reset the scoreboard images """
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()


        """ Empty the list of aliens and bullets """
        aliens.empty()
        bullets.empty()

        """ Create a new fleet and center the ship """
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()



def check_keydown_events(event,ai_settings,screen,ship,bullets):
    """ Respond to keypress """
    if event.key == pygame.K_RIGHT:
        # Move ship to the right
        ship.moving_right = True

    elif event.key == pygame.K_LEFT:
        # Moving ship to the left
        ship.moving_left = True

    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)


def check_keyup_events(event,ship):
    """ Responds to key release"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False

    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button,fireball):
    """ Update images on the screen and flip to the new screen. """

    # Redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind ship and aliens.

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    for fireball in fireball.sprites():
        fireball.draw_fireball()

    """ Draw the score information """
    sb.show_score()

    """ Draw the paly button if the game is inactive """
    if not stats.game_active:
        play_button.draw_button()

    #Make the most recently drawn screen visible
    pygame.display.flip()


def fire_bullet(ai_settings,screen,ship,bullets):
    """ Fire a bullet if limit is not reached """

    # Create a new bullet and add it to the group bullets
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def fire_fireball(ai_settings,screen,aliens,bullets,fireball):
    if len(fireball) < ai_settings.fireball_allowed:
        import random
        rad = random.randint(0,6)
        count = 0
        for alien in aliens.sprites():
            if count == rad:
                new_fireball = Fireball(ai_settings,screen,alien)
                fireball.add(new_fireball)
            count+=1


def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """Update position of bullets and get rid of old bullets."""

    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
     # print(len(bullets))
    check_bullet_alien_collision(ai_settings, screen,stats,sb, ship, aliens, bullets)


def check_bullet_alien_collision(ai_settings, screen,stats,sb, ship, aliens, bullets):
    """ Respond to bullet-alien collision """
    """ Check for any bullets that have hit the aliens """
    """ If so, get rid of the bullet and the alien """

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    """ The sprite.groupcollide() method compares each bullet’s rect with each
    alien’s rect and returns a dictionary containing the bullets and aliens that
    have collided. Each key in the dictionary is a bullet, and the corresponding
    value is the alien that was hit. """

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)

    if len(aliens) == 3:
        """ Destroy existing bullets,speeed up game and create new fleet """
        """ If entire fleet is destroyed, start a new level """
        bullets.empty()
        ai_settings.increase_speed()

        """ Increase level """
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings,screen,ship,aliens)

def create_fleet(ai_settings,screen,ship,aliens):
    """ Create a fill fleet of aliens """
    # Create an alien and find the number of aliens in a row.
    # Spacing between each alien is equal to one alien width.

    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)

    #Create the fleet for aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            #Create an alien and place it in the row
            create_alien(ai_settings,screen,aliens,alien_number,row_number)


def get_number_aliens_x(ai_settings,alien_width):
    """ Determine the number of aliens that fit in a row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    """ Create an alien and place it in the row """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_rows(ai_settings,ship_height,alien_height):
    """ Determine the number of rows of aliens that fit on the screen"""
    available_space_y = ( ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows  = int(available_space_y / (2*alien_height))
    return int(number_rows/2)

def check_fleet_edges(ai_settings,aliens):
    """ Respond appropiately if an alien has reached an edge """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    """ Drop the entire fleet and change the fleet's direction """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,stats,screen,ship,aliens,bullets,fireball):
    """ Respond to ships being hit by alien """

    if stats.ships_left > 0:
        """ Decrement the ships left """
        stats.ships_left -= 1

        """ Empty the list of aliens and bullets """
        aliens.empty()
        bullets.empty()
        fireball.empty()

        """ Create a new fleet and center the ship """
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

        """ Pause (The screen will freeze momentarily and the player will see that the alien has hit the ship) """
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():

        """ An alien reaches the bottom when
        its rect.bottom value is greater than or equal to the screen’s rect.bottom attribute """

        if alien.rect.bottom >= screen_rect.bottom:
            """Treat this the same as if the ship got hit."""
            ship_hit(ai_settings, stats, screen,ship, aliens, bullets)
            break


def update_aliens(ai_settings,stats,screen,ship,aliens,bullets,fireball):
    """
     Check if the fleet is at an edge,
     and then update the postions of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings,aliens)
    aliens.update()



    """ Look for alien-ship collision """
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets,fireball)

        """ The method spritecollideany() takes two arguments: a sprite and a
            group. The method looks for any member of the group that’s collided with
            the sprite and stops looping through the group as soon as it finds one 
            member that has collided with the sprite. Here, it loops through the group aliens
            and returns the fist alien it finds that has collided with ship. """

    #check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_fireball(ai_settings,stats,screen,ship,aliens,bullets,fireball):
    """Update position of bullets and get rid of old bullets."""

    # Update bullet positions.
    fireball.update()

    # Get rid of bullets that have disappeared.
    for fb in fireball.copy():
        if fb.rect.bottom >= screen.get_rect().bottom:
            fireball.remove(fb)
    #print(len(fireball))

    """ Handle collision between fireball and ship """
    if pygame.sprite.spritecollideany(ship,fireball):
        ship_hit(ai_settings,stats,screen,ship,aliens,bullets,fireball)

    #check_bullet_alien_collision(ai_settings, screen,stats,sb, ship, aliens, bullets)