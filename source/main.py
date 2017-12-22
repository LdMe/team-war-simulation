from classes import *
from time import sleep


def main():
    
    X=600
    Y=600
    Xscale=30
    Yscale=30
    screen = pygame.display.set_mode((X,Y + 2 * Yscale))
    mimapa = mapa(X,Y,Xscale,Yscale)
    game = pygame.init()
    
    print(mimapa.whereIs((100,100)))
    print(mimapa.get(-1,-1))
    mimapa.createmap()
    list_teams = []
    num_teams = 4
    for i in range(num_teams):
        team = teams(randomColor(),i)
        list_teams.append(team)
    mimapa.createDessert((int(random() * X),int(random()* Y)),int(random() * X / Xscale),0.2)
    mimapa.createGrassland((int(random() * X),int(random()* Y)),int(random() * X / Xscale),0.2)
    mimapa.createLake((int(random() * X),int(random()* Y)),int(random() * X / Xscale),0.2)
    print(len(mimapa.trees))
    print("hello")
    mimapa.checkPatches()
    print("world")
    mimapa.createDessert_trees(0.05)
    mimapa.createGrassland_trees(0.1)
    mimapa.createGround_trees(0.1)
    print("war")
    print(len(mimapa.trees))
    active = 1
    for i in list_teams:
           mimapa.create_ships(mimapa.lakes,3,i)
           mimapa.create_tanks(mimapa.ground +mimapa.grasslands + mimapa.desserts,4,i)
           mimapa.create_soldiers(mimapa.ground +mimapa.grasslands + mimapa.desserts,4,i)
           mimapa.create_bases(mimapa.ground +mimapa.grasslands + mimapa.desserts,1,i)
           mimapa.create_bases(mimapa.lakes,1,i,True)
           mimapa.create_planes(mimapa.ground +mimapa.grasslands + mimapa.desserts,3,i)
           mimapa.create_healicopters(mimapa.ground +mimapa.grasslands + mimapa.desserts,3,i)
    mimapa.teams= list_teams
    while(active):
        mimapa.show(screen)
        for i in (mimapa.bases + mimapa.tanks + mimapa.ships + mimapa.explosions +mimapa.helis + mimapa.planes + mimapa.shots):
            i.act(screen,mimapa)
 #       mimapa.showCorner(screen,"up",3,WHITE)
#        mimapa.showCorner(screen,"down",4,BLACK)
#        mimapa.showCorner(screen,"right",3,BLUE)
#        mimapa.showCorner(screen,"left",3,RED)
        pygame.display.update()
        if(not mimapa.fast):
            sleep(0.01)
        active = active + detectaction(mimapa)
        if(active ==2):
            return 1
    return 0
        
a = 1
while(a ==1):
    a = main()




