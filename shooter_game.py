#Создай собственный Шутер!
from pygame import *
import random
import time as tm

mixer.init()
mixer.music.load('space.ogg')
bullet_music = mixer.Sound('fire.ogg')
# mixer.music.play()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, speed, x, y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
    def fill(self):
        draw.rect(window, (255, 0, 0), self.rect)
        
class Player(GameSprite):
    def move(self):
        keys_pressed = key.get_pressed()   
        if keys_pressed[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        elif keys_pressed[K_s] and self.rect.y < height - 60:
            self.rect.y += self.speed
        elif keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        elif keys_pressed[K_d] and self.rect.x < width - 60:
            self.rect.x += self.speed
            
    def fire(self):
        bullet = Bullet('bullet.png', speed=3, x=self.rect.x+22, y=self.rect.y-20)
        bullets.add(bullet)
            
class Enemy(GameSprite):
    def update(self):
        if self.rect.y > height:
            self.rect.x = random.randint(1, width - 100)
            self.rect.y = 0
            global lose
            lose = lose + 1
        else:
            self.rect.y += self.speed
            
class Bullet(GameSprite):
    def __init__(self, player_image, speed, x, y):
        super().__init__(player_image, speed, x, y)
        self.image = transform.scale(image.load(player_image), (20, 20))
        self.rect = Rect(x, y, 20, 20)
        
    def update(self):
        if self.rect.y <= 0:
            self.kill()
        else:
            self.rect.y -= self.speed  

height = 900
width = 1100
window = display.set_mode((width, height))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (width, height))
clock = time.Clock()
fps = 60
player = Player('rocket.png', speed=10, x=300, y=400)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
last_n = []

for i in range(5):
    x = random.randint(1, width)
    speed = random.randint(1, 3)   
    monster = Enemy('ufo.png', speed=speed, x=x, y=0)
    monsters.add(monster)


for i in range(2):
    x = random.randint(1, width)
    speed = random.randint(1, 2)   
    asteroid = Enemy('asteroid.png', speed=speed, x=x, y=0)
    asteroids.add(asteroid) 
    

lose = 0
win = 0
life = 3
num_fire = 0
start_time = 0
reload = False
finish = False
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 70)
lose_t = font2.render('YOU LOOSE', True, (255, 0, 0))
win_t = font2.render('YOU WIN', True, (0, 128, 0))
reload_t = font2.render('Wait, reload...', True, (235, 0, 0))

game = True
while game:
    for e in event.get():
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            if num_fire < 5 and reload == False:
                player.fire()
                bullet_music.play()    
                num_fire += 1  
            if num_fire >= 5 and reload == False:
                reload = True   
                start_time = tm.time()   
                   
                
        if e.type == QUIT:
            game = False
            
    if not finish:
        text_lose = font1.render('Пропущено:'+ str(lose), 1, (255, 255, 255))
        text_win = font1.render('Счет:'+ str(win), 1, (255, 255, 255))
        life_t = font1.render(str(life), 1, (0, 228, 0))
        window.blit(background, (0, 0))
        window.blit(text_win, (0, 10))
        window.blit(text_lose, (0, 40))
        window.blit(life_t, (width-40, 40))
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        player.reset() 
            
    if reload == True:
        end_time = tm.time()
        if end_time - start_time < 2:
            window.blit(reload_t, ((width/2) - 150, height - 50))
        else:
            num_fire = 0
            reload = False
            
        
    for asteroid in asteroids:
        if asteroid.rect.y == height:
            lose -= 1
    
    if sprite.groupcollide(bullets, monsters, True, True):
        win += 1
        x = random.randint(1, width - 120)
        speed = random.randint(1, 3)
        monster = Enemy('ufo.png', speed=speed, x=x, y=0)        
        monsters.add(monster)
        
    if sprite.spritecollide(player, asteroids, True):
        life -= 1
        x = random.randint(1, width - 100)
        speed = random.randint(1, 2)
        asteroid = Enemy('asteroid.png', speed=speed, x=x, y=0)
        asteroids.add(asteroid)
        
    if sprite.spritecollide(player, monsters, True):
        life -= 1
        x = random.randint(1, width - 120)
        speed = random.randint(1, 3)
        monster = Enemy('ufo.png', speed=speed, x=x, y=0)        
        monsters.add(monster)        
            
    player.move()
    monsters.update()
    asteroids.update()
    bullets.update()
    
    if win >= 30:
        window.blit(win_t, (250, 250))
        finish = True
    elif lose >= 3 or life <= 0:
        window.blit(lose_t, (250, 250))
        finish = True
        
    
    clock.tick(fps)
    display.update()