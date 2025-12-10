
# The MIT License (MIT)
# Copyright (c) 2012 Robin Duda, (chilimannen)

import sys
import os
import pygame
from pygame.locals import *

# Add project root to sys.path so we can import 'src'
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import settings
from src.core.settings import TRAFFIC_COUNT, COLOR_BG, COLOR_TEXT

# Import core modules
from src.core import camera
from src.core.loader import load_image

# Import data
from src.data import maps

# Import entities
from src.entities import player, traffic, tracks
from src.entities.map_tile import MapTile

# Import managers
from src.managers import game_manager as gamemode

# Import UI
from src.ui import pointer, menu, bounds_alert, timeout_alert

# Main function.
def main():
    # initialize objects.
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font(None, 24)
    car = player.Player()
    cam = camera.Camera()
    target = gamemode.Finish()
    bound_alert = bounds_alert.Alert()
    time_alert = timeout_alert.Alert()
    info = menu.Alert()
    
    # Calculate center based on current display
    center_w = int(pygame.display.Info().current_w / 2)
    center_h = int(pygame.display.Info().current_h / 2)
    
    ptr = pointer.Tracker(int(center_w * 2), int(center_h * 2))

    # create sprite groups.
    map_s     = pygame.sprite.Group()
    player_s  = pygame.sprite.Group()
    traffic_s = pygame.sprite.Group()
    tracks_s  = pygame.sprite.Group()
    target_s  = pygame.sprite.Group()
    pointer_s = pygame.sprite.Group()
    timer_alert_s = pygame.sprite.Group()
    bound_alert_s = pygame.sprite.Group()
    menu_alert_s = pygame.sprite.Group()

    # generate tiles
    # Load map images locally to this scope or use a resource manager. 
    # For now, we load them into a list as per original logic but cleaner.
    loaded_map_images = []
    for tile_name in maps.map_tile:
        loaded_map_images.append(load_image(tile_name, False))

    for x in range (0, 10):
        for y in range (0, 10):
            tile_index = maps.map_1[x][y]
            rot = maps.map_1_rot[x][y]
            # Create MapTile with the specific image
            map_s.add(MapTile(loaded_map_images[tile_index], x * 1000, y * 1000, rot))

    # load tracks
    tracks.initialize()
    # load finish
    target_s.add(target)
    # load direction
    pointer_s.add(ptr)
    # load alerts
    timer_alert_s.add(time_alert)
    bound_alert_s.add(bound_alert)
    menu_alert_s.add(info)
    # load traffic
    traffic.initialize(center_w, center_h)
    for count in range(0, TRAFFIC_COUNT):
        traffic_s.add(traffic.Traffic())

    player_s.add(car)

    cam.set_pos(car.x, car.y)

    while running:
        # Render loop.

        # Check for menu/reset, (keyup event - trigger ONCE)
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if keys[K_m]:
                    if (info.visibility == True):
                        info.visibility = False
                    else:
                        info.visibility = True
                if (keys[K_p]):
                    car.reset()
                    target.reset()
                if (keys[K_q]):
                    pygame.quit()
                    sys.exit(0)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                break

        # Check for key input. (KEYDOWN, trigger often)
        keys = pygame.key.get_pressed()
        if (target.timeleft > 0):
            if keys[K_LEFT]:
                car.steerleft()
            if keys[K_RIGHT]:
                car.steerright()
            if keys[K_UP]:
                car.accelerate()
            else:
                car.soften()
            if keys[K_DOWN]:
                car.deaccelerate()

        cam.set_pos(car.x, car.y)

        # Show text data.
        text_fps = font.render('FPS: ' + str(int(clock.get_fps())), 1, COLOR_TEXT)
        textpos_fps = text_fps.get_rect(centery=25, centerx=60)

        text_score = font.render('Score: ' + str(target.score), 1, COLOR_TEXT)
        textpos_score = text_fps.get_rect(centery=45, centerx=60)

        text_timer = font.render('Timer: ' + str(int((target.timeleft / 60)/60)) + ":" + str(int((target.timeleft / 60) % 60)), 1, COLOR_TEXT)
        textpos_timer = text_fps.get_rect(centery=65, centerx=60)

        # Render Scene.
        screen.blit(background, (0,0))

        map_s.update(cam.x, cam.y)
        map_s.draw(screen)
        
        # Conditional renders/effects
        # We need to get the color at player center relative to screen?
        # Original code: screen.get_at(((int(CENTER_W-5), int(CENTER_H-5)))).g
        # CENTER_W is half screen width.
        # This checks the pixel color at the center of the screen (where the car is presumed to be fixed in camera view?)
        # Yes, car is at center.
        try:
            car.grass(screen.get_at(((int(center_w-5), int(center_h-5)))).g)
        except IndexError:
            pass # Avoid crash if out of bounds (shouldn't happen in fullscreen)

        if (car.tracks):
            tracks_s.add(tracks.Track(cam.x + center_w, cam.y + center_h, car.dir))

        # Just render..
        tracks_s.update(cam.x, cam.y)
        tracks_s.draw(screen)
        
        player_s.update(cam.x, cam.y)
        player_s.draw(screen)

        traffic_s.update(cam.x, cam.y)
        traffic_s.draw(screen)

        target_s.update(cam.x, cam.y)
        target_s.draw(screen)

        pointer_s.update(car.x + center_w, car.y + center_h, target.x, target.y)
        pointer_s.draw(screen)

        # Conditional renders.
        if (bounds_alert.breaking(car.x+center_w, car.y+center_h) == True):
            bound_alert_s.update()
            bound_alert_s.draw(screen)
        if (target.timeleft == 0):
            timer_alert_s.draw(screen)
            car.speed = 0
            text_score = font.render('Final Score: ' + str(target.score), 1, COLOR_TEXT)
            textpos_score = text_fps.get_rect(centery=center_h+56, centerx=center_w-20)
        if (info.visibility == True):
            menu_alert_s.draw(screen)
            
        # Blit Blit..       
        screen.blit(text_fps, textpos_fps)
        screen.blit(text_score, textpos_score)
        screen.blit(text_timer, textpos_timer)
        pygame.display.flip()

        # Check collision!!!
        if pygame.sprite.spritecollide(car, traffic_s, False):
            car.impact()
            target.car_crash()

        if pygame.sprite.spritecollide(car, target_s, True):
            target.claim_flag()
            target.generate_finish()
            target_s.add(target)
            
        clock.tick(64)
        

# initialization
pygame.init()

screen = pygame.display.set_mode((pygame.display.Info().current_w,
                                  pygame.display.Info().current_h),
                                  pygame.FULLSCREEN)


pygame.display.set_caption('Race of Math.')
pygame.mouse.set_visible(False)
font = pygame.font.Font(None, 24)

# New background surface
background = pygame.Surface(screen.get_size())
background = background.convert_alpha()
background.fill(COLOR_BG)

if __name__ == "__main__":
    main()

pygame.quit()
sys.exit(0)
