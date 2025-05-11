from pygame import *


win_up = 500
win_line = 700

# Класс для спрайтов игры
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


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed() 
        if keys[K_LEFT] and self.rect.x > 0: 
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_line - 65: 
            self.rect.x += self.speed


class Player2(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0: 
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_line - 65:
            self.rect.x += self.speed


class Enemy(GameSprite):   #Класс врага
    def update(self):    #Метод для движения
        global lost
        if self.rect.y >= 500:   #Если координата у > 500 (спрайт очень низко)
            self.rect.y = 0  #Перемещаем спрайт наверх
            self.rect.x = randint(0, win_line - 65) # чтобы не вылетали за край
            lost = lost + 1
        else:  #Если координата у < 500 (не достигли низа)
            self.rect.y += self.speed #Увеличиваем координату (спрайт плывет вниз)


blueP = Player('palkablue2.png', 250, 400, 6 )
redP = Player2('redpalka.png', 250, 50, 6)

ball = Enemy('')

window = display.set_mode((win_line, win_up))
display.set_caption('pingpong')
backgrond = transform.scale(
    image.load('pole.jpg'), (win_line, win_up)
    )


clock = time.Clock()
FPS = 90

game = True
while game:    
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.blit(backgrond, (0,0))
    blueP.update()
    blueP.reset()
    redP.update()
    redP.reset()   
    display.update()
    clock.tick(FPS)