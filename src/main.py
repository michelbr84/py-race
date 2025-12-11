
# The MIT License (MIT)
# Copyright (c) 2012 Robin Duda, (chilimannen)

import sys
import os
import warnings

# Suppress pkg_resources deprecation warning from pygame
warnings.filterwarnings("ignore", category=UserWarning, module="pygame.pkgdata")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pkg_resources")

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
from src.ui.game_over_menu import GameOverMenu
from src.ui.pause_menu import PauseMenu
from src.ui.floating_text import TextManager

# Import UI
from src.ui import pointer, menu, bounds_alert, timeout_alert

def main():
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
        
        screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption('Race of Math')
        
        center_w = resolution[0] // 2
        center_h = resolution[1] // 2
        
        # 1. Run Start Menu
        start_menu_inst = StartMenu(screen, config_mgr, score_mgr)
        menu_result = start_menu_inst.run()
        
        if menu_result is None:
            pygame.quit()
            sys.exit(0)
            
        if menu_result == "RESTART":
            pygame.quit()
            continue
            
        # Seed selected
        seed = menu_result
        
        # 2. Generate Map
        generator.generate_map(seed)

        # 3. Initialize Game Objects
        text_mgr = TextManager()
        target = gamemode.Finish(score_mgr, text_mgr) 
        
        clock = pygame.time.Clock()
        running = True
        paused = False
        font = pygame.font.Font(None, 24)
        
        car = player.Player()
        cam = camera.Camera()
        
        bound_alert_inst = bounds_alert.Alert()
        time_alert_inst = timeout_alert.Alert()
        info = menu.Alert() 
        
        ptr = pointer.Tracker(int(center_w * 2), int(center_h * 2))

        # create sprite groups.
        map_s     = pygame.sprite.Group()
        player_s  = pygame.sprite.Group()
        traffic_s = pygame.sprite.Group()
        tracks_s  = pygame.sprite.Group()
        target_s  = pygame.sprite.Group()
        pointer_s = pygame.sprite.Group()
        
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
        
        # Main Game Loop
        while running:
            # 1. Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        # Toggle Pause
                        paused = True
                        pause_menu = PauseMenu(screen)
                        res = pause_menu.run()
                        if res == "QUIT":
                            pygame.quit()
                            sys.exit(0)
                        elif res == "MENU":
                            running = False # Break inner loop, goes to start menu
                        elif res == "RESUME":
                            paused = False
                            
                    if event.key == pygame.K_m:
                         info.appear()
                         pygame.display.flip()
                         # Small cheat: wait for input or just show? Original code just blitted once.
                         # We'll just let it render this frame or handling logic.
                         # Better logic: set a flag "show_info" and render it at the end.
                         pass

            if not running: break 
            
            # 2. Logic Updates (only if not paused, but loop blocks on pause above)
            
            # Input
            keys = pygame.key.get_pressed()
            if keys[K_UP]: car.accelerate()
            else: car.deaccelerate()
            if keys[K_DOWN]: car.impact()
            if keys[K_LEFT]: car.steerleft()
            if keys[K_RIGHT]: car.steerright()
            
            # Camera
            cam.set_pos(car.x, car.y)
            
            # Offroad check (Simple)
            try:
                tile_x = int(car.x / 1000)
                tile_y = int(car.y / 1000)
                if 0 <= tile_x < 10 and 0 <= tile_y < 10:
                    if maps.map_1[tile_y][tile_x] == 5: # Grass
                        car.grass(100) 
            except: pass

            # Boundaries
            if bound_alert_inst.breaking(car.x, car.y):
                bound_alert_inst.appear()
                car.impact()

            # Time Out Check -> Game Over
            if target.timeleft == 0:
                # Show Game Over
                car.speed = 0
                go_menu = GameOverMenu(screen, target.score, target.high_score_reached)
                go_res = go_menu.run()
                
                if go_res == "QUIT":
                    pygame.quit()
                    sys.exit(0)
                elif go_res == "MENU":
                    running = False 
                elif go_res == "RESTART":
                    # We can either break to outer loop (reload everything) or just reset entities.
                    # Outer loop is safer for full reset.
                    running = False 
                
            # Updates
            map_s.update(cam.x, cam.y)
            player_s.update(cam.x, cam.y)
            traffic_s.update(cam.x, cam.y)
            tracks_s.update(cam.x, cam.y)
            target_s.update(cam.x, cam.y)
            pointer_s.update(car.x, car.y, target.x, target.y)
            text_mgr.update(cam.x, cam.y)

            # Collisions
            if pygame.sprite.spritecollide(car, target_s, False):
                target.claim_flag()
                
            if pygame.sprite.spritecollide(car, traffic_s, False):
                car.impact()
                target.car_crash()
                # car.snd_crash.play() # handled in player

            # 3. Drawing
            screen.fill(COLOR_BG)
            
            map_s.draw(screen)
            tracks_s.draw(screen) # overlay tracks
            
            target_s.draw(screen)
            player_s.draw(screen)
            traffic_s.draw(screen)
            pointer_s.draw(screen)
            
            # Floating Text
            text_mgr.draw(screen, cam.x, cam.y)
            
            # UI Overlays
            text_score = font.render(f'Score: {target.score}', True, COLOR_TEXT)
            screen.blit(text_score, (20, 20))
            
            text_time = font.render(f'Time: {int(target.timeleft / 60)}', True, COLOR_TEXT)
            screen.blit(text_time, (20, 50))
            
            # Info overlay (if M pressed this frame, or permanent toggle?)
            # Original was instantaneous. Let's stick to key check above.
            if keys[K_m]:
                info.appear() # Re-blit simple info
            
            pygame.display.flip()
            clock.tick(60)

if __name__ == '__main__':
    main()
