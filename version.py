from pygame import *
import random

win_up = 500
win_line = 700

lostb = 0
lostr = 0
last_hit = None

#Остальной код GameSprite, Player, Player2, Enemy, Boost остается без изменений

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
            blue_c = True # мяч коснулся верхней границы, теперь blue_c = True
            red_c = False #red_c = False

        if self.rect.y >= win_up - 30:
            time.delay(50)
            global lostb
            lostb += 1
            self.rect.x = random.randint(0, win_line - 30) #FIX
            self.rect.y = 350
            self.speed_y *= -1
            red_c = True # коснулся нижней границы, red_c = True
            blue_c = False #blue_c = False

        if self.rect.x <= 0:
            self.speed_x *= -1
        if self.rect.x >= win_line - 30:
            self.speed_x *= -1
