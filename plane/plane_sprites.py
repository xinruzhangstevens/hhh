import random
import pygame

#屏幕大小的常量
SCREEN_RECT = pygame.Rect(0,0,480,700)
#刷新的帧率
#FRAME_PER_SEC = 60
#创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
#英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1
#创建boss定时器常量
CREATE_BOSS_EVENT =pygame.USEREVENT+2
#创建bubble定时器常量
CREATE_BUBBLE_EVENT = pygame.USEREVENT +3

class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, image_name, speed = 10,speedy = 0):

        #***调用父类的初始化方法
        super().__init__()

        #定义对象的属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.speedy = speedy

    def update(self):

        #在屏幕的垂直方向上移动
        self.rect.y +=self.speed


class Background(GameSprite):
    """游戏背景精灵"""
    def __init__(self,is_alt= False):
        #1.调用父类方法实现精灵的创建(image/rect/speed)
        super().__init__('./images/background.png')
        #判断是否是交替图像，如果是，需要设置初始位置
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):

        #1.调用父类的方法实现
        super().update()
        #2。判断图像是否移出屏幕，如果移出屏幕，将图像设置到屏幕的上方
        if self.rect.y>=SCREEN_RECT.height:
            self.rect.y = -self.rect.height

class Enemy(GameSprite):
    """敌机精灵"""

    def __init__(self):

        #1.调用父类方法，创建敌机精灵，同时指定敌机图片
        super().__init__('./images/enemy1.png')
        #2.指定敌机的初始随机速度  1~3
        self.speed = random.randint(1,6)
        #3.指定敌机的初始随机位置
        self.rect.bottom = 0
        self.explode_index = 0

        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0,max_x)

    def update(self):

        #1.调用父类方法，保持垂直方向的飞行
        super().update()
        #2.判断是否废除屏幕，如果是，需要从精灵组删除敌机
        if self.rect.y>=SCREEN_RECT.height:
            #print('fly out of the screen ,delete it.')
            #kill方法可以将精灵从所有精灵组中移出，精灵就会被自动销毁
            self.kill()

        # #销毁敌机
        # if self.explode_index == 5:
        #     self.kill()

        #敌机爆炸
        if self.explode_index!= 0 and self.explode_index <  5:
            new_rect = self.rect
            super().__init__('./images/enemy1_down%d.png'% self.explode_index)
            self.explode_index += 1
            self.rect = new_rect


    def __del__(self):
        #print("敌机挂了 %s" % self.rect)
        pass

class Hero(GameSprite):
    """英雄精灵"""
    def __init__(self):

        #1.调用父类方法，设置image&speed
        super().__init__('./images/me1.png',0)
        #2。设置英雄的初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom-120
        #3.创建子弹精灵组
        self.bullets = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.mainexplode_index =0

    def update(self):
        #英雄在水平方向移动
        self.rect.x += self.speed
        self.rect.y +=self.speedy
        #控制英雄不能离开屏幕
        if self.rect.x < 0 :
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
        if self.rect.y < 0 :
            self.rect.y = 0
        elif self.rect.bottom > SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.bottom

        #飞机爆炸
        if self.mainexplode_index !=0 and self.mainexplode_index <5:
            new_rect = self.rect
            super().__init__('./images/me_destroy_%d.png'% self.mainexplode_index)
            self.rect.centerx = new_rect.centerx
            self.rect.bottom = new_rect.bottom
            self.mainexplode_index += 1
            self.rect = new_rect

    def fire(self):
        #print('fire')
        for i in (0,1,2):
            #1.创建子弹精灵
            bullet= Bullet()
            #2。设置精灵的位置
            bullet.rect.bottom = self.rect.y-20
            bullet.rect.centerx = self.rect.centerx+20-i*20
            #3。将精灵添加到精灵组
            self.bullets.add(bullet)

class Bullet(GameSprite):
    """子弹精灵"""
    def __init__(self):
        #调用父类方法，设置子弹图片，设置初始速度
        super().__init__('./images/bullet1.png',-2)

    def update(self):
        #调用父类方法，让子弹沿垂直方向飞行
        super().update()
        #判断子弹是否飞出屏幕
        if self.rect.bottom<0:
            self.kill()

    def __del__(self):
        print('子弹被销毁')

class Boss(GameSprite):
    """boss精灵"""
    def __init__(self):
        #1.调用父类方法，设置image
        super().__init__('./images/enemy3_n1.png')
        #2。设置初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.top = SCREEN_RECT.top
        #3。创建武器精灵组
        self.weapons = pygame.sprite.Group()
        self.exist = False
        self.bossexplode_index = 0
        self.bulletseating = 0

    def update(self):
        self.rect.x +=self.speed
        if self.rect.x < 0 :
            self.rect.x = 0
            self.speed=-self.speed
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
            self.speed=-self.speed
        # 飞机爆炸
        if self.bossexplode_index !=0 and self.bossexplode_index <7 :
            new_rect = self.rect
            super().__init__('./images/enemy3_down%d.png' % self.bossexplode_index)
            self.rect.centerx = new_rect.centerx
            self.rect.bottom = new_rect.bottom
            self.bossexplode_index += 1
            self.rect = new_rect
    def bubble(self):
        for i in (0,1):
            weapon = Weapon()
            weapon.rect.bottom = self.rect.bottom+50
            weapon.rect.centerx = self.rect.centerx+20-i*20
            self.weapons.add(weapon)
class Weapon(GameSprite):
    """武器精灵"""
    def __init__(self):
        super().__init__('./images/enemy3_down6.png',10)
    def update(self):
        super().update()
        if self.rect.y>SCREEN_RECT.height:
            self.kill()