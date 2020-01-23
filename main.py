from Object import *
from time import *
import random
from itertools import count
from cs1lib import *
import winsound

LEVEL_ONE = "Map1.txt"
LEVEL_TWO = "Map2.txt"
LEVEL_THREE = "Map3.txt"
LEVEL_FOUR = "Map4.txt"

WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1000
SCALE = 6
TILE_SHEET = "spritesheet.png"

TILES = {"Sky1": (32, 24),"Grass1_top": (0, 0), "Grass2_top": (8, 0), "Dirt1_top": (16, 0), "Dirt2_top": (24, 0), "Dirt3_top": (16, 8), "Dirt4_top": (16, 16), "Dirt5_top": (16, 24), "Dirt1_left": (0, 40), "Dirt2_left": (0, 32), "Dirt3_left": (8, 40), "Dirt4_left": (16, 40), "Dirt5_left": (24, 40), "Dirt1_right": (24, 80), "Dirt2_right": (24, 88), "Dirt3_right": (16, 80), "Dirt4_right": (8, 80), "Dirt5_right": (0, 80), "DirtCorner1": (24, 8), "Rock1_top": (0, 8), "Rock2_top": (8, 8), "Tree1": (56, 24), "Tree2": (64, 24), "Tree3": (72, 24), "Tree4": (80, 24), "Branch1_right": (88, 24), "Branch2_right": (96, 24), "Branch3_right": (104, 24), "Black1_top": (24,24)}

def Update_Tile_xy(Map):
    #For each column
    for column in range(len(Map)):
            
        #For each row in a column
        for row in range(len(Map[column])):
            
            #update the tile's xy coordinates
            Map[column][row].update_tile_xy(column, row)

def map_read(file_name):
    
    #Initialize a list that will contain all map info
    Map = []
    
    x = 0
    y = 0
    
    #Open a file for reading
    file = open(file_name, "r")
    
    line = "" #A line of the text
    
    
    collision_reading = True
    first_line = True
    
    while collision_reading == True:
        line = file.readline()
        
        #print(line) #for debugging
        
        #Make the columns for the 2D list
        if first_line == True:
            for character in line:
                Map.append([])
            first_line = False
        
        for character in line:
            
            #If the tile is meant to be air(shown by putting 0) append a Tile object with the air attribute
            if character == "0":
                
                Map[x].append(Tile("Air", "Sky1"))
                
            #If the tile is meant to be solid(shown by putting 1) append a Tile object with the solid attribute
            elif character == "1":
                
                Map[x].append(Tile("Solid", "Grass1"))
                
            #If the collision map ends, stop reading for collision
            elif character == "~":
                
                collision_reading = False
            
            x += 1
        
        x = 0
        
    x = 0
    #Start reading tile types
    tile_reading = True
    
    while tile_reading == True:
        
        line = file.readline()
        
        line = line.split(",")
        #print line
        
        
        for tile_type in line:
            
            if tile_type == "~":
                tile_reading = False
            
            elif tile_type != "\n":
                Map[x][y].tile = tile_type
            
            x += 1
            
        x = 0
        
        y += 1
    
    #Closes file
    file.close()
    
    
    Update_Tile_xy(Map) 
    
    return Map


def Draw(Map, entity_list, camera_x, camera_y):
    
    tile_xl = int((camera_x / 8) - 2)
    tile_yt = int((camera_y / 8) - 2)
    
    tile_xr = int((tile_xl + ((WINDOW_WIDTH / SCALE) / 8)) + 3)
    tile_yb = int((tile_yt + ((WINDOW_HEIGHT / SCALE) / 8)) + 3)
    
    #Load the sprite sheet
    img = load_image(TILE_SHEET)
    
    #For each column
    for column in range(tile_xl + 1, tile_xr + 1):
            
        #For each row in a column
        for row in range(tile_yt + 1, tile_yb + 1):
                
                if (0 <= column <= len(Map) - 1):
                    
                    if (0 <= row <= len(Map[column]) - 1):
                        
                        #Get the x and y coordinates of the tile on the sprite sheet
                        x, y = TILES[Map[column][row].tile]
                        
                        #Draw the tile
                        advanced_draw_image(img, Map[column][row].xl, Map[column][row].yt, x, y, 8, 8, SCALE, camera_x*SCALE, camera_y*SCALE)
    
    for entity in entity_list:
        
        if entity_list.index(entity) != 0:
        
            #if the entity is within the camera
            if ((entity.xl - camera_x >= -8) or (entity.xr - camera_x >= -8)) and ((entity.yt - camera_y >= -8) or (entity.yb - camera_y >= -8)):
            
                
                #junk is not used, is just there to catch an extra value from the tuple
                x, y, width, height, junk = entity.current_sprite
                
                
                advanced_draw_image(img, entity.draw_x, entity.draw_y, x, y, width, height, SCALE, camera_x*SCALE, camera_y*SCALE)
    
    for entity in entity_list[0]:
        #if the entity is within the camera
        if ((entity.xl - camera_x >= -8) or (entity.xr - camera_x >= -8)) and ((entity.yt - camera_y >= -8) or (entity.yb - camera_y >= -8)):
        
            
            #junk is not used, is just there to catch an extra value from the tuple
            x, y, width, height, junk = entity.current_sprite
            
            
            advanced_draw_image(img, entity.xl, entity.yt, x, y, width, height, SCALE, camera_x*SCALE, camera_y*SCALE)
        
        
    #old drawing code
    """
    #For each column
    for column in Map:
            
        #For each row in a column
        for row in column:
            
            #if the tile is within the camera or a little outside it
            if ((row.xl - camera_x >= -8) or (row.xr - camera_x >= -8)) and ((row.yt - camera_y >= -8) or (row.yb - camera_y >= -8)):
                
                #Get the x and y coordinates of the tile on the sprite sheet
                x, y = TILES[row.tile]
                
                #Draw the tile
                advanced_draw_image(img, row.xl, row.yt, x, y, 8, 8, SCALE, camera_x*SCALE, camera_y*SCALE)
                
    
    for entity in entity_list:
        
        #if the entity is within the camera
        if ((entity.xl - camera_x >= -8) or (entity.xr - camera_x >= -8)) and ((entity.yt - camera_y >= -8) or (entity.yb - camera_y >= -8)):
        
            
            #junk is not used, is just there to catch an extra value from the tuple
            x, y, width, height, junk = entity.current_sprite
            
            
            advanced_draw_image(img, int(entity.xl), int(entity.yt), x, y, width, height, SCALE, camera_x*SCALE, camera_y*SCALE)
    """

def Map_collision(Map, entity, camera_x, camera_y):
    tile_xl = int((camera_x / 8) - 2)
    tile_yt = int((camera_y / 8) - 2)
    
    tile_xr = int((tile_xl + ((WINDOW_WIDTH / SCALE) / 8)) + 3)
    tile_yb = int((tile_yt + ((WINDOW_HEIGHT / SCALE) / 8)) + 3)
    
    #For each column
    for column in range(tile_xl, tile_xr + 1):
            
        #For each row in a column
        for row in range(tile_yt, tile_yb + 1):
                
                if (0 <= column <= len(Map) - 1):
                    
                    if (0 <= row <= len(Map[column]) - 1):
                        
                        if Map[column][row].collide(entity.xl, entity.xr, entity.yt, entity.yb) and Map[column][row].tile_type == "Solid":
                            
                            entity.collision_handler("Tile", Map[column][row])
                            
                        elif Map[column][row].collide(entity.xl, entity.xr, entity.yt, entity.yb + 1) and Map[column][row].tile_type == "Solid":
                            entity.in_air = False

def Entity_collision(entities, target_entity):
    
    for entity in entities:
        if entities.index(entity) != 0:
            if entity.collide(target_entity.xl, target_entity.xr, target_entity.yt, target_entity.yb):
                target_entity.collision_handler(entity.type, entity)
            
            if target_entity.type == "Player" and entity.type == "Flamer" and entity.collide(target_entity.xl, target_entity.xr, target_entity.yt, target_entity.yb + 1):
                target_entity.in_air = False
            


def Update_entities(Map, entities, camera_x, camera_y, tick):
    
    for entity in entities:
        if entities.index(entity) != 0:
            if (((entity.xl - camera_x >= -8) and (entity.xr - camera_x <= 1000/SCALE)) and ((entity.yt - camera_y >= -8) or (entity.yb - camera_y >= -8)) or entity.type == "Player"):
            
                entity.in_air = True
            
                entity.update_xy()
                Map_collision(Map, entity, camera_x, camera_y)
                Entity_collision(entities, entity)
                
                entity.gravity()
                
                entity.draw_x = entity.xl
                entity.draw_y = entity.yt
                
                if entity.type == "Flamer":
                    projectile = entity.fire_projectile(tick, entities[1])
                    if projectile != None:
                        entities.append(projectile)
                        
                if entity.type == "Player":
                    entities[2].xl, entities[2].yt = entity.Attack() 
                
                if entity.health == 0:
                    if entity.type == "Player":
                        return True
                    elif entity.type != "Death":
                        entities.append(Death(entity.xl,entity.yt))
                        del entities[entities.index(entity)]
                        
                    else:
                        del entities[entities.index(entity)]
                        
                entity.animation_update(tick)
    for entity in entities[0]:
        entity.animation_update(tick)

def main():
    
    Game_Over = False
    
    camera_x = 0
    camera_y = 0
    
    entity_list = [[Animation(880, 160, "tree fire"),Animation(1000, 198, "tree fire"),Animation(1144, 208, "tree fire")], Player_entity(152, 258, 10), Sword(-100, -100), Tri_Flame(936, 216, 7), Flamer(290,232,10), Logs(648, 320), Logs(648, 288), Logs(648, 256), Logs(648, 224), Win_Goal(1190, 147)]
    
    Map = map_read(LEVEL_ONE)
    
    attack_button_held = False
    
    set_clear_color(0, 0, 0)
    
    while not window_closed():
        
        if Game_Over == True:
            
            fps = 35
            loop_delta = 1./fps
            
            current_time = target_time = clock()
            
            #Clear screen, draw, then sleep
            clear()
            
            advanced_draw_image(load_image(TILE_SHEET), 0, 0, 32, 32, 91, 32, SCALE, 0, 0)
            advanced_draw_image(load_image(TILE_SHEET), 32, 32, 123, 32, 85, 32, SCALE, 0, 0)
            
            request_redraw()
            
            #find how long to sleep for
            target_time += loop_delta
            sleep_time = target_time - clock()
            
            #sleep
            if sleep_time > 0:
                sleep(sleep_time)
            else:
                print 'took too long' + str(sleep_time)
                
            if is_key_pressed("k") or is_key_pressed("l") or is_key_pressed("a") or is_key_pressed("d"):
                camera_x = 0
                camera_y = 0
                
                entity_list = [[Animation(100, 100, "tree fire")], Player_entity(100, 9, 10), Sword(-100, -100), Tri_Flame(200, 248, 10), Flamer(290,232,10), Logs(376, 212), ]
                
                Map = map_read(LEVEL_ONE)
                
                attack_button_held = False
                
        elif entity_list[1].win == True:
            fps = 35
            loop_delta = 1./fps
            
            current_time = target_time = clock()
            
            #Clear screen, draw, then sleep
            clear()
            
            advanced_draw_image(load_image(TILE_SHEET), 0, 0, 87, 97, 127, 31, SCALE, 0, 0)
            
            request_redraw()
            
            #find how long to sleep for
            target_time += loop_delta
            sleep_time = target_time - clock()
            
            #sleep
            if sleep_time > 0:
                sleep(sleep_time)
            else:
                print 'took too long' + str(sleep_time)

        else:
        
            fps = 35
            loop_delta = 1./fps
            
            current_time = target_time = clock()
            
            
            #Clear screen, draw, then sleep
            clear()
            Draw(Map, entity_list, camera_x, camera_y)
            request_redraw()
            
            
            
            #Keypress handling
            
            #if you stop holding a movement button, stop teh character
            if (not is_key_pressed("a")) and (not is_key_pressed("d")):
                entity_list[1].change_x = 0
            
            if is_key_pressed("a") and entity_list[1].change_x >= -2:
                entity_list[1].change_x -= 1
            
            elif is_key_pressed("d") and entity_list[1].change_x <= 2:
                entity_list[1].change_x += 1
                
            elif entity_list[1].change_x > 0:
                entity_list[1].change_x -= 1
                
            elif entity_list[1].change_x < 0:
                entity_list[1].change_x += 1
                
            if entity_list[1].change_x == 3:
                entity_list[1].change_x = 2
            
            if entity_list[1].change_x == -3:
                entity_list[1].change_x = -2
            
            if is_key_pressed("s"):
                entity_list[0].crouch = True
                
            
             
            #For debugging collision   
            #if entity_list[0].change_x < 2:
            #    entity_list[0].change_x += 1
                
            if is_key_pressed("l") and entity_list[1].in_air == False:
                entity_list[1].change_y = -6
                
            if is_key_pressed("k") and attack_button_held == False:
                entity_list[1].attack = True
                attack_button_held = True
                
            elif not is_key_pressed("k"):
                attack_button_held = False
                
            """
            if entity_list[0].change_x > 2:
                entity_list[0].change_x -= 0.2
                
            if entity_list[0].change_x < -2:
                entity_list[0].change_x += 0.2
            """  
            Game_Over = Update_entities(Map, entity_list, camera_x, camera_y, loop_delta)

            
            
            camera_x = entity_list[1].xl - ((WINDOW_WIDTH/2)/SCALE)
            camera_y = entity_list[1].yt - ((WINDOW_HEIGHT/2)/SCALE)

        
        
            #find how long to sleep for
            target_time += loop_delta
            sleep_time = target_time - clock()
            
            #sleep
            if sleep_time > 0:
                sleep(sleep_time)
            else:
                print 'took too long' + str(sleep_time)

            
            #winsound.PlaySound("Action_opening_theme.wav", winsound.SND_ASYNC)
        
start_graphics(main, "Forest Fire", WINDOW_WIDTH, WINDOW_HEIGHT)

        
