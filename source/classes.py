import pygame
from interactions import *

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)
BLUE = (0,0,255)


class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit, message
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
#        image.set_alpha(0)
        image.blit(self.sheet, (0, 0), rect)
        #if colorkey == None:
            
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)



class bars:
    def __init__(self,x,y,scalex,color):
        self.xpos = x
        self.ypos = y
        self.Xscale = scalex
        self.Yscale = scalex / 5
        self.color = color
        self.rect = pygame.Rect(self.xpos,self.ypos,self.Xscale,self.Yscale )

    def show(self,screen):
        pygame.draw.rect(screen, self.color,self.rect)
    def act(self,x,y):
        self.rect.x = x
        self.xpos = x
        self.ypos = y - self.Yscale * 2
        self.rect.y = y - self.Yscale * 2
class lifebars(bars):
    def show(self,screen,life,max_life):
        self.rect2 =pygame.Rect(self.xpos,self.ypos,int(self.Xscale * (life / float(max_life))),self.Yscale)
        
        pygame.draw.rect(screen, RED,self.rect)
        pygame.draw.rect(screen, GREEN,self.rect2)
    def act(self,x,y):
        self.rect.x = x
        self.xpos = x
        self.ypos = y - self.Yscale
        self.rect.y = y - self.Yscale
class mapa:
    def __init__(self,X,Y,Xscale=10,Yscale =10):
        counter = 0
        self.lista = []
        self.X = X
        self.Y = Y
        self.fast = False
        self.positions = {}
        self.Xscale = Xscale
        self.Yscale = Yscale
        self.image = spritesheet("images/ground.png")
        self.reserved = []
        self.ground_images = []
        self.grass_images = []
        self.water_images = []
        self.dessert_images = []
        self.trees_images = []
        self.lakes = []
        self.desserts = []
        self.grasslands = []
        self.ground = []
        self.trees = []
        self.reserved = []
        self.animated = []
        self.selected = []
        self.tanks = []
        self.ships = []
        self.bases = []
        self.helis = []
        self.planes = []
        self.teams = []
        self.explosions = []
        self.shots = []
        self.fondo = self.image.image_at(( 100,40,20,20))
        self.fondo = pygame.transform.scale(self.fondo,(self.X,2 * self.Yscale))
        tree = self.image.image_at((0,40,20,20))
        tree = pygame.transform.flip(tree,True,False)
        self.trees_images.append(tree)
        for i in range(5):
            self.grass_images.append(self.image.image_at((i * 20,20,20,20)))
            self.dessert_images.append(self.image.image_at((i * 20 + 100,0,20,20)))
            self.water_images.append(self.image.image_at((i * 20 + 100,20,20,20)))
            self.ground_images.append(self.image.image_at((i * 20,0,20,20)))
            self.trees_images.append(self.image.image_at((i *20,40,20,20)))
        for i in range(X / Xscale):
            self.lista.append([])
            for j  in range(Y / Yscale):
                patch = patches(i * Xscale,j * Yscale,Xscale,Yscale,counter)
                self.lista[i].append(patch)
                self.positions[str(counter)] =(i,j)
                counter = counter + 1
        self.n_patches = counter
        for i in range(len(self.lista)):
            for j in range(len(self.lista[i])):
                if(i > 1):
                    self.lista[i][j].neighbors.append(self.lista[i -1][j])
                    if(j > 1):
                        self.lista[i][j].neighbors.append(self.lista[i -1][j - 1])
                        
                if(i < len(self.lista) - 1):
                    self.lista[i][j].neighbors.append(self.lista[i +1][j])
                    if(j < len(self.lista[i])- 1):
                        self.lista[i][j].neighbors.append(self.lista[i +1][j+ 1])
                    
                if(j > 1):
                    self.lista[i][j].neighbors.append(self.lista[i ][j-1])
                    if(i < len(self.lista) - 1):
                         self.lista[i][j].neighbors.append(self.lista[i +1][j - 1])
                    
                if(j < len(self.lista[i])- 1):
                    self.lista[i][j].neighbors.append(self.lista[i ][j+1])
                    if(i > 1):
                        self.lista[i][j].neighbors.append(self.lista[i -1][j + 1])
                        
    def create_shot(self,obj):
        shot1 = shots(obj.xpos,obj.ypos,(obj.dx,obj.dy),obj.team)
        self.shots.append(shot1)
        self.animated.append(shot1)
    def show_explosions(self,screen):
        for j in self.explosions:
            if(not j.dead):
                j.act(screen,self) 
    def create_explosion(self,obj):
        exp = explosions(obj.xpos,obj.ypos)
        self.animated.append(exp)
        self.explosions.append(exp)
    def create_soldiers(self,lista,num = 1,team = None,patch = None):
            if(team == None):
                color = BLACK
            else:
                color = team.color
            number_old = len(self.tanks)
            old_patch = patch
            for i in range(num):
                number = number_old+ i
                if(patch == None):
                    patch = oneOf(lista)
                    iteration = 0
                    while(patch.reserved):
                        if(iteration > 1000):
                            return 0
                        iteration = iteration + 1
                        patch = oneOf(lista)
                if(patch != 0):
                    tank = soldiers(patch.xpos,patch.ypos,30,30,number,team)
                    
                    patch.reserve(self)
                    self.animated.append(tank)
                    self.tanks.append(tank)
                    if(team != None):
                        team.animated.append(tank)
                        team.tanks.append(tank)
                    patch = old_patch
    def create_towers(self,lista,num = 1,team = None,patch = None):
        if(patch != None):
            if(patch.type == "water"):
                return
            if(team == None):
                color = BLACK
            else:
                color = team.color
            number_old = len(self.tanks)
            old_patch = patch
            for i in range(num):
                number = number_old+ i
                if(patch == None):
                    patch = oneOf(lista)
                    iteration = 0
                    while(patch.reserved):
                        if(iteration > 1000):
                            return 0
                        iteration = iteration + 1
                        patch = oneOf(lista)
                if(patch != 0):
                    tank = towers(patch.xpos,patch.ypos,30,30,number,team)
                    
                    patch.reserve(self)
                    self.animated.append(tank)
                    self.tanks.append(tank)
                    if(team != None):
                        team.animated.append(tank)
                        team.tanks.append(tank)
                    patch = old_patch
    def create_tanks(self,lista,num = 1,team = None,patch = None):
            if(team == None):
                color = BLACK
            else:
                color = team.color
            number_old = len(self.tanks)
            old_patch = patch
            for i in range(num):
                number = number_old+ i
                if(patch == None):
                    patch = oneOf(lista)
                    iteration = 0
                    while(patch.reserved):
                        if(iteration > 1000):
                            return 0
                        iteration = iteration + 1
                        patch = oneOf(lista)
                if(patch != 0):
                    tank = tanks(patch.xpos,patch.ypos,30,30,number,team)
                    
                    patch.reserve(self)
                    self.animated.append(tank)
                    self.tanks.append(tank)
                    if(team != None):
                        team.animated.append(tank)
                        team.tanks.append(tank)
                    patch = old_patch
    def create_planes(self,lista,num = 1,team = None,patch = None):
            if(team == None):
                color = BLACK
            else:
                color = team.color
            number_old = len(self.planes)
            old_patch = patch
            for i in range(num):
                number = number_old+ i
                if(patch == None):
                    patch = oneOf(lista)
                    
                if(patch != 0):
                    plane = planes(patch.xpos,patch.ypos,30,30,number,team)
                    
                    self.animated.append(plane)
                    self.planes.append(plane)
                    if(team != None):
                        team.animated.append(plane)
                        team.planes.append(plane)
                    patch = old_patch
    def create_healicopters(self,lista,num = 1,team = None,patch = None):
            if(team == None):
                color = BLACK
            else:
                color = team.color
            number_old = len(self.helis)
            old_patch = patch
            for i in range(num):
                number = number_old+ i
                if(patch == None):
                    patch = oneOf(lista)
                if(patch != 0):
                    heli = healicopters(patch.xpos,patch.ypos,30,30,number,team)
          
                    self.animated.append(heli)
                    self.helis.append(heli)
                    if(team != None):
                        team.animated.append(heli)
                        team.helis.append(heli)
                    patch = old_patch
    def create_ships(self,lista,num = 1,team = None,patch = None):
           if(team == None):
                color = BLACK
           else:
                color = team.color
           number_old = len(self.ships)
           old_patch = patch
           for i in range(num):
               number = number_old + i
               if(patch == None):
                    patch = oneOf(lista)
                    iteration = 0
                    if(patch == 0):
                            return 0
                    while(patch.reserved):
                        if(iteration > 1000):
                            return 0
                        iteration = iteration + 1
                        patch = oneOf(lista)
                        if(patch == 0):
                            return 0
               if(patch != 0):
                 
                    
                   ship = ships(patch.xpos,patch.ypos,30,30,number,team)
                   patch.reserve(self) 
                   
                   self.animated.append(ship)
                   self.ships.append(ship)
                   if(team != None):
                        team.animated.append(ship)
                        team.ships.append(ship)
                   patch = old_patch
    def create_bases(self,lista,num = 1,team = None,dock = False,patch = None):
           if(team == None):
                color = BLACK
           else:
                color = team.color
           number_old = len(self.bases)
           old_patch = patch
           for i in range(num):
               number = number_old + i
               if(patch == None):
                    patch = oneOf(lista)
               if(patch != 0):
                   base = bases(patch.xpos,patch.ypos,30,30,number,color,dock)
                   base.team = team
                   self.animated.append(base)
                   self.bases.append(base)
                   if(team != None):
                        team.bases.append(base)
                   
                   patch = old_patch
    def checkPatches(self):
        for i in self.lakes:
            counter = 0
            for j in i.neighbors:
                if(j.type != "water"):
                    chosen = j
                    counter = counter + 1
                    
            if(counter > 4):
                i.type = chosen.type
                i.image = chosen.image
                self.lakes.remove(i)
            if(i.type != "water"):
                if(i in self.lakes):
                    self.lakes.remove(i)
        for i in self.desserts:
            if(i.type != "sand"):
                self.desserts.remove(i)
        for i in self.grasslands:
            if(i.type != "grass"):
                self.desserts.remove(i)
        for i in self.ground:
            if(i.type != "grass"):
                self.ground.remove(i)
        for i in self.trees:
            if(i.patch.type =="water"):
                 if(i in self.trees):
                    self.trees.remove(i)
            for j in (i.patch.neighbors):
                if(j.type =="water"):
                    if(i in self.trees):
                        self.trees.remove(i)
                        
        
           
    def get(self,i,j):
        return self.lista[i][j]
    def createmap(self):
        for i in self.lista:
            for j in i:
                j.setImage(oneOf(self.ground_images),"ground",self)
                self.ground.append(j)
                
                
    def changePatch(self,image,name,num,X= -1,Y= -1):
        if(X==-1 and Y ==-1):
            vector = self.positions[str(num)]
            x = vector[0]
            y = vector[1]
        else:
            x = X
            y = Y
        self.lista[x][y].setImage(image,name)
    def whatIs(self,num):
        vector = self.positions[str(num)]
        x = vector[0]
        y = vector[1]
        return self.lista[x][y].type
    def createGrassland(self,pos,size,top = 0.5):
        point = self.whereIs(pos)
        vector = self.positions[str(point.num)]
        x = vector[0]
        y = vector[1]
        top = 0.5
        for i in range(size):
            for j in range(size):
                if(random()*((i + j) / (size)) < top and (x+i)<len(self.lista) and (y - j) >=0):
                    self.lista[x + i ][y - j].setImage(oneOf(self.grass_images),"grass",self)
                    self.grasslands.append(self.lista[x + i ][y - j])
                if(random()*((i + j) / (size)) < top and (x-i)>=0  and (y + j) < len(self.lista[0])):
                    self.lista[x - i][y + j].setImage(oneOf(self.grass_images),"grass",self)
                    self.grasslands.append(self.lista[x - i ][y + j])
                if(random()*((i + j) / (size)) < top and (x+i)<len(self.lista) and (y + j) < len(self.lista[0])):
                    self.lista[x + i][y + j].setImage(oneOf(self.grass_images),"grass",self)
                    self.grasslands.append(self.lista[x + i ][y +j])
                if(random()*((i + j) / (size)) < top and (x-i)>=0 and (y - j) >=0):
                    self.lista[x - i][y - j].setImage(oneOf(self.grass_images),"grass",self)
                    self.grasslands.append(self.lista[x - i ][y - j])
        
    def createDessert(self,pos,size,top = 0.5):
        point = self.whereIs(pos)
        vector = self.positions[str(point.num)]
        x = vector[0]
        y = vector[1]
        top = 0.5
        for i in range(size):
            for j in range(size):
                if(random()*((i + j) / (size)) < top and (x+i)<len(self.lista) and (y - j) >=0):
                    self.lista[x + i ][y - j].setImage(oneOf(self.dessert_images),"sand",self)
                    self.desserts.append(self.lista[x + i ][y - j])
                if(random()*((i + j) / (size)) < top and (x-i)>=0  and (y + j) < len(self.lista[0])):
                    self.lista[x - i][y + j].setImage(oneOf(self.dessert_images),"sand",self)
                    self.desserts.append(self.lista[x - i ][y + j])
                if(random()*((i + j) / (size)) < top and (x+i) < len(self.lista) and (y + j) < len(self.lista[0])):
                    self.lista[x + i][y + j].setImage(oneOf(self.dessert_images),"sand",self)
                    self.desserts.append(self.lista[x + i ][y +j])
                if(random()*((i + j) / (size)) < top and (x-i)>=0 and (y - j) >=0):
                    self.lista[x - i][y - j].setImage(oneOf(self.dessert_images),"sand",self)
                    self.desserts.append(self.lista[x - i ][y - j])
    
    def createDessert_trees(self,seed):
        for j in self.desserts:
           
           if(random() < seed and not j.reserved):
                    Tree = trees(j.xpos,j.ypos,oneOf([self.trees_images[4], self.trees_images[5]]),j)
                    j.reserve(self)
                    self.trees.append(Tree)
    def createGrassland_trees(self,seed):
        for j in self.grasslands:
            
            if(random() < seed and not j.reserved):
                    Tree = trees(j.xpos,j.ypos,oneOf([self.trees_images[0], self.trees_images[1],self.trees_images[2],self.trees_images[3]]),j)
                    self.trees.append(Tree)
                    j.reserve(self)
    def createGround_trees(self,seed):
      for j in self.ground:
        
        if(random() < seed and not j.reserved):
                    Tree = trees(j.xpos,j.ypos,oneOf([self.trees_images[0], self.trees_images[1],self.trees_images[2],self.trees_images[3]]),j)
                    self.trees.append(Tree)
                    j.reserve(self)
                
    def createLake(self,pos,size,top = 0.5):
        point = self.whereIs(pos)
        vector = self.positions[str(point.num)]
        x = vector[0]
        y = vector[1]
        
        for i in range(size):
            for j in range(size):
                if(random()*((i + j) / (size)) < top and (x+i)<len(self.lista) and (y - j) >=0):
                    self.lista[x + i ][y - j].setImage(oneOf(self.water_images),"water",self)
                    self.lakes.append(self.lista[x + i ][y - j])
                if(random()*((i + j) / (size)) < top and (x-i)>=0  and (y + j) < len(self.lista[0])):
                    self.lista[x - i][y + j].setImage(oneOf(self.water_images),"water",self)
                    self.lakes.append(self.lista[x - i ][y + j])
                if(random()*((i + j) / (size)) < top and (x+i)<len(self.lista) and (y + j) < len(self.lista[0])):
                    self.lista[x + i][y + j].setImage(oneOf(self.water_images),"water",self)
                    self.lakes.append(self.lista[x + i ][y +j])
                if(random()*((i + j) / (size)) < top and (x-i)>=0 and (y - j) >=0):
                    self.lista[x - i][y - j].setImage(oneOf(self.water_images),"water",self)
                    self.lakes.append(self.lista[x - i ][y - j])
        for i in self.lakes:
            for j in i.neighbors:
                if(j.type != "water"):
                    j.setImage(oneOf(self.dessert_images + self.grass_images),"sand",self)
                    self.desserts.append(j)


    def whereIs(self,(x,y)):
        for i in self.lista:
            for j in i:
                if(j.xpos<=x<(j.xpos +self.Xscale) and j.ypos<=y<(j.ypos +self.Yscale)):
                    return j
        return "point not found"
    def showCorner(self,screen,side,width,color = WHITE):
        if(side == "left"):
            for i in range(width):
                for j in self.lista[i]:
                    pygame.draw.rect(screen, color,j.rect)
        elif(side == "right"):
            for i in range(1,width + 1):
                for j in self.lista[-i]:
                    pygame.draw.rect(screen, color,j.rect)
        elif(side == "up"):
            for i in self.lista:
                for j in range(width):
                    pygame.draw.rect(screen, color,i[j].rect)
        elif(side == "down"):
            for i in self.lista:
                for j in range(1,width+1):
                    pygame.draw.rect(screen, color,i[-j].rect)
            
            
                
    def show(self,screen):
        for j in self.selected:
            if (j.dead):
                self.selected.remove(j)
        for i in self.lista:
            for j in i:
                if(j.hasImage):

                   screen.blit(j.image,(j.xpos,j.ypos)) 
                else:
                    pygame.draw.rect(screen, (int(j.xpos / float(self.X) *255),int(j.ypos /float( self.Y) * 255),0),j.rect)
                    pygame.draw.rect(screen, BLACK,j.rect)
        for i in self.trees:
            i.show(screen)
        screen.blit(self.fondo,(0,self.Y)) 
        self.show_explosions(screen)

            ############################################################## TREES
class trees:
    def __init__(self,x,y,image,patch = None,xscale= 40,yscale=40):
        self.xpos = x
        self.ypos =y
        self.Xscale = xscale
        self.Yscale =yscale
        self.patch = patch
        self.image = image
        
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.image,(self.Xscale,self.Yscale))
    def show(self,screen):
#        pygame.draw.rect(screen, BLACK,self.patch.rect)
        screen.blit(self.image,(self.xpos - (self.Xscale - self.patch.Xscale) / 2,self.ypos - self.Yscale / 2))


class patches:
    def __init__(self,x,y,scalex,scaley,n):
        self.xpos = x
        self.ypos = y
        self.num = n
        self.reserved = 0
        self.hasImage = False
        self.Xscale = scalex
        self.Yscale =scaley
        self.image  = None
        self.type = None
        self.neighbors = []
        self.rect = pygame.Rect(self.xpos,self.ypos,self.Xscale,self.Yscale)
    def __str__(self):
        result = "\n" +"patch " + str(self.num) +"\n" +"type: " + str(self.type) + "\n" +" x: " + str(self.xpos) + " y: " + str(self.ypos) + "\n" 
        return result
    def cleanPatch(self,mapa):
        if(self in mapa.desserts):
            mapa.desserts.remove(self)
        if(self in mapa.ground):
            mapa.ground.remove(self)
        if(self in mapa.grasslands):
            mapa.grasslands.remove(self)
        if(self in mapa.lakes):
            mapa.lakes.remove(self)
        self.type = None
    def setImage(self,image,name,mapa):
        self.cleanPatch(mapa)
        self.image = image
        self.type = name
        self.hasImage= True
        self.image = pygame.transform.scale(self.image,(self.Xscale,self.Yscale))
    def distance(self,(x,y)):
        distance = abs(self.xpos - x )+ abs(self.ypos - y)
        return distance
    def reserve(self,L):
                self.reserved = 1
                if(self not in L.reserved):
                    L.reserved.append(self)
    def reserve1(self,obj,L):
        if(self.xpos - obj.rect.left >= 0 and self.xpos - obj.rect.right <= 0):
            if(self.ypos - obj.rect.top >= 0 and self.ypos - obj.rect.bottom <= 0):
                self.reserved = 1
                if(self not in L.reserved):
                    L.reserved.append(self)

    def dereserve(self,obj,L):
        if(self.xpos - obj.rect.left >= 0 and self.xpos - obj.rect.right <= 0):
            if(self.ypos - obj.rect.top >= 0 and self.ypos - obj.rect.bottom <= 0):
                self.reserved = 0
                if(self  in L.reserved):
                    L.reserved.remove(self)


           #####################################################
######################################################################
class agents:
    def __init__(self,x,y,scalex,scaley,num =0,team = None):
        if(team == None):
            color = Black
        else:
            color = team.color
        self.speed = 2
        self.max_speed = 2
        self.showbars = False
        self.xpos = x
        self.ypos = y
        self.dx = 0
        self.dy = 0
        self.team = team
        self.color = color
        self.Xscale = scalex
        self.Yscale = scaley
        self.selected = False
        self.num = num
        self.angle = 0
        self.old_angle = self.angle
        self.name = None
        self.max_life = 100
        self.life = self.max_life
        self.maxnum_shots = 1
        self.num_shots = 1
        self.max_reloadtime = 50
        self.reloadtime = int(random() * self.max_reloadtime)
        self.dead = False
        self.ammo = self.max_ammo = 5
        self.rect = pygame.Rect(self.xpos,self.ypos,self.Xscale* 0.7,self.Yscale * 0.7)
 
        
        self.bar = bars(self.xpos,self.ypos,self.Xscale,self.color)
        self.lifebar = lifebars(self.xpos,self.ypos,self.Xscale,self.color)
        self.enemy = None
        self.set_image()
        
    def set_image(self):     
        self.image_up = self.image.image_at((80,60,20,20))
        self.image_up = pygame.transform.scale(self.image_up,(self.Xscale,self.Yscale))
        self.image_up.set_colorkey(BLACK)
        self.image = self.image_up
    def face(self,obj):
        x= obj.xpos - self.xpos
        y = obj.ypos - self.ypos
        if(abs(x) < abs(y)):
            if(y > 0):
                self.direction = "S"
            else:
                self.direction = "N"

        elif(abs(x) >= abs(y)):
            if(x > 0):
                self.direction = "E"
            else:
                self.direction = "W"
    def __str__(self):
        team = self.team
        if(self.team == None):
            print("none")
            team = ""
        res1 = "\n____________________________________________________ \n"
        result = res1 + self.name + " "  + str(self.num) +"\n" + " x: "+ str(int(self.xpos)) +" y: "+ str(int(self.ypos))  +"\n" + "life:" + str(int((self.life / float(self.max_life)) * 100)) + "% " +res1 + team.__str__() 
        return result
    def act(self,screen,mapa):
        self.shoot(mapa)
        self.move(mapa)
        self.show(screen)
        for i in self.team.helis:
            i.heal(self)
        
        
        if(self.life <= 0):
            self.dead = True
    
    
    def image_act(self):
            self.image = pygame.transform.rotate(self.image_up,-90 -self.angle * (180 / ( pi)))
    def FacePos(self, xpos,ypos):
        x = xpos - self.xpos
        y = ypos - self.ypos
        alpha = self.angle - 1
        if(x == 0):
            if(y < 0):
                self.angle = -pi / 2
            else:
                
                self.angle = pi / 2
        if( y == 0):
            if(x > 0):
                self.angle = pi
            else:
                self.angle = 0
        if(x != 0 and  y != 0):
            self.angle = atan(y / x)
        if( x < 0):
            self.angle = self.angle + pi
        
        self.dx = cos(self.angle)
        self.dy = sin(self.angle)
        if(alpha  + 1!= self.angle):
            self.image_act()
        return
    def check(self,mapa):
        pass
    def turn(self,side):
        if(side =="left"):
            self.angle = self.angle -0.1
        else:
            self.angle = self.angle +0.1
        self.dx = cos(self.angle)
        self.dy = sin(self.angle)
    def act_manual(self,screen,mando,mapa):
        self.xpos += self.speed * self.dx
        self.ypos += self.speed * self.dy
        for i in mando.keys.keys():
            if(mando.keys[i].pressed and mando.teams[i]==self.team.num):
                action = mando.actions[i]
                if(action == "accelerate"):
                    self.accelerate()
                elif(action == "brake"):
                     self.brake()
                elif(action == "left"):
                    print(self.angle)
                    self.turn("left")
                elif(action == "right"):
                    self.turn("right")
                elif(action =="shoot"):
                    self.shoot_manual(mapa)
        self.image_act()
        self.show(screen)
                
            
    def accelerate(self):
        self.speed = self.max_speed
        self.xpos += self.speed * self.dx
        self.ypos += self.speed * self.dy
    def brake(self):
        self.speed = 0
    def shoot_manual(self,mapa):
        mapa.create_shot(self)
    def Face(self,someone):
        x = someone.xpos - self.xpos
        y = someone.ypos - self.ypos
        alpha = self. angle - 1
        if(x == 0):
            if(y < 0):
                self.angle = -pi / 2.0
            else:
                
                self.angle = pi / 2.0
        if( y == 0):
            if(x > 0):
                self.angle = pi
            else:
                self.angle = 0
        if(x != 0 and  y != 0):
            self.angle = atan(y / float(x))
        if( x < 0):
            self.angle = self.angle + pi
        
        self.dx = cos(self.angle)
        self.dy = sin(self.angle)
        if(alpha  + 1!= self.angle):
            self.image_act()
    def move(self,mapa):
        if(random() < 0.01 and self.speed != 0 and self.name != "plane"):
             self.speed = 0           
        if(random() < 0.1 and self.speed == 0):  
                self.speed = self.max_speed
        self.check(mapa)
        
            
        self.mov(mapa)
        self.rect.x = self.xpos
        self.rect.y = self.ypos
        self.bar.act(self.xpos,self.ypos)
        self.lifebar.act(self.xpos,self.ypos)
    def mov(self,mapa):
        self.image_act()
        for s in mapa.shots:
            if( s.team != self.team and self.rect.colliderect(s.rect)):
                self.life = self.life - s.power
                s.dead = True
                mapa.create_explosion(self)
                if(self.life < 0):
                    s.team.points = s.team.points + 1
                    
        self.xpos += self.speed * self.dx
        self.ypos += self.speed * self.dy
        if(random()< 0.04):
            self.FacePos(int(random()*mapa.X),int(random() * mapa.Y))
        if(self.xpos > mapa.X - self.Xscale):
            self.xpos =mapa.X- self.Xscale
            self.Face(oneOf(self.team.animated))
        elif(self.xpos < 0):
            self.xpos = 0
            self.Face(oneOf(self.team.animated))
        if(self.ypos > mapa.Y - self.Yscale):
            self.ypos = mapa.Y - self.Yscale
            self.Face(oneOf(self.team.animated))
        elif(self.ypos < 0):
            self.ypos = 0
            self.Face(oneOf(self.team.animated))
        self.rect.x = self.xpos
        self.rect.y = self.ypos
    def mv(self):
        self.xpos = self.xpos + self.speed * self.orientations[self.direction][0]
        self.ypos = self.ypos + self.speed * self.orientations[self.direction][1]
    def show(self,screen):
        try:
 #           pygame.draw.rect(screen, BLACK,self.rect)
            screen.blit(self.image,(self.xpos,self.ypos))
            
        except:
            screen.blit(self.oriented_images[self.direction],(self.xpos,self.ypos))
        if(self.showbars  ):
           self.bar.show(screen)
           self.lifebar.show(screen,self.life,self.max_life)
    def shoot(self,mapa):
      if(self.ammo <= 0 ):
          destiny = minDof(self,self.team.bases)
          if(destiny != 0):
              if(self.name in destiny.names):
                  self.Face(destiny)
              elif(random() <0.4):
                  iterations = 0
                  while(iterations < 20 and self.name not in destiny.names):
                      destiny= choice(self.team.bases)
                      
                      iterations = iterations + 1
              
          pass
      else:
        if(self.reloadtime > 0):
            self.reloadtime = self.reloadtime - 1
        else:
            
            if(self.enemy == None or self.enemy.dead or random() < 0.04):
                self.enemy = None
                enemies = (i for i in (mapa.animated) if i.team != self.team)
                enemy = minDof(self,list(enemies))
                if(enemy != 0):
                    iterations = 0
                    while(enemy.team == self.team or enemy.dead and len(mapa.animated)> 1):
                        enemy = oneOf(list(enemies))
                        if(iterations > 1):
                          print("no enemies found")
                        iterations = iterations + 1
                        if(iterations > 100 or enemy == 0):
                            enemy = None
                            break
                    self.enemy = enemy
            if(self.enemy != None):
                x = self.enemy.xpos - self.xpos
                y = self.enemy.ypos - self.ypos
            else:
                x = 0
                y = 0
            if(random() < 0.5 and self.ammo > 0 and self.enemy != None):
                
                    self.Face(self.enemy)
                    mapa.create_shot(self)
                    self.ammo = self.ammo - 1
                    self.num_shots = self.num_shots - 1
                    self.reloadtime = self.max_reloadtime / 5
                    if(self.num_shots <= 0):
                        self.num_shots =self.maxnum_shots
                        self.reloadtime = self.max_reloadtime
               
class ships(agents):
    
    
    def set_image(self):
        self.name = "ship"
        self.max_life = 50
        self.life = self.max_life
        self.ammo = self.max_ammo = 5
        image = spritesheet("images/ground.png")
        self.image_up =image.image_at((20,60,20,20))
        self.image_up.set_colorkey(BLACK)
        self.image_up = pygame.transform.scale(self.image_up,(self.Xscale,self.Yscale))
        self.image = self.image_up
    
    
    def check(self,mapa):
        collided = 0
        
        patch = mapa.whereIs((self.xpos,self.ypos))
        if(type(patch) != str):
            if(patch.type != "water"):
                ground = (i for i in patch.neighbors if i.type == "water")
                if(ground != False and not isinstance(ground,int)):
                    ground = list(ground)
                    minimo = minDof(self,ground)
                    if(minimo != 0):
                        self.Face(minimo)
            for i in patch.neighbors:
              
              if(i.type != "water" ):
                collided = collideWith(self,i) 
                  
                
                
            if(random() < 0.01):
                self.Face(oneOf(mapa.lakes))
        for i in mapa.ships:
            collided = collideWith(self,i)
        if(collided):
            self.Face(oneOf(mapa.lakes))
        if(self.dead):
            mapa.ships.remove(self)
            mapa.animated.remove(self)
            self.team.ships.remove(self)
            self.team.animated.remove(self)
    
        
class planes(agents):
    
    
    def set_image(self):
        self.counter = 0
        self.name = "plane"
        self.max_life = 100
        self.life = self.max_life
        image = spritesheet("images/ground.png")
        self.images = []
        
        
        for i in range(2):
            
            self.image = image.image_at((80  + 20 * i,60,20,20))
            self.image = pygame.transform.scale(self.image,(self.Xscale,self.Yscale))
            self.image.set_colorkey(BLACK)
            self.images.append(self.image)
        self.image_up = self.image
        self.max_counter = len(self.images)
    def act(self,screen,mapa):
        self.shoot(mapa)
        self.move(mapa)
        self.show(screen)
        self.image_up = self.images[self.counter]
        self.counter = self.counter + 1
        if(self.counter >= self.max_counter ):
            self.counter = 0
        for i in self.team.helis:
            i.heal(self)
        
        
        if(self.life <= 0):
            self.dead = True
        
        
    def check(self,mapa):
        if(self.dead):
            mapa.planes.remove(self)
            mapa.animated.remove(self)
            self.team.planes.remove(self)
            self.team.animated.remove(self)
        
class healicopters(planes):
    
        
    def set_image(self):
        self.name = "heli"
        self.max_life = 60
        self.life = self.max_life
        image = spritesheet("images/ground.png")
        self.images = []
        for i in range(4):
            
            self.image = image.image_at((120  + 20 * i,60,20,20))
            self.image = pygame.transform.scale(self.image,(self.Xscale,self.Yscale))
            self.image.set_colorkey(BLACK)
            self.images.append(self.image)

        self.image_up = self.image
        self.counter = 0
        self.max_counter = len(self.images)
    def act(self,screen,mapa):
        for i in self.team.helis:
            i.heal(self)
        
        
        self.move(mapa)
        self.image_up = self.images[self.counter]
        self.counter = self.counter + 1
        if(self.counter >= self.max_counter):
            self.counter = 0
        self.show(screen)
        
        
        if(self.life <= 0):
            self.dead = True

    def heal(self,i):
        if(i != self and random() < 0.4):
            x = i.xpos - self.xpos
            y = i.ypos - self.ypos
            if(sqrt(x ** 2 + y ** 2) < 2 * sqrt(self.Xscale ** 2 +self.Yscale ** 2) and i.life < i.max_life):
                
                i.life = i.life + 1
                
            if(i.life < i.max_life / 2):
                self.Face(i)
                
    
    def check(self,mapa):
        if(self.dead):
            mapa.helis.remove(self)
            mapa.animated.remove(self)
            self.team.helis.remove(self)
            self.team.animated.remove(self)
    
        
        
           
class tanks(agents):
    
    
    def set_image(self):
        self.name = "tank"
        self.max_life = 100
        self.life = self.max_life
        image = spritesheet("images/ground.png")
        self.image_up =image.image_at((60,60,20,20))
        self.image_up.set_colorkey(BLACK)
        self.image_up = pygame.transform.scale(self.image_up,(self.Xscale,self.Yscale))
        
        self.image = self.image_up
    def check(self,mapa):
        collided = False
        patch = mapa.whereIs((self.xpos,self.ypos))
        if(type(patch) != str):
            if(patch.type == "water"):
                ground = (i for i in patch.neighbors if i.type != "water")
                if(ground != False and not isinstance(ground,int)):
                    ground = list(ground)
                    minimo = minDof(self,ground)
                    if(minimo != 0):
                        self.Face(minimo)
                    self.mov(mapa)
            for i in patch.neighbors:
               
              if(i.type == "water" ):
                if(collideWith(self,i)):
                    collided = True
                    break
        if(not collided):
            for i in mapa.tanks + mapa.bases:
                collided = collideWith(self,i)
        if(collided):
            self.Face(oneOf(mapa.grasslands+mapa.ground+mapa.desserts))
            self.speed = self.max_speed
        if(self.dead):
            mapa.tanks.remove(self)
            mapa.animated.remove(self)
            self.team.animated.remove(self)
            self.team.tanks.remove(self) 
class towers(agents):
    def set_image(self):
        self.name = "tower"
        self.maxnum_shots = 3
        self.image_xpos = self.xpos - self.Xscale * 0.1
        self.image_ypos = self.ypos - self.Yscale * 0.3
        self.bar.act(self.image_xpos,self.image_ypos)
        self.lifebar.act(self.image_xpos,self.image_ypos)
        image = spritesheet("images/ground.png")
        self.max_life = 100
        self.ammo = self.max_ammo= 10000
        self.reload_time = 100
        self.life = self.max_life
        self.image1 =image.image_at((60,120,20,20))
        self.image1.set_colorkey(BLACK)
        self.image2 =image.image_at((80,120,20,20))
        self.image2.set_colorkey(BLACK)
        self.image3 = self.image2
        self.image1 = pygame.transform.scale(self.image1,(self.Xscale,self.Yscale))
        self.image2 = pygame.transform.scale(self.image2,(self.Xscale,self.Yscale))
        self.rect2 = pygame.Rect(self.image_xpos + self.Xscale * 0.5,self.image_ypos - self.Yscale * 0.1,self.Xscale* 0.1,self.Yscale )
    def act(self,screen,mapa):
        self.shoot(mapa)
        self.image_act()
        self.show(screen)
        for i in self.team.helis:
            i.heal(self)
        for s in mapa.shots:
            if( s.team != self.team and self.rect.colliderect(s.rect)):
                self.life = self.life - s.power
                s.dead = True
                mapa.create_explosion(self)
                if(self.life < 0):
                    s.team.points = s.team.points + 1
        if(self.life <= 0 ):
            self.dead = True
        if(self.dead):
            mapa.tanks.remove(self)
            mapa.animated.remove(self)
            self.team.animated.remove(self)
            self.team.tanks.remove(self) 
        
    def image_act(self):
        (self.image3,self.rect2) = rot_center(self.image2,self.rect2,( 3* pi / 2 - self.angle) * (360 / (2 * pi)))
    def show(self,screen):
        screen.blit(self.image1,(self.image_xpos,self.image_ypos))
        screen.blit(self.image3,(self.rect2.x,self.rect2.y))
        if(self.showbars  ):
           self.bar.show(screen)
           self.lifebar.show(screen,self.life,self.max_life)
        
class soldiers(tanks):
    def set_image(self):
        
        self.counter = 0
        self.name = "tank"
        self.max_life = 100
        self.life = self.max_life
        image = spritesheet("images/ground.png")
        self.images = []
        self.image1 =image.image_at((0,120,20,20))
        self.image1.set_colorkey(BLACK)
        self.image1 = pygame.transform.scale(self.image1,(self.Xscale,self.Yscale))
        self.image2 =image.image_at((20,120,20,20))
        self.image2.set_colorkey(BLACK)
        self.image2 = pygame.transform.scale(self.image2,(self.Xscale,self.Yscale))
        self.image3 =image.image_at((40,120,20,20))
        self.image3.set_colorkey(BLACK)
        self.image3 = pygame.transform.scale(self.image3,(self.Xscale,self.Yscale))
        self.images.append(self.image1)
        self.images.append(self.image2)
        self.images.append(self.image3)
        self.images.append(self.image2)
        self.image_up = self.image2
        self.max_counter = len(self.images)
        
    def act(self,screen,mapa):
        self.shoot(mapa)
        self.move(mapa)
        self.show(screen)
        if(self.speed != 0):
            self.image_up = self.images[self.counter / 3]
        else:
            self.image_up = self.image2
        self.counter = self.counter + 1
        if(self.counter >= self.max_counter * 3):
            self.counter = 0
        for i in self.team.helis:
            i.heal(self)
        
        
        if(self.life <= 0):
            self.dead = True
        
 
class bases:
    def __init__(self,x,y,scalex,scaley,num = 0,color = BLACK,dock = False):
        image = spritesheet("images/ground.png")
        self.speed = 2
        self.xpos = x
        self.ypos = y
        self.showbars = False
        self.num = num
        self.name = "base"
        self.color =color
        self.Xscale = scalex
        self.Yscale = scaley
        self.selected = False
        self.dead = False
        self.patch = None
        self.max_life = 200
        self.life = self.max_life
        if(dock):
            self.names = ("ship","plane")
        else:
            self.names = ("tank","plane")
        self.bar = bars(self.xpos,self.ypos,self.Xscale,self.color)
        self.lifebar = lifebars(self.xpos,self.ypos,self.Xscale,self.color)
        self.team = None
        if(dock):
            self.image = image.image_at((20,80,20,20))
        else:
            self.image = image.image_at((0,80,20,20))
        self.image.set_colorkey(BLACK)
        self.rect = pygame.Rect(self.xpos,self.ypos,self.Xscale,self.Yscale)
        self.image = pygame.transform.scale(self.image,(self.Xscale,self.Yscale))
        self.bar.act(self.xpos,self.ypos)
        self.lifebar.act(self.xpos,self.ypos)
        
    def give_ammo(self,mapa):
       team = (i for i in mapa.animated if(i.team == self.team and i.name != "base" and i.name != "shot" and i.name != "explosion"))
       for i in team:
            x = i.xpos -self.xpos
            y = i.ypos -self.ypos
            if(sqrt(x ** 2 + y ** 2) < 2 * sqrt(self.Xscale ** 2 + self.Yscale ** 2)):
             try:
                if(i.ammo < i.max_ammo):
                    i.ammo = i.ammo + 1
             except:
                    pass
    def show(self,screen):
#        pygame.draw.rect(screen, BLACK,self.patch.rect)
        screen.blit(self.image,(self.xpos,self.ypos ))
        if(self.showbars  ):
           self.bar.show(screen)
           self.lifebar.show(screen,self.life,self.max_life)
    def __str__(self):
        team = self.team
        if(self.team == None):
            team = ""
        res1 = "\n____________________________________________________ \n"
        result =  res1+"base " + str(self.num) + "\n" + "x: "+ str(self.xpos) +" y: "+ str(self.ypos) + " " + "life:" + str(int((self.life / float(self.max_life)) * 100)) + "% "+res1 + team.__str__()+ "\n"
        
        return result 
    def act(self,screen,mapa):
        if(self.patch == None):
            self.patch = mapa.whereIs((self.xpos,self.ypos))
        for i in self.team.helis:
            i.heal(self)
        self.give_ammo(mapa)
        self.show(screen)
        for s in mapa.shots:
            if( s.team != self.team and self.rect.colliderect(s.rect)):
                self.life = self.life - s.power
                s.dead = True
                mapa.create_explosion(self)
                if(self.life <=0):
                    s.team.points = s.team.points + 1
                    self.dead = True
        if(self.dead):
            self.team.bases.remove(self)
            mapa.bases.remove(self)
            mapa.animated.remove(self)

class teams:
    def __init__(self,color,num = 0):
        self.color = color
        self.num = num
        self.animated = []
        self.planes= []
        self.ships = []
        self.tanks = []
        self.bases = []
        self.helis = []
        self.points = 0
    def add(self,obj):
        self.animated.append(obj)
    def __str__(self):
        res = "\n###################################################### \n"
        res1 = "\n____________________________________________________ \n"
        result = res +"team " +str(self.num) +  res1 + "color: " +str(self.color)+ "\n" + "points: " +str(self.points) + "\n"
 
        result1 = "bases: " + str(len(self.bases)) + " planes: " + str(len(self.planes)) + " ships: " + str(len(self.ships)) + " tanks: " + str(len(self.tanks))  
        result2 = " helicopters: " + str(len(self.helis)) + res
        return result +result1 +result2



class explosions:
    def __init__(self,x,y,scalex = 20,scaley = 20):
        self.xpos = x
        self.ypos = y
        self.team = None
        self.name = "explosion"
        self.Xscale = scalex
        self.Yscale = scaley
        self.selected = False
        self.rect = pygame.Rect(self.xpos,self.ypos,self.Xscale,self.Yscale)
        self.images = []
        
        self.dead = False
        image = spritesheet("images/ground.png")
        for i in range(5):
            image1 = image.image_at((80 +20 * i,80,20,20))
            image1.set_colorkey(BLACK)
            self.images.append(image1)
        
        for i in range(1,3):
            self.images.append(self.images[- i - 1])
        image1 =image.image_at((180,80,20,20))
        image1.set_colorkey(BLACK)
        for i in range(1):
            self.images.append(image1)
        self.n = len(self.images)
        self.max_life = self.n * 10
        self.life = self.max_life
        self.counter = 0
    def act(self,screen,mapa):
        
        self.show(screen)
        if(self.dead):
            mapa.explosions.remove(self)
            mapa.animated.remove(self)
            
    def show(self,screen):
        if(not self.dead):
            screen.blit(self.images[self.counter],(self.xpos,self.ypos ))
            if(self.life %self.n == 0):
                self.counter = self.counter + 1
                if(self.counter >= self.n):
                    self.counter = self.n - 1
            self.life = self.life - 1
            if(self.life <= 0):
                self.dead = True
    

class shots:
    def __init__(self,x,y,direction,team = None):
        self.xpos = x
        self.ypos = y
        self.Xscale = 10
        self.speed = 5
        self.Yscale = 10
        self.life = 100
        self.direction = direction
        self.dx = self.direction[0]
        self.dy = self.direction[1]
        
        self.team = team
        self.selected = False
        self.name = "shot"
        self.dead = False
        self.power = 20
        image = spritesheet("images/ground.png")
        self.image = image.image_at((140,80,20,20))
        self.image.set_colorkey(BLACK)
        self.rect = pygame.Rect(self.xpos,self.ypos,self.Xscale,self.Yscale)
        self.image = pygame.transform.scale(self.image,(self.Xscale,self.Yscale))
    def move(self):
        self.xpos = self.xpos + self.speed * self.dx
        self.ypos = self.ypos + self.speed * self.dy
        self.rect.x = self.xpos
        self.rect.y = self.ypos
        self.life = self.life - 1
        if(self.life == 0):
            self.dead = True
        
    def show(self,screen):
        screen.blit(self.image,(self.xpos,self.ypos ))
    def act(self,screen,mapa):
        if(self.xpos > mapa.X or self.ypos > mapa.Y or self.xpos * self.ypos <0):
          self.dead = True
        if(self.dead):
            mapa.shots.remove(self)
            mapa.animated.remove(self)
        self.move()
        self.show(screen)
        
        
        
        
