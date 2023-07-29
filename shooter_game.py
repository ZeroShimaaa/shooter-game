#Create your own shooter

from pygame import *
from random import *
from time import time as timer

finish = False
FPS = 60
game = True
clock = time.Clock()
win_width=700
win_height=500
window = display.set_mode((700, 500))
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
lost = 0
score = 0
goal = 20
max_lost = 10
life = 3
rel_time = False
num_fire = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class PlayerClass(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed 
        if key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15)
        bullets.add(bullet)

class enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()
rocket = PlayerClass('rocket.png', 5, win_height - 100, 10)
monsters = sprite.Group()
for i in range(5):
    monster = enemy('ufo.png', randint(80, win_width - 80), -40, randint(1,5))
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(3):
    asteroid = enemy('asteroid.png', randint(30, win_width - 30), -40, randint(1, 7))
    asteroids.add(asteroid)


font.init()
font2 = font.SysFont("Arial", 36)
font1 = font.SysFont("Arial", 36)
win = font1.render('You win', True, (255, 255, 255))
lose = font2.render('You lose', True, (180, 0, 0))
mixer.init()
mixer.music.load('space.ogg') 
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg') 
while game: 
    if finish != True:
        window.blit(background,(0,0))
        bullets.update()
        bullets.draw(window)
        rocket.update()
        rocket.reset()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        text_lose = font2.render('Missed:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 20))

        collides = sprite.groupcollide(monsters,  bullets, True, True)

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...',1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0 
                rel_time = False

        if sprite.spritecollide(rocket, monsters, False) or sprite.spritecollide(rocket, monsters, False):
            sprite.spritecollide(rocket, monsters, True)
            sprite.spritecollide(rocket, asteroids, True)
            life = life - 1
        
        if life == 0 or lost >= max_lost:
            finish = True 
            window.blit(lose, [200, 200])
        
        text_life = font1.render(str(life), 1, (0, 150, 0))
        window.blit(text_life, (600, 10))

        for c in collides:
            score = score + 1
            monster = enemy('ufo.png', randint(80, win_width - 80), -40, randint(1,5))
            monsters.add(monster)
        if score >= 10:
            finish = True
            window.blit(win, (200, 200))
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    rocket.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True    
    display.update()
    clock.tick(FPS)