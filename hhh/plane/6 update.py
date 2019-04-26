import pygame

pygame.init()

#创建游戏窗口 480*700
screen = pygame.display.set_mode((480,700))

#绘制背景图像
#1>加载图像数据
bg = pygame.image.load("./images/background.png")
#2>bilt绘制图像
screen.blit(bg,(0,0))
#3>update更新屏幕显示
#pygame.display.update()

#绘制英雄图片

hero = pygame.image.load('./images/me1.png')
screen.blit(hero,(150,300))
#pygame.display.update()

#可以在所有绘制工作完成之后，统一调用update方法
pygame.display.update()
while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()

pygame.quit()