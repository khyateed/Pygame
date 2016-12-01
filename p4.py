
# Dig for gold
# Based on Whack-a-mole game using pygame by Kimberly Todd

from pygame import *
from pygame.sprite import *
from random import *


B_WIDTH = 10
B_HEIGHT = 13

       

bgcolor = (40, 40, 60)    #Color taken from background of sprite

class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        p =pygame.image.load("player.png")
        self.image = pygame.transform.scale(p, (75,75))
        self.rect = self.image.get_rect()

    # move gold to a new random location
    def move(self, x_pos, y_pos):

        self.rect.center = (x_pos,y_pos)

    
class Ice(Player):
    def __init__(self, row, col):
        Sprite.__init__(self)
        ice = image.load('ice.png').convert()
        self.image = pygame.transform.scale(ice, (80,80))
        self.rect = self.image.get_rect()
        self.rect.center = (row, col)
class Ball(Player):
     def __init__(self):
        Sprite.__init__(self)
        p =pygame.image.load("ball.png")
        self.image = pygame.transform.scale(p, (40,40))
        self.rect = self.image.get_rect(center=(-20,-20))

     def hit(self, target):
        return self.rect.colliderect(target)

class Gold(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        gold = image.load("gold.bmp").convert_alpha()
        self.image = pygame.transform.scale(gold, (30,30))
        self.rect = self.image.get_rect(center=(-20,-20))

    # move gold to a new random location
    def move(self):
        randX = randint(300, 900)
        randY = randint(0, 700)
        self.rect.center = (randX,randY)






class Bullet(Ball):

    def __init__(self, xpos, ypos, hspeed, vspeed):
        super(Bullet, self).__init__()
        self.image = image.load('bullet.png')
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.hspeed = hspeed
        self.vspeed = vspeed

        self.set_direction()

    def update(self):
        self.rect.x += self.hspeed
        self.rect.y += self.vspeed
        if self.collide():
            self.kill()

    def collide(self):
        if self.rect.x < 0 - B_WIDTH or self.rect.x > WIDTH:
            return True
        elif self.rect.y < 0 - B_HEIGHT or self.rect.y > HEIGHT:
            return True

    def set_direction(self):
        if self.hspeed > 0:
            self.image = pygame.transform.rotate(self.image, 270)
        elif self.hspeed < 0:
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.vspeed > 0:
            self.image = pygame.transform.rotate(self.image, 180)

def random_bullet(speed):
    
    return Bullet(WIDTH, randint(0, HEIGHT), -speed, 0)
      
#######################################################################################
init()


WIDTH=900
HEIGHT=700
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption('Climb through the Ice')

# hide the mouse cursor so we only see shovel
mouse.set_visible(False)


f = font.Font(None, 25)
DELAY = 3000;
##### Constructors ######
player = Player()
ball = Ball()
ice = []
gold=Gold()

bullets =[]
bullet = random_bullet(randint(10,15))
bullets.append(bullet)



screen_rect = screen.get_rect()
rows = range(300,850,100)
cols = range(100,650,100)
for i in rows:
    for j in cols:
        ice.append(Ice(i, j))
        


# creates a group of sprites so all can be updated at once aka every time i mention sprites, i'm talking about gold and shovel. 
sprites = RenderPlain(player, ice, ball, gold, bullets)

x_pos=30
y_pos=30
repeat=True
hits=0
time.set_timer(USEREVENT + 1, DELAY)
# loop until user quits
while True:
    
    e = event.poll()
    

    if e.type == USEREVENT + 1: # TIME has passed
        gold.move()
    elif e.type == KEYDOWN: 
        if e.key == K_q:
            quit()
      
        if e.key == K_UP:
            y_pos -= 20
        if e.key == K_DOWN:
            y_pos += 20
            
        player.move(x_pos, y_pos)
        
       
        if e.key == K_SPACE: 
            x = x_pos
           
            while repeat == True:
                 
                ball.move(x, y_pos)
                sprites.update()
                sprites.draw(screen)
                pygame.display.update()
                screen.fill(bgcolor)
                x+=20
                if ball.hit(gold):
                    mixer.Sound("cha-ching.wav").play()
                    hits +=3
                    gold.move()
                    t = f.render("Score: " + str(hits), False, (255,255,255))
                    screen.blit(t, (320, 0))
                if x > screen_rect.right:
                    mixer.Sound("splash.wav").play()
                    ball.move(-15,-15)
                    break

                for i in ice:
                    if ball.hit(i):
                        
                        repeat = False
                        ice.remove(i)
                        
                        i.kill()
                        ball.move(-15,-15)
                        #i.move(0,0)
                        mixer.Sound("hit.wav").play()
                        hits+=1
                        
                        break
                
                    
            
            repeat = True
            time.set_timer(USEREVENT + 1, DELAY)

    for bullet in bullets:           
        if bullet.hit(player):
            bullet.kill()
            bullet.move(-20,-20)
            print('oops')

    if len(ice)==0:
        break

    # refill background color so that we can paint sprites in new locations
           # draw text to screen.  Can you move it?
    screen.fill(bgcolor)

    t = f.render("Score: " + str(hits), False, (255,255,255))
    screen.blit(t, (320, 0))
    # update and redraw sprites
    sprites.update()
    sprites.draw(screen)
    pygame.display.update()

while True:
    t = font.Font(None, 150).render("You Win! ", False, (255,0,0))
    screen.blit(t, (200, 200))

    t = f.render("Final Score: " + str(hits), False, (255,255,255))
    screen.blit(t, (320, 0))
    t = f.render("Press q to quit", False, (255,255,255))
    screen.blit(t, (400, 400))

    pygame.display.update()
    e = event.poll()
    if e.type == KEYDOWN: 
        if e.key == K_q:
            quit()
    

#thursday morning

