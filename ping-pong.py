#подключение библеотек
from pygame import * 



font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)

#победа и поражение
win = font1.render("Игрок слева проиграл!", True, (180, 0, 0))
lose = font1.render('Игрок справа проиграл!', True, (180, 0, 0))

#подключение фоновой музыки
mixer.init()
mixer.music.load('background.music.ogg')
mixer.music.play()

#подключение звука выстрела
fire_sound = mixer.Sound('fire.ogg')

#подключение звука пропуска врага
missed_enemies = mixer.Sound('cheater.ogg')

hit5 = mixer.Sound('hit5.ogg')
hit10 = mixer.Sound('hit10.ogg')
hit20 = mixer.Sound('hit20.ogg')

#фон
img_back = "background.png" 
#герой
img_hero = "hero.png" 
#пули
img_bullet = "bullet.png" 
#враги
img_enemy = "enemy.png" 
img_enemy1 = "enemy2.png"

#счёт
score = 0 
#сколько очков нужно для победы
goal = 15
#количество пропусков
lost = 0 
#сколько пропусков нужннно чтобы проиграть
max_lost = 6

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
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:

            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

#создание пули
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 17, 40, -15)
        bullets.add(bullet)

#подкласс для счётчика пропуска врагов
class Enemy(GameSprite):

    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
            missed_enemies.play()
#подкласс без счётчика пропусков врагов
class Enemy1(GameSprite):

    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
#класс поподание во врага
class Bullet(GameSprite):

    def update(self):
        self.rect.y += self.speed

        if self.rect.y < 0:
            self.kill()#прописано в классе плеер

#создание окна
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

#создание героя с помощью класса
ship = Player(img_hero, 5, win_height - 130, 110, 150, 10)

#создание врагов с помощью классов и групп
monsters = sprite.Group()
for i in range(1, 4):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 100, 90, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy1(img_enemy1, randint(80, win_width - 80), -40, 50, 50, randint(1, 5))
    asteroids.add(asteroid)


bullets = sprite.Group()

finish = False

run = True 
while run:

    for e in event.get():
        if e.type == QUIT:
            run = False
#при нажатии клавиши пробел будет проигрываться звук и создаваться пули
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
#вывод на экран всех героев
    if not finish:

        window.blit(background,(0,0))
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
#создание счётчиков
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        if score == 5:
            hit5.play()

        if score == 10:
            hit10.play()

        if score == 15:
            hit20.play()


#счётчик пропущенных врагов
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for e in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80),  -40, 100, 90, randint(1, 5))
            monsters.add(monster)

#дохождение врагов до конца карты
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if sprite.spritecollide(ship, asteroids, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
#выигрыш
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
#обновление экрана
        display.update()
    time.delay(50)