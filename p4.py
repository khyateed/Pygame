
# Dig for gold
# Based on Whack-a-mole game using pygame by Kimberly Todd

from pygame import *
from pygame.sprite import *
from random import *
import math

B_WIDTH = 20
B_HEIGHT = 60
bgcolor = (40, 40, 60) 
       

   

class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        p =pygame.image.load("player.png")
        self.image = pygame.transform.scale(p, (75,75))
        self.rect = self.image.get_rect(center=(450,650))

  
    def move(self, x_pos, y_pos):
        self.rect.center = (x_pos,y_pos)   

class Gold(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        gold = image.load("gold.bmp").convert_alpha()
        self.image = pygame.transform.scale(gold, (30,30))
        self.rect = self.image.get_rect(center=(-20,-20))

    # move gold to a new random location
    def move(self):
        randX = randint(0, 900)
        randY = randint(0, 500)
        self.rect.center = (randX,randY)

class Ice(Player):
    def __init__(self, row, col):
        Sprite.__init__(self)
        ice = image.load('ice.png').convert()
        self.image = pygame.transform.scale(ice, (80,80))
        self.rect = self.image.get_rect(center=(row,col))

class Ball(Player):
     def __init__(self):
        Sprite.__init__(self)
        p =pygame.image.load("ball.png")
        self.image = pygame.transform.scale(p, (40,40))
        self.rect = self.image.get_rect(center=(-20,-20))

     def hit(self, target):
        return self.rect.colliderect(target)


class Bullet(Ball):

    def __init__(self, xpos, ypos, hspeed, vspeed):
        super(Bullet, self).__init__()
        icicle = image.load('bullet.png')
        self.image = pygame.transform.scale(icicle, (20,60))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.hspeed = hspeed
        self.vspeed = vspeed

        #self.set_direction()

    def update(self):
        self.rect.x += self.hspeed
        self.rect.y += self.vspeed
        if self.collide():
            self.move(randint(100,800),0)

    def collide(self):
        if self.rect.x < 0 - B_WIDTH or self.rect.x > WIDTH:
            return True
        elif self.rect.y < 0 - B_HEIGHT or self.rect.y > HEIGHT:
            return True

    def set_direction(self):
        self.image = pygame.transform.rotate(self.image, 180)

class Lives(Sprite):
    def __init__(self,col):
        Sprite.__init__(self)
        p =pygame.image.load("heart.png")
        self.image = pygame.transform.scale(p, (40,40))
        self.rect = self.image.get_rect(center=(col,20))

  
    def move(self, x_pos, y_pos):
        self.rect.center = (x_pos,y_pos)   

  
def random_bullet(speed):
    
    return Bullet(randint(0, WIDTH), 0, 0, speed)

def draw_background(background_img):
    background_rect = background_img.get_rect()
    background_rect_width = background_rect.width
    background_rect_height = background_rect.height
    for i in range(math.ceil(WIDTH / background_rect.width)):
        for j in range(math.ceil(HEIGHT / background_rect.height)):
            screen.blit(background_img, Rect(i * background_rect_width,
                                             j * background_rect_height,
                                             background_rect_width,
                                             background_rect_height))


def draw_ice():
    ice = []
    rows = range(300,850,100)
    cols = range(100,650,100)
    for i in rows:
      for j in cols:
        ice.append(Ice(i, j))
    return ice
def draw_lives():
    lives =[]
    cols = range(50,150,40)
    for i in cols:
        lives.append(Lives(i))
    return lives
def win(hits):
    while True:
        draw_background(background_img)
        t = font.Font(None, 150).render("You Win! ", False, (100,0,255))
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
        

def lose(hits):
    while True:
        draw_background(background_img)
        t = font.Font(None, 150).render("You lost ", False, (255,0,0))
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

#################################### Main ###################################################
init()


WIDTH=900
HEIGHT=700
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption('Climb through the Ice')
background_img = background_img = pygame.image.load('back.png')
f = font.Font(None, 40)
DELAY = 3000;

################ Constructors #################

screen_rect = screen.get_rect()
ice=draw_ice()
lives=draw_lives()
player = Player()
ball = Ball()
gold=Gold()
bullet = random_bullet(randint(10,15))



sprites = RenderPlain(player, ice, ball, gold, bullet, lives)




x_pos=450
y_pos=650
repeat=True
hits=0
time.set_timer(USEREVENT + 1, DELAY)



#################### Game Loop ###########################
while True:
    
    e = event.poll()
    if e.type == USEREVENT + 1: # TIME has passed
        gold.move()
    elif e.type == KEYDOWN: 
        if e.key == K_q:
            quit()
        if e.key == K_RIGHT:
            x_pos += 25
        if e.key == K_LEFT:
            x_pos -= 25
            
        player.move(x_pos, y_pos)
        
        if e.key == K_SPACE: 
            y = y_pos   
            
            while repeat == True:   
                draw_background(background_img)

                ball.move(x_pos, y)
                sprites.update()
                sprites.draw(screen)
                pygame.display.update()
                screen.fill(bgcolor)
                y-=25
                
                if ball.hit(gold):
                    mixer.Sound("cha-ching.wav").play()
                    hits +=3
                    gold.move()
                    t = f.render("Score: " + str(hits), False, (255,255,255))
                    screen.blit(t, (320, 0))

                if y < screen_rect.top:
                    mixer.Sound("splash.wav").play()
                    ball.move(-15,-15)
                    break

                for i in ice:
                    if ball.hit(i):  
                        repeat = False
                        ice.remove(i)
                        i.kill()
                        ball.move(-15,-15)
                        mixer.Sound("hit.wav").play()
                        hits+=1
                        break
            repeat = True
            time.set_timer(USEREVENT + 1, DELAY)


    for l in lives:
        if bullet.hit(player):
            bullet.move(-20,-20)
            l.kill()
            lives.remove(l)
            mixer.Sound("bullet.wav").play()
            bullet.move(-20,-20)

  
            
            
    if len(lives)==0:
        lose(hits)
    if len(ice)==0:
        win(hits)

    # refill background 
    draw_background(background_img)
    t = f.render("Score: " + str(hits), False, (255,255,255))
    screen.blit(t, (320, 0))
    # update and redraw sprites
    sprites.update()
    sprites.draw(screen)
    pygame.display.update()


