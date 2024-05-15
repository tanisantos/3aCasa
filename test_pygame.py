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

light_ip = "192.168.1.4" #prod
#light_ip = "192.168.1.89" #dev

lampada_a_piscar = False

light = wizlight(light_ip)
lampada_process = None

buttons = []

random.seed(42)

def text_objects(text, font, color=white):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

class Button:
    def __init__(self, msg, x, y, w, h, ic, ac, action):
        self.msg = msg
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.ic = ic
        self.ac = ac
        self.action = action
        self.was_clicked = False

    def is_hovered(self):
        mouse = pygame.mouse.get_pos()
        return self.x+self.w > mouse[0] > self.x and self.y+self.h > mouse[1] > self.y
    
    def is_clicked(self):
        click = pygame.mouse.get_pressed()
        return click[0] == 1


    def draw(self):
        if self.is_hovered():
            pygame.draw.rect(gameDisplay, self.ac,(self.x, self.y, self.w, self.h))
            if self.is_clicked():
                if not self.was_clicked:
                    self.was_clicked = True
                    self.action()
            else:
                self.was_clicked = False
            
        else:
            pygame.draw.rect(gameDisplay, self.ic,(self.x, self.y, self.w, self.h))
        smallText = pygame.font.SysFont("lucidafax", 20)
        textSurf, textRect = text_objects(self.msg, smallText)
        textRect.center = ( (self.x+(self.w/2)), (self.y+(self.h/2)) )
        gameDisplay.blit(textSurf, textRect)        


def quitgame():
    pygame.quit()
    quit()

def game_intro():
    global buttons

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(rosa_claro)
        largeText = pygame.font.SysFont("portugalbolditalic",115)
        TextSurf, TextRect = text_objects("A Terça Casa", largeText, rosa_escuro)
        TextRect.center = ((display_width/2), (display_height/2) - 100)
        gameDisplay.blit(TextSurf, TextRect)

        for button in buttons:
            button.draw()

        pygame.display.update()

async def acender_lampada_main():
    global light
    print("acende")
    await light.turn_on(PilotBuilder(brightness = 255))

def acender_lampada():
    if lampada_a_piscar:
        parar_lampada_a_piscar()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(acender_lampada_main())

async def apagar_lampada_main():
    global light
    print("apaga")
    await light.turn_off()

def apagar_lampada():
    loop = asyncio.get_event_loop()
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
    await asyncio.sleep(random.randint(1, 10) * 0.01)
    await light.turn_on(PilotBuilder(brightness = 255))
    await asyncio.sleep(random.randint(1, 10) * 0.01) 

def piscar_lampada(n_flickers=10):
    loop = asyncio.get_event_loop()
    for i in range(n_flickers):
        print(i)
        loop.run_until_complete(piscar_lampada_main())

def call_piscar_lampada_with_subprocess(n_flickers=10):
    global lampada_a_piscar
    global lampada_process
    if lampada_a_piscar:
        parar_lampada_a_piscar()
    lampada_a_piscar = True
    lampada_process = Process(target=piscar_lampada, args=[n_flickers])
    lampada_process.start()

def parar_terramoto():
    # fadeout time is in milliseconds
    pygame.mixer.music.fadeout(3000)
    parar_lampada_a_piscar()

def poder():
    call_piscar_lampada_with_subprocess(n_flickers=8)

def terramoto():
    pygame.mixer.music.load('audio/earthquake.mp3')
    pygame.mixer.music.play(-1)
    call_piscar_lampada_with_subprocess(n_flickers=100)

def explosao():
    explosao = pygame.mixer.Sound('audio/explosion.mp3')   
    explosao.play() 

if __name__ == "__main__":
    buttons.append(Button("PODER!", 200, 300, 200, 50, rosa_escuro, black, poder))   
    buttons.append(Button("Acender lâmpada", 200, 300+75, 200, 50, rosa_escuro, black, acender_lampada))
    buttons.append(Button("Apagar lâmpada", 200, 375+75, 200, 50, rosa_escuro, black, apagar_lampada))
    buttons.append(Button("TERRAMOTO!!!", 200+200+50, 300, 200, 50, rosa_escuro, black, terramoto))
    buttons.append(Button("Explosão", 200+200+50, 300+75, 200, 50, rosa_escuro, black, explosao))
    buttons.append(Button("Parar terramoto", 200+200+50, 375+75, 200, 50, rosa_escuro, black, parar_terramoto))
    pygame.init() 
    gameDisplay = pygame.display.set_mode((display_width,display_height))
    pygame.display.set_caption('A Terça Casa') 
    game_intro()
    pygame.quit()
    quit()