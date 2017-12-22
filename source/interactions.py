import pygame
from random import random
from random import choice
from math import *

def rot_center(image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect
def collideWith(me,wall):
    result = False
    if me.rect.colliderect(wall.rect) and me != wall and me.speed != 0:
        #if(abs(me.dx)> abs(me.dy)):
                if (me.dx > 0 and  me.rect.right -wall.rect.left  <= me.max_speed): # Moving right; Hit the left side of the wall
                    me.rect.right = wall.rect.left
#                    me.dx = -me.dx
                    me.xpos = me.rect.x
                    result = True
                if (me.dx < 0 and wall.rect.right - me.rect.left <= me.max_speed): # Moving left; Hit the right side of the wall
                    me.rect.left = wall.rect.right
#                    me.dx = -me.dx
                    me.xpos = me.rect.x
                    result = True
        #elif(abs(me.dx)< abs(me.dy)):
        
                if (me.dy > 0 and me.rect.bottom - wall.rect.top <= me.max_speed):
                    me.rect.bottom = wall.rect.top
#                    me.dy = -me.dy
                    me.ypos = me.rect.y
                    result = True
                if (me.dy < 0 and  wall.rect.bottom - me.rect.top <= me.max_speed): # Moving up; Hit the bottom side of the wall
                    me.rect.top = wall.rect.bottom
  #                  me.dy = -me.dy
                    me.ypos = me.rect.y
                    result = True
                me.speed = 0
    return result

def detectaction(mapa):
    pos = (0,0)
    for event in pygame.event.get():
        if(event.type == pygame.KEYDOWN ):
            if (event.key == pygame.K_r):
                return 1
            elif (event.key == pygame.K_ESCAPE):
                return -1
            elif (event.key == pygame.K_p):
                for i in mapa.selected:
                    print(i)
            elif (event.key == pygame.K_f):
                mapa.fast = not mapa.fast
            elif (event.key == pygame.K_s):
                for i in mapa.animated:
                    try:
                        i.showbars = not i.showbars
                    except:
                        pass
        if(event.type == pygame.MOUSEBUTTONDOWN ):
            pos =pygame.mouse.get_pos()
            done = False
            p = mapa.whereIs(pos)
            print(p)
            if(pygame.mouse.get_pressed()[2] ):
                
                mapa.create_towers([],1,oneOf(mapa.teams),p)
            for j in mapa.animated:
                    if(j.rect.collidepoint(pos)and not j.selected):
                        j.selected = True
                        mapa.selected.append(j)
                        done = True
                        print(j)
                    else:
                        if(j.selected):
                            j.selected = False
                            if(j in mapa.selected):
                                mapa.selected.remove(j)
        if(event.type == pygame.MOUSEBUTTONUP ):
            if(pygame.mouse.get_pos() == pos):
                pass
                
            
    return 0



def detectaction1(mapa):
    pos = (0,0)
    for event in pygame.event.get():
        if(event.type == pygame.KEYDOWN ):
            if (event.key == pygame.K_r):
                return 1
            elif (event.key == pygame.K_ESCAPE):
                return -1
        if(event.type == pygame.MOUSEBUTTONDOWN ):
            pos =pygame.mouse.get_pos()
        if(event.type == pygame.MOUSEBUTTONUP ):
            if(pygame.mouse.get_pos() == pos):
                done = False
                print("true")
                for j in mapa.animated:
                    if(j.rect.collidepoint(pos)):
                        j.selected = True
                        mapa.selected.append(j)
                        done = True
                        print(done,pos)
                    else:
                        if(j.selected):
                            j.selected = False
                            if(j in mapa.selected):
                                mapa.selected.remove(j)
                
            
    return 0
def detectaction_ejemplo(h,maxpos,m,base,M,L):
    selection = 0
    if(m.R != 0):
        for p in L.people:
            if(p.xpos > m.R[0] and p.xpos < m.R[0]+ m.R[2]):
                if(p.ypos > m.R[1] and p.ypos < m.R[1]+ m.R[3]):
                    p.selected = 1
               # else:
#                    p.selected = 0
#            else :
#                p.selected = 0

    for event in pygame.event.get():
        
        if(event.type == pygame.MOUSEBUTTONDOWN ):
            pos =pygame.mouse.get_pos()
            
            
            m.button =(pygame.mouse.get_pressed())
            if(m.button == m.LEFT):
                if(not m.rectstart):
                  m.rectstart = pos
                  m.rect = pygame.Rect(m.rectstart[0],m.rectstart[1],m.rectstart[0]-pos[0],m.rectstart[1]-pos[1])
                    
                else:
                    m.rect = pygame.Rect(m.rectstart[0],m.rectstart[1],m.rectstart[0]-pos[0],m.rectstart[1]-pos[1])
                    
            selectperson(m,L,pos)
            
            
                        
        elif(event.type == pygame.MOUSEBUTTONUP ):
            m.pulsed = 0
            m.rectstart = 0
            m.rect = 0
            m.R = 0
            if( M.pos == 3 ):#!!wall selection visual
                M.pos = 0
            
                M.selection = ""
            
            
        elif(event.type == pygame.KEYDOWN ):
            M.pos = 0
            M.selection = ""
            if (event.key == pygame.K_ESCAPE):
                return 2
        
        if (event.type == pygame.MOUSEMOTION):
            m.act(event.pos)
            if(m.pulsed and m.button == m.LEFT):            
                m.rect = pygame.Rect(m.rectstart[0],m.rectstart[1],m.rectstart[0]-event.pos[0],m.rectstart[1]-event.pos[1])
  
        

    return 0

def minDof(me,lista):
    x = me.xpos
    y = me.ypos
    dist = 10000
    chosen = 0
    for i in lista:
        dx = x - i.xpos
        dy = y - i.ypos
        distance = sqrt(dx ** 2 + dy ** 2)
        if(distance < dist):
            chosen = i
            dist = distance
    return chosen


def oneOf(lista):
    if(len(lista)> 0):
        result = int(random() * len(lista))
        return lista[result]
    
    return 0


def randomColor():
    R = int(random() * 250)
    G = int(random() * 250)
    B = int(random() * 250)
    return (R,G,B)

