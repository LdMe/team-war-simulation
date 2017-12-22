import pygame

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




class buttons:
    def __init__(self,x,y,color= 0,btype = 0,sizeX = 160,sizeY = 80):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.image = spritesheet("buttons.png")
        self.select_button(btype,color)
        self.xpos = x
        self.ypos = y
        self.image1.set_colorkey(BLACK)
        self.image2.set_colorkey(BLACK)
        self.rect = pygame.Rect(x,y,self.sizeX,self.sizeY)
        self.pressed = False
        self.presscounter = 0
        self.timer = 5
    def reset(self):
        self.pressed = False
    def press(self):
        self.pressed = True
        self.presscounter = self.timer
    def select_button(self,btype,color):
        if(btype == 0):
           self.image1 = self.image.image_at(( 0,color *100,160,80))
           self.image2 = self.image.image_at(( 160,color * 100,160,80))
           self.image1 = pygame.transform.scale(self.image1,(self.sizeX,self.sizeY))
           self.image2 = pygame.transform.scale(self.image2,(self.sizeX,self.sizeY))
         
        elif(btype == 1):
           self.sizeX = self.sizeY
           self.image1 = self.image.image_at(( 340,color *100,100,100))
           self.image2 = self.image.image_at(( 460,color * 100,100,100))
           self.image1 = pygame.transform.scale(self.image1,(self.sizeX,self.sizeY))
           self.image2 = pygame.transform.scale(self.image2,(self.sizeX,self.sizeY))
         
        else:
            self.sizeY = 100
            self.sizeX = 100
        
    def show(self,screen):
         if(self.pressed):
            self.presscounter = self.presscounter - 1
            if(self.presscounter <=0):
                self.presscounter = 0
 #               self.pressed = False
            screen.blit(self.image2,(self.xpos,self.ypos))
            
         else:
            screen.blit(self.image1,(self.xpos,self.ypos))
        
