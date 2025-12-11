
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
from src.core.config_manager import ConfigManager
from src.core.score_manager import ScoreManager

# Import data
from src.data import maps

# Import entities
from src.entities import player, traffic, tracks
from src.entities.map_tile import MapTile

# Import managers
from src.managers import game_manager as gamemode

# Import generator and menu
from src.core import generator
from src.ui.start_menu import StartMenu

# Import UI
from src.ui import pointer, menu, bounds_alert, timeout_alert

def main():
    # Loop for restarts (resolution changes)
    while True:
        # Initialize Managers
        config_mgr = ConfigManager()
        score_mgr = ScoreManager()
        
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()
        
        # Apply Config
        resolution = config_mgr.get("resolution")
        volume = config_mgr.get("volume")
        
        # Set Volume (crude global scaling if possible, or per sound)
        # Pygame mixer doesn't have a global volume for all active sounds easily accessible 
        # without iterating channels, but we can try setting it on loaded sounds or music.
        # For now, we assume user adjusts system volume or we implement a sound manager later.
        # We can try to set a global reserved channel volume? No.
        
        screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption('Race of Math')
        
        # center calculation might depend on resolution
        center_w = resolution[0] // 2
        center_h = resolution[1] // 2
        
        # 1. Run Start Menu
        start_menu_inst = StartMenu(screen, config_mgr, score_mgr)
        menu_result = start_menu_inst.run()
        
        if menu_result is None:
            # Quit
            pygame.quit()
            sys.exit(0)
            
        if menu_result == "RESTART":
            # Restart loop to apply settings
            pygame.quit()
            continue
            
        # Seed selected
        seed = menu_result
        
        # 2. Generate Map
        generator.generate_map(seed)

        # 3. Initialize Game Objects
        # Pass score_mgr to Finish (Game Manager)
        target = gamemode.Finish(score_mgr) 
        
        clock = pygame.time.Clock()
        running = True
        font = pygame.font.Font(None, 24)
        
        car = player.Player()
        cam = camera.Camera()
        
        bound_alert = bounds_alert.Alert()
        time_alert = timeout_alert.Alert()
        info = menu.Alert() # Note: 'menu' here is the in-game alert menu
        
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
        loaded_map_images = []
        for tile_name in maps.map_tile:
            loaded_map_images.append(load_image(tile_name, False))

        for x in range (0, 10):
            for y in range (0, 10):
                tile_index = maps.map_1[x][y]
                rot = maps.map_1_rot[x][y]
                map_s.add(MapTile(loaded_map_images[tile_index], x * 1000, y * 1000, rot))

        # generate traffic
        traffic.initialize(center_w, center_h)
        for _ in range(0, TRAFFIC_COUNT):
            traffic_s.add(traffic.Traffic())

        player_s.add(car)
        target_s.add(target)
        pointer_s.add(ptr)
        bound_alert_s.add(bound_alert)
        timer_alert_s.add(time_alert)
        menu_alert_s.add(info)

        # Main Game Loop
        while running:
            # Render background
            screen.fill(COLOR_BG)
            
            # Input
            keys = pygame.key.get_pressed()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    # Breaks inner loop, goes back to Start Menu (outer loop) because we loop 'main' logic?
                    # No, currently main() has while True.
                    # If we break here, we just restart the whole main() block which shows Start Menu. Perfect.
                    break

            if not running: break # Go back to restart loop (frontend menu)

            if keys[K_UP]:
                car.accelerate()
            else:
                car.deaccelerate()

            if keys[K_DOWN]:
                car.impact()

            if keys[K_LEFT]:
                car.steerleft()

            if keys[K_RIGHT]:
                car.steerright()

            if keys[K_p]:
                car.reset()
                target.reset()
                
            if keys[K_m]:
                info.appear()

            # Logic checks
            cam.set_pos(car.x, car.y)

            # Check for generic boundaries
            # Note: map is 10x10 tiles of 1000px => 0 to 10000
            if bounds_alert.breaking(car.x, car.y):
                bound_alert.appear()
                car.impact()

            if target.timeleft == 0:
                # Force save high score if not done
                time_alert.appear()
                car.speed = 0
                # End or Reset?
                # Original logic just showed alert.
                # We can enforce "Press P to Reset" or auto-reset.
                
            # Updates
            map_s.update(cam.x, cam.y)
            player_s.update(cam.x, cam.y)
            traffic_s.update(cam.x, cam.y)
            tracks_s.update(cam.x, cam.y)
            target_s.update(cam.x, cam.y)
            pointer_s.update(car.x, car.y, target.x, target.y)

            # Check flag collision
            if pygame.sprite.spritecollide(car, target_s, False):
                target.claim_flag()
                # player.score += ? handled in claim_flag
                
            # Check traffic collision
            if pygame.sprite.spritecollide(car, traffic_s, False):
                car.impact()
                target.car_crash()
                # car.snd_crash.play() # Already in car.impact()

            # Offroad check
            # map index logic
            try:
                # Using hardcoded 1000 tile size
                # x index = (car.x + center_w) / 1000 ? No car.x is absolute world pos
                # Original logic access maps via int(car.x / 1000)
                # But car.x is centered? 
                # Let's trust original collision logic or add grass check here if missing from player.
                # player.py has grass(value) method.
                
                # We need to get the pixel value under the car to check for grass color?
                # Or check tile type.
                # Original MAIN.py did: 
                # if (maps.map_1[int(car.y / 1000)][int(car.x / 1000)] == 5): car.grass(255)
                # Let's restore that if it was there.
                
                tile_x = int(car.x / 1000)
                tile_y = int(car.y / 1000)
                if 0 <= tile_x < 10 and 0 <= tile_y < 10:
                    if maps.map_1[tile_y][tile_x] == 5: # 5 is Null/Grass
                        car.grass(100) # Arbitrary high value to trigger
                
            except Exception as e:
                pass

            # Drawing
            map_s.draw(screen)
            tracks_s.draw(screen)
            target_s.draw(screen)
            player_s.draw(screen)
            traffic_s.draw(screen)
            pointer_s.draw(screen)
            
            # UI Overlays
            # Score
            text_score = font.render(f'Score: {target.score}', True, COLOR_TEXT)
            screen.blit(text_score, (20, 20))
            
            # Time
            text_time = font.render(f'Time: {int(target.timeleft / 60)}', True, COLOR_TEXT)
            screen.blit(text_time, (20, 50))

            pygame.display.flip()
            clock.tick(60)

if __name__ == '__main__':
    main()
