import pygame
import time
import random
import asyncio
import time
import random
import sys
from multiprocessing import Process

from pywizlight import wizlight, PilotBuilder, discovery
 
display_width = 900
display_height = 600
 
black = (0,0,0)
white = (255,255,255)

rosa_claro = (249,132,138)
rosa_escuro = (131,30,64)

red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0) 

# light_ip = "192.168.1.4" #prod
light_ip = "192.168.1.89" #dev

lampada_a_piscar = False

light = wizlight(light_ip)
loop = asyncio.get_event_loop()
lampada_process = None

def text_objects(text, font, color=white):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def button(msg,x,y,w,h,ic,ac,action,*args):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("lucidafax", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
    

def quitgame():
    pygame.quit()
    quit()


def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(rosa_claro)
        largeText = pygame.font.SysFont("portugalbolditalic",115)
        TextSurf, TextRect = text_objects("A Terça Casa", largeText, rosa_escuro)
        TextRect.center = ((display_width/2), (display_height/2) - 100)
        gameDisplay.blit(TextSurf, TextRect)

        button("PODER!", 200, 300, 200, 50, rosa_escuro, black, poder)        
        button("Acender lâmpada", 200, 300+75, 200, 50, rosa_escuro, black, acender_lampada)
        button("Apagar lâmpada", 200, 375+75, 200, 50, rosa_escuro, black, apagar_lampada)
        button("TERRAMOTO!!!", 200+200+50, 300, 200, 50, rosa_escuro, black, terramoto, 6)
        button("Parar terramoto", 200+200+50, 300+75, 200, 50, rosa_escuro, black, parar_terramoto)

        pygame.display.update()

async def acender_lampada_main():
    global light
    await light.turn_on(PilotBuilder(brightness = 255))

def acender_lampada():
    global loop
    loop.run_until_complete(acender_lampada_main())

async def apagar_lampada_main():
    global light
    await light.turn_off()

def apagar_lampada():
    global loop
    loop.run_until_complete(apagar_lampada_main())

def parar_lampada_a_piscar():
    global lampada_process
    global lampada_a_piscar
    if lampada_a_piscar and lampada_process and lampada_process.is_alive():
        lampada_process.terminate()
        lampada_a_piscar = False

async def piscar_lampada_main():
    global light
    await light.turn_off()
    time.sleep(random.randint(1, 10) * 0.01)
    await light.turn_on(PilotBuilder(brightness = 255))
    time.sleep(random.randint(1, 10) * 0.01) 

def piscar_lampada(n_flickers=10):
    global lampada_a_piscar
    global loop
    lampada_a_piscar = True
    for i in range(n_flickers):
        print(i)
        loop.run_until_complete(piscar_lampada_main())
    lampada_a_piscar = False

def call_piscar_lampada_with_subprocess(n_flickers=10):
    global lampada_a_piscar
    global lampada_process
    if lampada_a_piscar:
        parar_lampada_a_piscar()
    lampada_process = Process(target=piscar_lampada, args=[n_flickers])
    lampada_process.start()

def parar_terramoto():
    global loop
    global lampada_a_piscar
    if lampada_a_piscar:
        pygame.mixer.music.pause()
        parar_lampada_a_piscar()

def poder():
    call_piscar_lampada_with_subprocess(n_flickers=8)

def terramoto():
    pygame.mixer.music.load('audio/earthquake.mp3')
    pygame.mixer.music.play(-1)
    call_piscar_lampada_with_subprocess(n_flickers=6)    

if __name__ == "__main__":
    pygame.init() 
    gameDisplay = pygame.display.set_mode((display_width,display_height))
    pygame.display.set_caption('A Terça Casa') 
    game_intro()
    pygame.quit()
    quit()