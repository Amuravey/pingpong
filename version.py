from pygame import *
import random

win_up = 500
win_line = 700

lostb = 0
lostr = 0
last_hit = None

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width=65, height=65):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.width = width
        self.height = height
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def update_image(self):
        self.image = transform.scale(image.load(self.image_path), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y



class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width=65, height=65):
        super().__init__(player_image, player_x, player_y, player_speed, width, height)
        self.image_path = player_image # Сохраняем путь к изображению
        self.x = player_x
        self.y = player_y

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
            self.x = self.rect.x
        if keys[K_RIGHT] and self.rect.x < win_line - 65:
            self.rect.x += self.speed
            self.x = self.rect.x

    def increase_size(self, scale_factor):
        self.width = int(self.width * scale_factor)
        self.height = int(self.height * scale_factor)
        self.image = transform.scale(image.load(self.image_path), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x + self.width//2, self.y + self.height//2)

class Player2(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width=65, height=65):
        super().__init__(player_image, player_x, player_y, player_speed, width, height)
        self.image_path = player_image
        self.x = player_x
        self.y = player_y

    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
            self.x = self.rect.x
        if keys[K_d] and self.rect.x < win_line - 65:
            self.rect.x += self.speed
            self.x = self.rect.x

    def increase_size(self, scale_factor):
        self.width = int(self.width * scale_factor)
        self.height = int(self.height * scale_factor)
        self.image = transform.scale(image.load(self.image_path), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x + self.width//2, self.y + self.height//2)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width=30, height=30):
        super().__init__(player_image, player_x, player_y, player_speed, width, height)
        self.speed_x = 1
        self.speed_y = 1

    def update(self):
        global blue_c, red_c

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


        if self.rect.y <= 0:
            time.delay(50)
            self.rect.x = win_line // 2
            self.rect.y = win_up // 2
            self.speed_y *= -1
            blue_c = False # мяч коснулся верхней границы, теперь blue_c = True
            red_c = True #red_c = False

        if self.rect.y >= win_up - 30:
            time.delay(50)
            global lostb
            lostb += 1
            self.rect.x = random.randint(0, win_line - 30) #FIX
            self.rect.y = 350
            self.speed_y *= -1
            red_c = False # коснулся нижней границы, red_c = True
            blue_c = True #blue_c = False

        if self.rect.x <= 0:
            self.speed_x *= -1
        if self.rect.x >= win_line - 30:
            self.speed_x *= -1


class Boost(GameSprite):
    def __init__(self, player_image, player_x, player_y, width=30, height=30):
         super().__init__(player_image, player_x, player_y, 0, width, height)


blueP = Player('palkablue2.png', 250, 400, 6, 100, 50)

redP = Player2('redpalka.png', 250, 50, 6, 100, 100)

ball = Enemy('ball.png', 350, 200, 0, 30, 30)

boost = Boost('boost.png', random.randint(50, 650), random.randint(50, 450), 30, 30) 
boostspeed = Boost('boostspeed.png', random.randint(50, 650), random.randint(50, 450), 30, 30)

font.init()
font1 = font.SysFont('Arial', 35)
lose = font1.render('BLUE LOSE', True, (180, 0, 0))
win = font1.render('RED WIN', True, (180, 0, 0))
window = display.set_mode((win_line, win_up))
display.set_caption('pingpong')
backgrond = transform.scale(
    image.load('galaxy.jpg'), (win_line, win_up)
    )

clock = time.Clock()
FPS = 100

game = True
finish = False
blue_c = False
red_c = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.blit(backgrond, (0,0))
        blueP.update()
        blueP.reset()
        redP.update()
        redP.reset()
        ball.update()
        ball.reset()
        boost.reset()
        boostspeed.reset()


        if sprite.collide_rect(blueP, ball):
            if blue_c == False:
                ball.speed_y *= -1
                blue_c = True
                last_hit = blueP
                red_c = False
        if sprite.collide_rect(redP, ball):
            if red_c == False:
                ball.speed_y *= -1
                last_hit = redP # Кто последний отбил мяч
                red_c = True
                blue_c = False

        if sprite.collide_rect(ball, boost):
            if last_hit == blueP:
                blueP.increase_size(1.1) #Увеличиваем на 10%
                blueP.speed +=1
            elif last_hit == redP:
                redP.increase_size(1.1)
                redP.speed +=1
            boost = Boost('boost.png', random.randint(50, 650), random.randint(50, 450), 30, 30) # Новое положение

        if sprite.collide_rect(ball, boostspeed):
            ball.speed_x *= 1.2
            ball.speed_y *= 1.2
            boostspeed = Boost('boostspeed.png', random.randint(50, 650), random.randint(50, 450), 30, 30)

        if lostb >= 3:
            finish = True
            window.blit(lose, (200, 200))

        if lostr >= 3:
            finish = True
            window.blit(win, (200, 200))

        display.update()
    clock.tick(FPS)
