from Object import *
from cs1lib import *
from __builtin__ import raw_input

WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1000
SCALE = 5
TILE_SHEET = "spritesheet.png"
TILES = {"Sky1": (32, 24),"Grass1_top": (0, 0), "Grass2_top": (8, 0), "Dirt1_top": (16, 0), "Dirt2_top": (24, 0), "Dirt3_top": (16, 8), "Dirt4_top": (16, 16), "Dirt5_top": (16, 24), "Dirt1_left": (0, 40), "Dirt2_left": (0, 32), "Dirt3_left": (8, 40), "Dirt4_left": (16, 40), "Dirt5_left": (24, 40), "Dirt1_right": (24, 80), "Dirt2_right": (24, 88), "Dirt3_right": (16, 80), "Dirt4_right": (8, 80), "Dirt5_right": (0, 80), "DirtCorner1": (24, 8), "Rock1_top": (0, 8), "Rock2_top": (8, 8), "Tree1": (56, 24), "Tree2": (64, 24), "Tree3": (72, 24), "Tree4": (80, 24), "Branch1_right": (88, 24), "Branch2_right": (96, 24), "Branch3_right": (104, 24), "Black1_top": (24,24)}
TILE_ORDER = ["Sky", "Black", "Grass", "Dirt", "DirtCorner", "Rock", "Tree", "Branch", "Black"]

def map_read(file_name):
    
    #Initialize a list that will contain all map info
    Map = []
    
    entities = [[]]
    
    x = 0
    y = 0
    
    #Open a file for reading
    file = open(file_name, "r")
    
    line = "" #A line of the text
    
    
    collision_reading = True
    first_line = True
    
    set_clear_color(0, 0, 0)
    
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
    """
    temp = []
    line = file.readline()
    line = line.split(";")
    for entity in line:
        if entity != "":
            entity_things = entity.split(",")
            temp.append(Animation(entity_things[1],entity_things[2],entity_things[0]))
    
    entities.append(temp)
    
    line = file.readline()
    line = line.split(";")
    for entity in line:
        if entity != "":
            entity_things = entity.split(",")
            if entity_things[0] == "Player":
                entities.append(Player_entity(int(entity_things[1]),int(entity_things[2]),40))
            elif entity_things[0] == "Tri Flame":
                entities.append(Tri_Flame(int(entity_things[1]),int(entity_things[2]),7))
            elif entity_things[0] == "Flamer":
                entities.append(Flamer(int(entity_things[1]),int(entity_things[2]),40))
            elif entity_things[0] == "Logs":
                entities.append(Logs(int(entity_things[1]),int(entity_things[2])))
    """
    #Closes file
    file.close()
    
    
    Update_Tile_xy(Map) 
    
    return Map, entities

def Map_init():
    #creates the Map list
    Map = []
    
    #Asks for how high and/or wide you want the map to be
    Map_Width = int(raw_input("What Width?"))
    Map_Height = int(raw_input("What Height?"))
    
    #Add as many columns as the Width
    for x in range(Map_Width):
        Map.append([])
        
        #Add as many tiles in those columns as the Height
        for y in range(Map_Height):
            Map[x].append(Tile("Air", "Sky1"))
    
    #Return the 2D list: Map
    return Map

def Update_Tile_xy(Map):
    #For each column
    for column in range(len(Map)):
            
        #For each row in a column
        for row in range(len(Map[column])):
            
            #update the tile's xy coordinates
            Map[column][row].update_tile_xy(column, row)
            
    
"""
def Draw_Tiles(Map, camera_x, camera_y):
    
    
    tile_xl = int((camera_x / 8) - 2)
    tile_yt = int((camera_y / 8) - 2)
    
    tile_xr = int((tile_xl + ((WINDOW_WIDTH / SCALE) / 8)) + 3)
    tile_yb = int((tile_yt + ((WINDOW_HEIGHT / SCALE) / 8)) + 3)
    
    #Load the sprite sheet
    img = load_image(TILE_SHEET)
    
    #For each column
    for column in range(tile_xl, tile_xr + 1):
            
        #For each row in a column
        for row in range(tile_yt, tile_yb + 1):
                
                if (0 <= column <= len(Map) - 1):
                    
                    if (0 <= row <= len(Map[column]) - 1):
                        
                        #Get the x and y coordinates of the tile on the sprite sheet
                        x, y = TILES[Map[column][row].tile]
                        
                        #Draw the tile
                        advanced_draw_image(img, Map[column][row].xl, Map[column][row].yt, x, y, 8, 8, SCALE, camera_x*SCALE, camera_y*SCALE)
"""
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

def Write_To_Text(Map, entities, file):
    file = open(file, "w")
    line_storage = ""
    
    #collision writing
    for y in range(len(Map[0])):
        for x in Map:
            if (0 <= y <= len(x) - 1):
                
                if x[y].tile_type == "Air":
                    line_storage = line_storage + "0"
                elif x[y].tile_type == "Solid":
                    line_storage = line_storage + "1" 
        file.write(line_storage + "\n")
        line_storage = ""
        
    file.write("~" + "\n")
    
    #tile writing
    for y in range(len(Map[0])):
        for x in Map:
            if (0 <= y <= len(x) - 1):
                line_storage = line_storage + x[y].tile + ","
            
        file.write(line_storage + "\n")
        line_storage = ""
    
    file.write("~")
    """
    for entity in entities[0]:
        line_storage = line_storage + entity.current_sprite_type + "," + str(entity.xl) + "," + str(entity.yt) + ";"
    
    file.write(line_storage + "\n")
    line_storage = ""
    
    for entity in entities:
        if entities.index(entity) != 0:
            line_storage = line_storage + entity.type + "," + str(entity.xl) + "," + str(entity.yt) + ";"
    
    file.write(line_storage)
    file.write("~")
    """
    #close text file
    file.close()

def main():
    
    current_tile_range = "Grass"
    current_tile_type = "Solid"
    current_tile = "Grass1_top"
    current_tile_number = 1
    current_tile_direction = "top"
    
    camera_x = 0
    camera_y = 0
    
    file = "Map1.txt"
    
    #creates the Map list
    Map = []
    
    if raw_input("Load file?(y or n)") == "y":
        file = raw_input("Which file?")
        Map, entity_list = map_read(file)
    
    else:
        #Asks for how high and/or wide you want the map to be
        Map_Width = int(raw_input("What Width?"))
        Map_Height = int(raw_input("What Height?"))
    
        #Add as many columns as the Width
        for x in range(Map_Width):
            Map.append([])
            
            #Add as many tiles in those columns as the Height
            for y in range(Map_Height):
                Map[x].append(Tile("Air", "Sky1"))
    
    Update_Tile_xy(Map)
    
    tile_selection = True
    current_entity_type = "Player"
    current_animation_type = "tree fire"
    
    #While the window is not closed
    while not window_closed():
        
        clear()
        
        Draw(Map, entity_list, camera_x, camera_y)
        
        request_redraw()
        sleep(0.05)
        
        #gets the x and y cordinates of the mouse
        mousex = mouse_x()
        mousey = mouse_y()
        
        #if the mouse had clicked
        if mouse_down():
            
            #modifies mousex and y so that it corresponds with the camera position, and the scale
            mousex = (mousex/SCALE) + camera_x
            mousey = (mousey/SCALE) + camera_y
            
            
    
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
                            #if the mouse is inside the tile when clicked, change that tile
                            if Map[column][row].collide(mousex, mousex, mousey, mousey):
                                
                                if tile_selection == True:
                                    Map[column][row].tile_type = current_tile_type
                                    Map[column][row].tile = current_tile
                                    
                                elif tile_selection == False:
                                    
                                    if current_entity_type == "Player":
                                    
                                        entity_list.append(Player_entity(Map[column][row].xl, Map[column][row].yt, 40))
                                                       
                                    elif current_entity_type == "Tri Flame":
                                        
                                        entity_list.append(Tri_Flame(Map[column][row].xl, Map[column][row].yt, 7))
                                        
                                    elif current_entity_type == "Flamer":
                                        
                                        entity_list.append(Flamer(Map[column][row].xl, Map[column][row].yt, 5))
                                        
                                    elif current_entity_type == "Logs":
                                        
                                        entity_list.append(Logs(Map[column][row].xl, Map[column][row].yt, 5))
                                        
                                    elif current_entity_type == "Animation":
                                        entity_list[0].append(Animation(Map[column][row].xl, Map[column][row].yt, current_animation_type))
                                    
                                    elif current_entity_type == "Erase":
                                        
                                        for entity in entity_list:
                                            if entity.collide(mousex, mousex, mousey, mousey):
                                                del entity_list[entity_list.index(entity)]
         
        if is_key_pressed("a"):
            camera_x -= 4
            
        if is_key_pressed("d"):
            camera_x += 4
            
        if is_key_pressed("w"):
            camera_y -= 4
            
        if is_key_pressed("s"):
            camera_y += 4
            
        if is_key_pressed("l"):
            if TILE_ORDER.index(current_tile_range) > len(TILE_ORDER) - 1:
                current_tile_range = TILE_ORDER[len(TILE_ORDER) - 1]
                
            else:
                current_tile_range = TILE_ORDER[TILE_ORDER.index(current_tile_range) + 1]
        
            print current_tile_range
        
        if is_key_pressed("k"):
            if TILE_ORDER.index(current_tile_range) < 0:
                current_tile_range = TILE_ORDER[0]
            else:
                current_tile_range = TILE_ORDER[TILE_ORDER.index(current_tile_range) - 1]
                
            print current_tile_range
            
        
        if is_key_pressed("p"):
            current_tile_number += 1
            print "tile number" + str(current_tile_number)
        
        if is_key_pressed("o"):
            current_tile_number -= 1
            print "tile number" + str(current_tile_number)
            
        if is_key_pressed("t"):
            current_tile_direction = "top"
            print "top"
            
        if is_key_pressed("g"):
            current_tile_direction = "bottom"
            print "bottom"
            
        if is_key_pressed("f"):
            current_tile_direction = "left"
            print "left"
            
        if is_key_pressed("h"):
            current_tile_direction = "right"
            print "right"
            
        if is_key_pressed("1"):
            current_tile_type = "Air"
            print "Air"
            
        if is_key_pressed("2"):
            current_tile_type = "Solid"
            print "Solid"
            
        if is_key_pressed("3"):
            
            #gets the x and y cordinates of the mouse
            mousex = mouse_x()
            mousey = mouse_y()
            mousex = (mousex/SCALE) + camera_x
            mousey = (mousey/SCALE) + camera_y
            print "X:" + str(mousex)
            print "Y:" + str(mousey)
        
        if is_key_pressed("4"):
            tile_selection = False
            
        if is_key_pressed("5"):
            tile_selection = True
        
        if is_key_pressed("6"):
            current_entity_type = raw_input("what entity?")
            
        if is_key_pressed("7"):
            current_animation_type = raw_input("what animation")
        
        if (current_tile_range + str(current_tile_number) + "_" + current_tile_direction) in TILES.keys():
            current_tile = current_tile_range + str(current_tile_number) + "_" + current_tile_direction
            
        elif current_tile_range + str(current_tile_number) in TILES.keys():
            current_tile = current_tile_range + str(current_tile_number)
        
        else:
            print "could not find: " + current_tile_range + str(current_tile_number) + "_" + current_tile_direction + " in dictionary"
         
        
    #once the program is done running, save to the Map file 
    Write_To_Text(Map, entity_list, file)
    
            
    
start_graphics(main, "TSA_Game Map Maker", WINDOW_WIDTH, WINDOW_HEIGHT)