
# Dig for gold
# Based on Whack-a-mole game using pygame by Kimberly Todd

from pygame import *
from pygame.sprite import *
from random import *


       

bgcolor = (140, 170,255)    #Color taken from background of sprite

class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        p =pygame.image.load("player.png")
        self.image = pygame.transform.scale(p, (75,75))
        self.rect = self.image.get_rect()

    # move gold to a new random location
    def move(self, x_pos, y_pos):

        self.rect.center = (x_pos,y_pos)

    def hit(self, target):
        return self.rect.colliderect(target)

class Ice(Player):
    def __init__(self, row, col):
        Sprite.__init__(self)
        ice = image.load('ice.png').convert()
        self.image = pygame.transform.scale(ice, (80,80))
        self.rect = self.image.get_rect()
        self.rect.center = (row, col)

######################################################################
init()

screen = display.set_mode((900, 700))
display.set_caption('Climb through the Ice')

# hide the mouse cursor so we only see shovel
mouse.set_visible(False)

f = font.Font(None, 25)

# create the mole and shovel using the constructors
player = Player()
ice = []
rows = range(300,850,100)
cols = range(100,650,100)
for i in rows:
    for j in cols:
        ice.append(Ice(i, j))
        
        
        pygame.display.update()


# creates a group of sprites so all can be updated at once aka every time i mention sprites, i'm talking about gold and shovel. 
sprites = RenderPlain(player, ice)



x_pos=30
y_pos=30
hits=0
# loop until user quits
while True:
    e = event.poll()
    if e.type == QUIT:
        quit()
        break

         
    elif e.type == KEYDOWN: 
    
        # if e.key == K_LEFT:
        #     x_pos -= 20
        # if e.key == K_RIGHT:
        #     x_pos += 20
        if e.key == K_UP:
            y_pos -= 20
        if e.key == K_DOWN:
            y_pos += 20
        player.move(x_pos, y_pos)
        
        for x in ice:
            if player.hit(x):
                x.kill()
                x.move(0,0)
                mixer.Sound("hit.wav").play()
                hits+=1
            

        


    # refill background color so that we can paint sprites in new locations
    screen.fill(bgcolor)
    t = f.render("Score: " + str(hits), False, (0,0,0))
    screen.blit(t, (320, 0))        # draw text to screen.  Can you move it?

    # update and redraw sprites
    sprites.update()
    sprites.draw(screen)
    pygame.display.update()
