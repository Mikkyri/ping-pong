#подключение библеотек
from pygame import * 

#класс для создания персонажей
class GameSprite(sprite.Sprite):

#пораметры для персонажей
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#подкласс для передвижения героя
class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_width - 80:
            self.rect.y += self.speed
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_u] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_width - 80:
            self.rect.y += self.speed

#создание окна и его пораметры
back = (200, 255, 255)
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
window.fill(back)

#флаги, отвечающие за состояние игры
game = True
finish = False
clock = time.Clock()
FPS = 60

#создание игроков
raketL = Player('qqq.png', 30, 200, 4, 50, 150)
raketR = Player('qqq.png', 30, 200, 4, 50, 150)
#создание мяча
ball = GameSprite('boll.png', 200, 200, 4, 50, 50)

font.init()
font = font.Font(None, 35)
#победа и поражение
win = font1.render("Левый игрок выиграл!", True, (180, 0, 0))
lose = font1.render('Правый игрок выиграл!', True, (180, 0, 0))

speed_x = 3
speed_y = 3

while game:
    for e in event.get():
        if e.type == QUIT:
            run = False
#вывод на экран всех героев
    if finish != True:

        window.fill(back)
        raketL.update_l()
        raketR.update_r()
        ball.rect.x += speed_x
        ball.rect.y += speed_y
        
        if sprite.collide_rect(raketL, ball) or sprite.collide_rect(raketR, ball):
            speed_x *= -1
            speed_y *= 1
        
        #если мяч достигает границ экрана, меняем направление его движения
        if ball.rect.y > win_height-50 or ball.rect.y < 0:
            speed_y *= -1
        
#если мяч улетел дальше ракетки, выводим условие проигрыша для второго игрока
        if ball.rect.x < 0:
            finish = True
            window.blit(lose1, (200, 200))
            game_over = True
        
#если мяч улетел дальше ракетки, выводим условие проигрыша для второго игрока
        if ball.rect.x < 0:
            finish = True
            window.blit(lose2, (200, 200))
            game_over = True
        
        raketL.reset()
        raketR.reset()
        ball.reset()
        

    display.update()
    clock.tick(FPS)
