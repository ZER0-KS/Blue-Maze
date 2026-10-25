from pygame import *
import math
import os

mixer.init()

def music(song, loop=True):
    mixer.music.stop()
    mixer.music.load(song)

    if loop:
        mixer.music.play(-1)
    else:
        mixer.music.play()

def sfx(sound):
    effect = mixer.Sound(sound)
    effect.play()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    def update(self):
        if plyr.rect.x <= win_width-80 and plyr.x_speed > 0 or plyr.rect.x >= 0 and plyr.x_speed < 0:
            self.rect.x += self.x_speed
        
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        
        if plyr.rect.y <= win_height-80 and plyr.y_speed > 0 or plyr.rect.y >= 0 and plyr.y_speed < 0:
            self.rect.y += self.y_speed
        
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0: # going down
            for p in platforms_touched:
                
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0: #going up
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        mouse_x, mouse_y = mouse.get_pos()
        angle = math.atan2(mouse_y - self.rect.centery, mouse_x - self.rect.centerx)
        bullet = Bullet(
            'Bullet.png',
            self.rect.centerx,
            self.rect.centery,
            15,
            20,
            15,
            math.cos(angle),
            math.sin(angle),
        )
        bullets.add(bullet)
        sfx("shoot.wav")
    
class Enemy(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = speed
    def update(self):
        if self.rect.x <= 1050:
            self.side = "right"
        if self.rect.x >= win_width - 85:
            self.side = "left"

        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
    def update_y(self):
            if self.rect.y <= 20:
                self.side = "right"
            if self.rect.y >= 600:
                self.side = "left"
    
            if self.side == "left":
                self.rect.y -= self.speed
            else:
                self.rect.y += self.speed

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, speed, direction_x, direction_y):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.rect.center = (player_x, player_y)
        self.speed = speed
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.x_speed = speed * direction_x
        self.y_speed = speed * direction_y

    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
        if (self.rect.right < -10 or self.rect.left > win_width + 10 or
                self.rect.bottom < -10 or self.rect.top > win_height + 10):
            self.kill()

def title_screen():
    img = image.load('Title.png')
    window.fill((255, 255, 255))
    window.blit(transform.scale(img, (win_width, win_height)), (0, 0))

def losing():
    music("losingTheme.mp3", False)

    img = image.load('Game_over.png')
    position = img.get_width() // img.get_height()
    window.fill ((255, 255, 255))
    window.blit(transform.scale(img, (win_width * position, win_height)), (0,0))

def winning():
    music("winningTheme.mp3", False)
    img = image.load('Winning.png')
    position = img.get_width() // img.get_height()
    window.fill ((255, 255, 255))
    window.blit(transform.scale(img, (win_width * position, win_height)), (0,0))

def restart_game():
    global finish

    # Reset player
    plyr.rect.x = 300
    plyr.rect.y = win_height - 100
    plyr.x_speed = 0
    plyr.y_speed = 0

    # Reset enemies
    enmy.rect.x = win_width - 180
    enmy.rect.y = 180
    enmy.side = "left"

    enmy2.rect.x = 685
    enmy2.rect.y = 50
    enmy2.side = "left"

    # Put enemies back into the group
    monsters.add(enmy, enmy2)

    # Remove leftover bullets
    bullets.empty()

    finish = False

    music("maintheme.wav")

win_width = 1280
win_height = 720
display.set_caption("BLUE MAZE")
window = display.set_mode((win_width, win_height))
back = (1, 0, 101)

w1 = GameSprite('Wall.png', 400, 320, 50, 400)
w2 = GameSprite('Wall.png', 200, 320, 400, 50)
w3 = GameSprite('Wall.png', 600, 150, 50, 220)
w4 = GameSprite('Wall.png', 800, 0, 50, 550)
w5 = GameSprite('Wall.png', 1000, 200, 50, 550)

barriers = sprite.Group()
barriers.add(w1)
barriers.add(w2)
barriers.add(w3)
barriers.add(w4)
barriers.add(w5)

bullets = sprite.Group()

plyr = Player('Player.png', 300, win_height - 100, 80, 80, 0, 0)

enmy = Enemy('Enemy.png', win_width - 180, 180, 80, 80, 5)
enmy2 = Enemy('Enemy.png', 685, 50, 80, 80, 5)

monsters = sprite.Group()
monsters.add(enmy)
monsters.add(enmy2)

final_sprite = GameSprite('End.png', win_width - 210, win_height - 80, 200, 80)

run = True
finish = False
title = True

music("titleTheme.mp3", False)
title_screen()

while run:
    time.delay(20)
    
    for e in event.get():

        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:

            # Title screen
            if title:
                if e.key == K_RETURN:
                    title = False
                    restart_game()

            # Winning / losing screen
            elif finish:
                if e.key == K_SPACE:
                    restart_game()
                elif e.key == K_ESCAPE:
                    title = True
                    finish = False
                    music("titleTheme.mp3", False)

            # Main game
            else:
                if e.key == K_a:
                    plyr.x_speed = -5
                elif e.key == K_d:
                    plyr.x_speed = 5
                elif e.key == K_w:
                    plyr.y_speed = -5
                elif e.key == K_s:
                    plyr.y_speed = 5

        elif e.type == MOUSEBUTTONDOWN and not title and not finish:
            plyr.fire()

        elif e.type == KEYUP:
            if e.key == K_a:
                plyr.x_speed = 0
            elif e.key == K_d:
                plyr.x_speed = 0
            elif e.key == K_w:
                plyr.y_speed = 0
            elif e.key == K_s:
                plyr.y_speed = 0


    if not finish:
        if title:
            title_screen()

        elif not finish:
            window.fill(back)
            barriers.draw(window)

            plyr.reset()
            plyr.update()

            if enmy.alive():
                enmy.reset()
                enmy.update()

            if enmy2.alive():
                enmy2.reset()
                enmy2.update_y()

            final_sprite.reset()

            bullets.draw(window)
            bullets.update()

            hit = sprite.groupcollide(monsters, bullets, True, True)
            if hit:
                sfx("die.wav")

            sprite.groupcollide(bullets, barriers, True, False)

            if enmy.alive() and sprite.collide_rect(plyr, enmy):
                finish = True
                losing()

            if enmy2.alive() and sprite.collide_rect(plyr, enmy2):
                finish = True
                losing()

            if sprite.collide_rect(plyr, final_sprite):
                finish = True
                winning()

    if plyr.rect.left < 0:
        plyr.rect.left = 0

    if plyr.rect.right > win_width:
        plyr.rect.right = win_width

    if plyr.rect.top < 0:
        plyr.rect.top = 0

    if plyr.rect.bottom > win_height:
        plyr.rect.bottom = win_height

    display.update()