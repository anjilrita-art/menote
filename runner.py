import pygame
from sys import exit
pygame.init()

screen =pygame.display.set_mode((800,400))
pygame.display.set_caption("Anjil game")
clock = pygame.time.Clock()
txt_fornt=pygame.font.Font(None,50)


sky_surface=pygame.image.load("sky.png")
ground_surface=pygame.image.load("ground.png")
txt_surface=txt_fornt.render("Snail Game",True,"black")
snail_surface=pygame.image.load("snail2.png")
snail_x_pos=600
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_surface,(0,0))     
    screen.blit(ground_surface,(0,300))  
    screen.blit(txt_surface,(300,0)) 
    snail_x_pos -= 4
    if snail_x_pos < -100: snail_x_pos = 800
    screen.blit(snail_surface,(snail_x_pos,265))


    pygame.display.update()
    clock.tick(60)

