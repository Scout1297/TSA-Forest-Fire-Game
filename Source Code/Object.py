class Object():
    
    def __init__(self):
        
        self.xl = 0
        self.xr = 0
        self.yt = 0
        self.yb = 0
        
        
    def collide_top(self, previous_entity_yb):
        
        if previous_entity_yb <= self.yt:
            return True
        
        else:
            return False
    
    def collide_bottom(self, previous_entity_yt):
        
        if previous_entity_yt >= self.yb:
            return True
        
        else:
            return False
    
    def collide_left(self, previous_entity_xr):
        
        if previous_entity_xr <= self.xl:
            return True
        
        else:
            return False

    def collide_right(self, previous_entity_xl):
        
        if previous_entity_xl >= self.xr:
            return True
        
        else:
            return False
        
    def collide(self, pxl, pxr, pyt, pyb):
        
        if (pxl < self.xr) and (pxr > self.xl) and (pyt < self.yb) and (pyb > self.yt):
            return True
        
        else:
            return False
    
    

class Tile(Object):
    
    def __init__(self, tile_type, tile):
        
        self.xl = 0
        self.xr = 0
        self.yt = 0
        self.yb = 0
        
        self.rotation = 90
        
        self.tile_type = tile_type
        self.tile = tile
        
    
    def update_tile_xy(self, tile_x, tile_y):
        
        self.xl = tile_x * 8 
            
        self.yt = tile_y * 8 
        
        #Updates the rightmost x point according to the leftmost x point
        self.xr = self.xl + 8
        #Updates the bottommost y point according to the topmost y point
        self.yb = self.yt + 8
        
class Tri_Flame(Object):
    
    def __init__(self, x, y, health):
        
        self.type = "Tri Flame"
        
        self.xl = x
        self.xr = 0
        self.yt = y
        self.yb = 0
        
        self.previous_xl = 0
        self.previous_xr = 0
        self.previous_yt = 0
        self.previous_yb = 0
        
        self.change_x = -1.0
        self.change_y = 0.0
        
        self.draw_x = 0
        self.draw_y = 0
        
        self.width = 16
        self.height = 16
        
        self.health = health
        
        self.img = "Player_Sheet.png"
        
        self.animation_queue = [(112,64,16,16,0.1),(96,64,16,16,0.1),(80,64,16,16,0.1)]
        
        self.current_sprite = self.animation_queue.pop()
        
        self.current_sprite_type = "running_right"
        
    def collision_handler(self, other_object_type, other_object):
        
        #if the player is colliding with a tile
        if other_object_type == "Tile":
            
            if other_object.collide_left(self.previous_xr) and not self.yb <= other_object.yt and not self.yt >= other_object.yb:
                self.change_x = -1
                print "left collide"
                
            if other_object.collide_right(self.previous_xl) and not self.yb <= other_object.yt and not self.yt >= other_object.yb: 
                self.change_x = 1
                print "right collide"
                
            #Updates the rightmost x point according to the leftmost x point
            self.xr = self.xl + self.width
            #Updates the bottommost y point according to the topmost y point
            self.yb = self.yt + self.height
            
        elif other_object_type == "Sword":
            
            self.health -= 1
                    

    def gravity(self):
        return None

    def update_xy(self):
        
        #make the current values the old values
        self.previous_xl = self.xl
        self.previous_xr = self.xr
        self.previous_yt = self.yt
        self.previous_yb = self.yb
        
        
        self.xl += self.change_x
        
        self.yt += self.change_y
        
        self.draw_x = self.xl
        self.draw_y = self.yt
        
        #Updates the rightmost x point according to the leftmost x point
        self.xr = self.xl + self.width
        #Updates the bottommost y point according to the topmost y point
        self.yb = self.yt + self.height

    def animation_update(self, tick):
        
        #if the character is running right
        if self.change_x > 0 and self.current_sprite_type != "running_right":
            self.current_sprite_type = "running_right"
            self.animation_queue = [(112,64,16,16,0.1),(96,64,16,16,0.1),(80,64,16,16,0.1)]
            self.current_sprite = self.animation_queue.pop()
        
        #if the character is running left
        if self.change_x < 0 and self.current_sprite_type != "running_left":
            self.current_sprite_type = "running_left"
            self.animation_queue = [(64,64,16,16,0.1),(48,64,16,16,0.1),(32,64,16,16,0.1)]
            self.current_sprite = self.animation_queue.pop()
                

                
        x, y, width, height, time = self.current_sprite
        
        time = time - tick
        
        if time <= 0:

            #if there is no more frames left in the current cycle of the animation
            if len(self.animation_queue) == 0:
                
                if self.current_sprite_type == "running_right":
                    self.animation_queue = [(112,64,16,16,0.1),(96,64,16,16,0.1),(80,64,16,16,0.1)]
                
                elif self.current_sprite_type == "running_left":
                    self.animation_queue = [(64,64,16,16,0.1),(48,64,16,16,0.1),(32,64,16,16,0.1)]
                             
                   
                self.current_sprite = self.animation_queue.pop()
            
            else:
                self.current_sprite = self.animation_queue.pop()
            
            
        else:
            self.current_sprite = (x, y, width, height, time)

class Flamer(Object):
    
    def __init__(self, x, y, health):
        
        self.type = "Flamer"
        
        self.xl = x
        self.xr = 0
        self.yt = y
        self.yb = 0
        
        self.previous_xl = 0
        self.previous_xr = 0
        self.previous_yt = 0
        self.previous_yb = 0
        
        self.draw_x = 0
        self.draw_y = 0
        
        self.width = 16
        self.height = 32
        
        self.fire_time = 2.0
        
        self.health = health
        
        self.img = "Player_Sheet.png"
        
        self.animation_queue = []
        
        self.current_sprite = (208,32,16,32,0.08)
        
        self.current_sprite_type = "running_right"
        
    def collision_handler(self, other_object_type, other_object):
        return None

    def gravity(self):
        return None

    def update_xy(self):
        #make the current values the old values
        self.previous_xl = self.xl
        self.previous_xr = self.xr
        self.previous_yt = self.yt
        self.previous_yb = self.yb
        
        self.draw_x = self.xl
        self.draw_y = self.yt
        
        #Updates the rightmost x point according to the leftmost x point
        self.xr = self.xl + self.width
        #Updates the bottommost y point according to the topmost y point
        self.yb = self.yt + self.height

    def fire_projectile(self, tick, Player):
        self.fire_time -= tick
        
        if self.fire_time <= 0.0:
            
            self.fire_time = 2.0
            
            if Player.xl >= self.xr:
                return Flamer_Projectile(self.xr - 1, self.yt + 2, 1)
            
            if Player.xr <= self.xl:
                return Flamer_Projectile(self.xl + 1, self.yt + 2, -1)
            
            else:
                return Flamer_Projectile(self.xl - 1, self.yt + 2, 1)
            
        else:
            return None

    def animation_update(self, tick):
                
        x, y, width, height, time = self.current_sprite
        
        time = time - tick
        
        if time <= 0:

            self.current_sprite = (208,32,16,32,0.08)
            
        else:
            self.current_sprite = (x, y, width, height, time)

class Flamer_Projectile(Object):
    
    def __init__(self, x, y, direction):
        
        self.type = "Flamer Projectile"
        
        self.xl = x
        self.xr = 0
        self.yt = y
        self.yb = 0
        
        self.previous_xl = 0
        self.previous_xr = 0
        self.previous_yt = 0
        self.previous_yb = 0
        
        self.change_x = direction
        self.change_y = 0.0
        
        self.draw_x = 0
        self.draw_y = 0
        
        self.width = 8
        self.height = 8
        
        self.health = 2
        
        self.current_sprite = (32,96,8,8,0.08)
        
        self.current_sprite_type = "running_right"
        
    def collision_handler(self, other_object_type, other_object):
        if other_object_type == "Player" or other_object_type == "Sword" or other_object_type == "Tile":
            self.health = 0
        

    def gravity(self):
        return None

    def update_xy(self):
        #make the current values the old values
        self.previous_xl = self.xl
        self.previous_xr = self.xr
        self.previous_yt = self.yt
        self.previous_yb = self.yb
        
        
        self.xl += self.change_x
        
        self.yt += self.change_y
        
        self.draw_x = self.xl
        self.draw_y = self.yt
        
        #Updates the rightmost x point according to the leftmost x point
        self.xr = self.xl + self.width
        #Updates the bottommost y point according to the topmost y point
        self.yb = self.yt + self.height
     
    def animation_update(self, tick):
        
        x, y, width, height, time = self.current_sprite
        
        time = time - tick
        
        if time <= 0:

            self.current_sprite = (32,96,8,8,0.08)
            
        else:
            self.current_sprite = (x, y, width, height, time)
     
class Sword(Object):
    
    def __init__(self, xl, yt):
        
        self.type = "Sword"
        
        self.xl = xl
        self.xr = 0
        self.yt = yt
        self.yb = 0
        
        self.previous_xl = 0
        self.previous_xr = 0
        self.previous_yt = 0
        self.previous_yb = 0
        
        self.draw_x = self.xl
        self.draw_y = self.yt
        
        self.width = 12
        self.height = 32
        
        self.rotation = 0
        
        self.health = 1
        
        self.in_air = True
        
        self.img = "Player_Sheet.png"
        
        self.animation_queue = [(244,15,1,1,0)]
        
        self.current_sprite = self.animation_queue.pop()
        
        self.current_sprite_type = "running_right"

    def update_xy(self):
        
        #make the current values the old values
        self.previous_xl = self.xl
        self.previous_xr = self.xr
        self.previous_yt = self.yt
        self.previous_yb = self.yb
        
        self.draw_x = self.xl
        self.draw_y = self.yt
        
        #Updates the rightmost x point according to the leftmost x point
        self.xr = self.xl + self.width
        #Updates the bottommost y point according to the topmost y point
        self.yb = self.yt + self.height
        
    def collision_handler(self, other_object_type, other_object):
        return None
    
    def gravity(self):
        return None
    
    def animation_update(self, tick):
        return None

class Player_entity(Object):
    
    def __init__(self, x, y, health):
        
        self.type = "Player"
        
        self.xl = x
        self.xr = 0
        self.yt = y
        self.yb = 0
        
        self.previous_xl = 0
        self.previous_xr = 0
        self.previous_yt = 0
        self.previous_yb = 0
        
        self.change_x = 0.0
        self.change_y = 0.0
        
        self.previous_change_x = 0.0
        self.previous_change_y = 0.0
        
        self.draw_x = 0
        self.draw_y = 0
        
        self.width = 20
        self.height = 29
        
        self.rotation = 0
        
        self.health = health
        
        self.crouch = False
        self.attack = False
        
        self.in_air = True
        
        self.img = "Player_Sheet.png"
        
        self.animation_queue = [(60,128,20,29,0.07), (40,128,20,29,0.07), (20,128,20,29,0.07), (0,128,20,29,0.07)]
        
        self.running = [(60,128,20,29,0.07), (40,128,20,29,0.07), (20,128,20,29,0.07), (0,128,20,29,0.07)]
        
        self.current_sprite = self.animation_queue.pop()
        
        self.current_sprite_type = "running_right"
        
        self.win = False
        
        
    def collision_handler(self, other_object_type, other_object):
        
        #if the player is colliding with a tile
        if other_object_type == "Tile" or other_object_type == "Flamer" or other_object_type == "Logs":
            
            if other_object.collide_left(self.previous_xr) and not self.yb <= other_object.yt and not self.yt >= other_object.yb:
                self.xl = other_object.xl - self.width
                
            if other_object.collide_right(self.previous_xl) and not self.yb <= other_object.yt and not self.yt >= other_object.yb:
                
                self.xl = other_object.xr
        
            if other_object.collide_top(self.previous_yb):
                
                self.yt = other_object.yt - self.height
                self.change_y = 0
                self.in_air = False
                
            if other_object.collide_bottom(self.previous_yt):
                
                self.yt = other_object.yb
                self.change_y = -0.1
                
            #Updates the rightmost x point according to the leftmost x point
            self.xr = self.xl + self.width
            #Updates the bottommost y point according to the topmost y point
            self.yb = self.yt + self.height

            
        #if the player is colliding with a hurtfull aspect of an enemy
        if other_object_type == "Tri Flame" or other_object_type == "Flamer Projectile":
            
            if other_object.collide_left(self.previous_xr):
                self.change_x = -2
                
            if other_object.collide_right(self.previous_xl):
                self.change_x = 2
        
            if other_object.collide_top(self.previous_yb):
                self.change_y = -1.6
                self.change_x *= -2
                
            if other_object.collide_bottom(self.previous_yt):
                self.change_y = 2
                self.change_x *= -2
                
            elif not other_object.collide_top(self.previous_yb) and not other_object.collide_right(self.previous_xl) and not other_object.collide_left(self.previous_xr):
                self.change_x *= -1.5
                
            self.health -= 2
            
            #Updates the rightmost x point according to the leftmost x point
            self.xr = self.xl + self.width
            #Updates the bottommost y point according to the topmost y point
            self.yb = self.yt + self.height
            
            self.in_air = False
        
        if other_object_type == "Win_Goal":
            self.win = True
              
    def gravity(self):
        
        #If the change in the Y direction is not 0
        if self.change_y != 0 or self.in_air == True:
            
            self.change_y += 0.3
      
    def update_xy(self):
        
        #make the current values the old values
        self.previous_xl = self.xl
        self.previous_xr = self.xr
        self.previous_yt = self.yt
        self.previous_yb = self.yb
        
        
        self.xl += self.change_x
        
        self.yt += self.change_y
        
        self.draw_x = self.xl
        self.draw_y = self.yt
        
        #Updates the rightmost x point according to the leftmost x point
        self.xr = self.xl + self.width
        #Updates the bottommost y point according to the topmost y point
        self.yb = self.yt + self.height
        
    def Attack(self):
        if self.attack:
            
            #if the character is attacking while facing right
            if self.change_x > 0 or self.current_sprite_type == "standing_right" or self.current_sprite_type == "jumping_right" or self.current_sprite_type == "attacking_right" or self.current_sprite_type == "running_right":
                
                self.draw_x = self.xl - 6
                self.draw_y = self.yt - 3
                return(self.xr - 5, self.yt - 3)
               
            #if the character is attacking while facing left 
            elif self.change_x < 0 or self.current_sprite_type == "standing_left" or self.current_sprite_type == "jumping_left" or self.current_sprite_type == "attacking_left" or self.current_sprite_type == "running_left":
                
                self.draw_x = self.xl - 6
                self.draw_y = self.yt - 3
                return(self.xl - 6, self.yt - 3)
                
        else:
            return (-100, -100)
                    
    def animation_update(self, tick):
        
        """
        if self.previous_sprite_type != self.current_sprite_type:
            if self.change_x > 0:
                self.current_sprite_type = "running_right"
                self.animation_queue = [(60,128,20,29,0.07), (40,128,20,29,0.07), (20,128,20,29,0.07), (0,128,20,29,0.07)]
                
            elif self.change_x > 0:
                self.current_sprite_type = "running_right"
                self.animation_queue = [(60,128,20,29,0.07), (40,128,20,29,0.07), (20,128,20,29,0.07), (0,128,20,29,0.07)]
        """
        
        #if the character is standing still
        if self.change_x == 0:
            #if the character was running towards the right before stopping
            if self.current_sprite_type == "running_right" or self.current_sprite_type == "jumping_right" or (self.current_sprite_type == "attacking_right" and self.attack == False):
                self.current_sprite_type = "standing_right"
                self.animation_queue = [(0,157,20,29,2), (20,157,20,29,2)]
                self.current_sprite = self.animation_queue.pop()
            
            #if the character was running towards the left before stopping
            if self.current_sprite_type == "running_left" or self.current_sprite_type == "jumping_left" or (self.current_sprite_type == "attacking_left"and self.attack == False):
                self.current_sprite_type = "standing_left"
                self.animation_queue = [(40,157,20,29,2), (60,157,20,29,2)]
                self.current_sprite = self.animation_queue.pop()
                
        #if the character is running right
        if self.change_x > 0 and self.current_sprite_type != "running_right" and self.current_sprite_type != "attacking_right":
            self.current_sprite_type = "running_right"
            self.animation_queue = [(60,128,20,29,0.07), (40,128,20,29,0.07), (20,128,20,29,0.07), (0,128,20,29,0.07)]
            self.current_sprite = self.animation_queue.pop()
        
        #if the character is running left
        if self.change_x < 0 and self.current_sprite_type != "running_left" and self.current_sprite_type != "attacking_left":
            self.current_sprite_type = "running_left"
            self.animation_queue = [(0,186,20,29,0.07),(20,186,20,29,0.07),(40,186,20,29,0.07),(60,186,20,29,0.07)]
            self.current_sprite = self.animation_queue.pop()
        
        #if the character is falling or jumping
        if self.change_y != 0 and not (self.current_sprite_type == "jumping_right" or self.current_sprite_type == "jumping_left"):
            
            #was in the if statements:  or (self.current_sprite_type == "attacking_right" and self.attack == False)
            #If the character is jumping to the right, play the corresponding animation
            if (self.change_x > 0 or self.current_sprite_type == "standing_right") and self.current_sprite_type != "attacking_right":
                self.current_sprite_type = "jumping_right"
                self.animation_queue = [(20,128,20,29,0.01)]
                self.current_sprite = self.animation_queue.pop()
                
            
            #If the character is jumping to the left, play the corresponding animation
            if (self.change_x < 0 or self.current_sprite_type == "standing_left") and self.current_sprite_type != "attacking_left":
                self.current_sprite_type = "jumping_left"
                self.animation_queue = [(40,186,20,29,0.07)]
                self.current_sprite = self.animation_queue.pop()
               
        
        #if the character is attacking
        if self.attack and not self.current_sprite_type == "attacking_right" and not self.current_sprite_type == "attacking_left":
            
            #if the character is attacking while facing right
            if self.change_x > 0 or self.current_sprite_type == "standing_right" or self.current_sprite_type == "jumping_right":
                self.current_sprite_type = "attacking_right"
                self.animation_queue = [(186,128,32,32,0.07), (154,128,32,32,0.04), (122,128,32,32,0.04), (90,128,32,32,0.04)]
                self.current_sprite = self.animation_queue.pop()
               
            #if the character is attacking while facing left 
            if self.change_x < 0 or self.current_sprite_type == "standing_left" or self.current_sprite_type == "jumping_left":
                self.current_sprite_type = "attacking_left"
                self.animation_queue = [(90,160,32,32,0.07), (122,160,32,32,0.04), (154,160,32,32,0.04), (186,160,32,32,0.04)]
                self.current_sprite = self.animation_queue.pop()
                

                
        x, y, width, height, time = self.current_sprite
        
        time = time - tick
        
        if time <= 0:

            #if there is no more frames left in the current cycle of the animation
            if len(self.animation_queue) == 0:
                
                if self.current_sprite_type == "standing_right":
                    self.animation_queue = [(0,157,20,29,2), (20,157,20,29,2)]
                    
                elif self.current_sprite_type == "standing_left":
                    self.animation_queue = [(40,157,20,29,2), (60,157,20,29,2)]
                
                elif self.current_sprite_type == "running_right":
                    self.animation_queue = [(60,128,20,29,0.07), (40,128,20,29,0.07), (20,128,20,29,0.07), (0,128,20,29,0.07)]
                
                elif self.current_sprite_type == "running_left":
                    self.animation_queue = [(0,186,20,29,0.07),(20,186,20,29,0.07),(40,186,20,29,0.07),(60,186,20,29,0.07)]
                
                elif self.current_sprite_type == "jumping_right":
                    self.animation_queue = [(20,128,20,29,0.01)]
                    
                elif self.current_sprite_type == "jumping_left":
                    self.animation_queue = [(40,186,20,29,0.07)]
                    
                elif self.current_sprite_type == "attacking_right":
                    self.attack = False
                    self.current_sprite_type = "standing_right"
                    self.animation_queue = [(0,157,20,29,2), (20,157,20,29,2)]
                    
                elif self.current_sprite_type == "attacking_left":
                    self.attack = False
                    self.current_sprite_type = "standing_left"
                    self.animation_queue = [(40,157,20,29,2), (60,157,20,29,2)]
                             
                   
                self.current_sprite = self.animation_queue.pop()
            
            else:
                self.current_sprite = self.animation_queue.pop()
            
            
        else:
            self.current_sprite = (x, y, width, height, time)
            
            
class Death(Object):
    def __init__(self, xl, yt):
        
        self.type = "Death"
        
        self.xl = xl
        self.xr = 0
        self.yt = yt
        self.yb = 0
        
        self.previous_xl = 0
        self.previous_xr = 0
        self.previous_yt = 0
        self.previous_yb = 0
        
        self.draw_x = self.xl
        self.draw_y = self.yt
        
        self.width = 16
        self.height = 16
        
        self.rotation = 0
        
        self.health = 1
        
        self.in_air = True
        
        self.img = "Player_Sheet.png"
        
        self.animation_queue = [(80,80,16,16,0.08), (64,80,16,16,0.08), (48,80,16,16,0.08), (32,80,16,16,0.08)]
        
        self.current_sprite = self.animation_queue.pop()


    def update_xy(self):
        
        #make the current values the old values
        self.previous_xl = self.xl
        self.previous_xr = self.xr
        self.previous_yt = self.yt
        self.previous_yb = self.yb
        
        self.draw_x = self.xl
        self.draw_y = self.yt
        
        #Updates the rightmost x point according to the leftmost x point
        self.xr = self.xl + self.width
        #Updates the bottommost y point according to the topmost y point
        self.yb = self.yt + self.height
        
    def collision_handler(self, other_object_type, other_object):
        return None
    
    def gravity(self):
        return None
    
    def animation_update(self, tick):
        x, y, width, height, time = self.current_sprite
        
        time = time - tick
        
        if time <= 0:

            #if there is no more frames left in the current cycle of the animation
            if len(self.animation_queue) == 0:
                self.health = 0
                
            else:
                self.current_sprite = self.animation_queue.pop()
            
            
        else:
            self.current_sprite = (x, y, width, height, time)

class Logs(Object):
    def __init__(self, x, y):
        
        self.type = "Logs"
        
        self.xl = x
        self.xr = 0
        self.yt = y
        self.yb = 0
        
        self.previous_xl = 0
        self.previous_xr = 0
        self.previous_yt = 0
        self.previous_yb = 0
        
        self.change_x = 0.0
        self.change_y = 0.0
        
        self.draw_x = 0
        self.draw_y = 0
        
        self.width = 32
        self.height = 32
        
        self.health = 2
        
        self.current_sprite = (176,0,32,32,0.08)
        
        self.current_sprite_type = "running_right"
        
    def collision_handler(self, other_object_type, other_object):
        if other_object_type == "Sword":
            self.health = 0
        

    def gravity(self):
        return None

    def update_xy(self):
        #make the current values the old values
        self.previous_xl = self.xl
        self.previous_xr = self.xr
        self.previous_yt = self.yt
        self.previous_yb = self.yb
        
        
        self.draw_x = self.xl
        self.draw_y = self.yt
        
        #Updates the rightmost x point according to the leftmost x point
        self.xr = self.xl + self.width
        #Updates the bottommost y point according to the topmost y point
        self.yb = self.yt + self.height
     
    def animation_update(self, tick):
        
        x, y, width, height, time = self.current_sprite
        
        time = time - tick
        
        if time <= 0:

            self.current_sprite = (176,0,32,32,0.08)
            
        else:
            self.current_sprite = (x, y, width, height, time)
    
    
class Animation(Object):
    def __init__(self, x, y, type2):
        
        self.type = "Animation"
        
        self.xl = x
        self.xr = 0
        self.yt = y
        self.yb = 0
        
        self.previous_xl = 0
        self.previous_xr = 0
        self.previous_yt = 0
        self.previous_yb = 0
        
        self.change_x = 0.0
        self.change_y = 0.0
        
        self.draw_x = 0
        self.draw_y = 0
        
        self.width = 32
        self.height = 32
        
        self.health = 2
        
        
        if type2 == "sign_L":
            self.current_sprite = (144,0,32,24,0.08)
        
            self.current_sprite_type = "sign_L"
            
        if type2 == "sign_AD":
            self.current_sprite = (32,0,32,24,0.08)
        
            self.current_sprite_type = "sign_AD"
            
        if type2 == "sign_K":
            self.current_sprite = (64,0,32,24,0.08)
        
            self.current_sprite_type = "sign_K"
            
        if type2 == "tree fire":
            self.animation_queue = [(128,64,32,24,0.08),(160,64,32,24,0.08)]
            self.current_sprite = self.animation_queue.pop()
            self.current_sprite_type = "tree fire"
            
        if type2 == "game over":
            self.current_sprite = (32,32,176,32,0.08)
            self.current_sprite_type = "game over"
        
    def collision_handler(self, other_object_type, other_object):
        if other_object_type == "Sword":
            self.health = 0
        

    def gravity(self):
        return None

    def update_xy(self):
        #make the current values the old values
        self.previous_xl = self.xl
        self.previous_xr = self.xr
        self.previous_yt = self.yt
        self.previous_yb = self.yb
        
        
        self.draw_x = self.xl
        self.draw_y = self.yt
        
        #Updates the rightmost x point according to the leftmost x point
        self.xr = self.xl + self.width
        #Updates the bottommost y point according to the topmost y point
        self.yb = self.yt + self.height
     
    def animation_update(self, tick):
        
        x, y, width, height, time = self.current_sprite
        
        time = time - tick
        
        if time <= 0:
            if len(self.animation_queue) <= 0:
                if self.current_sprite_type == "sign_L":
                    self.current_sprite = (144,0,32,24,0.08)
                
                    self.current_sprite_type = "sign_L"
                    
                if self.current_sprite_type == "sign_AD":
                    self.current_sprite = (32,0,32,24,0.08)
                
                    self.current_sprite_type = "sign_AD"
                    
                if self.current_sprite_type == "sign_K":
                    self.current_sprite = (64,0,32,24,0.08)
                
                    self.current_sprite_type = "sign_K"
                    
                if self.current_sprite_type == "tree fire":
                    self.animation_queue = [(128,64,32,24,0.08),(160,64,32,24,0.08)]
                    self.current_sprite = self.animation_queue.pop()
                    self.current_sprite_type = "tree fire"
                    
                if self.current_sprite_type == "game over":
                    self.current_sprite = (32,32,176,32,0.08)
                    self.current_sprite_type = "game over"
        
                    self.current_sprite = (176,0,32,32,0.08)
            
            else:
                self.current_sprite = self.animation_queue.pop()
            
        else:
            self.current_sprite = (x, y, width, height, time)

class Win_Goal(Object):
    
    def __init__(self, x, y):
        
        self.type = "Win_Goal"
        
        self.xl = x
        self.xr = 0
        self.yt = y
        self.yb = 0
        
        self.previous_xl = 0
        self.previous_xr = 0
        self.previous_yt = 0
        self.previous_yb = 0
        
        self.change_x = 0.0
        self.change_y = 0.0
        
        self.draw_x = 0
        self.draw_y = 0
        
        self.width = 32
        self.height = 1000
        
        self.health = 2
        
        self.current_sprite = (212,79,1,1,0.01)
        
        
    def collision_handler(self, other_object_type, other_object):
        return None
        

    def gravity(self):
        return None

    def update_xy(self):
        #make the current values the old values
        self.previous_xl = self.xl
        self.previous_xr = self.xr
        self.previous_yt = self.yt
        self.previous_yb = self.yb
        
        
        self.draw_x = self.xl
        self.draw_y = self.yt
        
        #Updates the rightmost x point according to the leftmost x point
        self.xr = self.xl + self.width
        #Updates the bottommost y point according to the topmost y point
        self.yb = self.yt + self.height
     
    def animation_update(self, tick):
        
        return None
    