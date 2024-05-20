import pygame
import time
import random
import asyncio
import time
import random
import sys
from multiprocessing import Process

from pywizlight import wizlight, PilotBuilder, discovery
 
display_width = 1090
display_height = display_width // 3 * 2
 
black = (0,0,0)
white = (255,255,255)

rosa_claro = (249,132,138)
rosa_escuro = (131,30,64)

red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0) 

light_ip = "192.168.1.89" #dev
light_ip = "192.168.1.182" #dev2
light_ip = "192.168.1.9" #prod

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
        text_size = display_width // 30
        smallText = pygame.font.SysFont("lucidafax", text_size)
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
        largetext_size = display_width // 8
        largeText = pygame.font.SysFont("portugalbolditalic", largetext_size)
        TextSurf, TextRect = text_objects("A Terça Casa", largeText, rosa_escuro)
        TextRect.center = ((display_width/2), (display_height/2) - display_width // 6)
        gameDisplay.blit(TextSurf, TextRect)

        for button in buttons:
            button.draw()

        pygame.display.update()

async def acender_lampada_main():
    global light
    print("acende")
    await light.turn_on(PilotBuilder(rgb = (255, 255, 255), brightness = 255))

def acender_lampada_fade_in():
    parar_terramoto()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(acender_lampada_fade_in_main())

async def acender_lampada_fade_in_main():
    global light
    print("acende")
    brightness = 0
    while brightness <= 255:
        await light.turn_on(PilotBuilder(rgb = (255, 255, 255), brightness = brightness))
        brightness += 1

def acender_lampada():
    if lampada_a_piscar:
        parar_terramoto()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(acender_lampada_main())

async def apagar_lampada_main():
    global light
    print("apaga")
    await light.turn_off()

def apagar_lampada():
    if lampada_a_piscar:
        parar_terramoto()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(apagar_lampada_main())

def parar_lampada_a_piscar():
    global lampada_process
    global lampada_a_piscar
    if lampada_process and lampada_process.is_alive():
        lampada_process.terminate()
        lampada_a_piscar = False

async def piscar_lampada_main():
    global light
    await light.turn_off()
    await asyncio.sleep(random.randint(3, 10) * 0.01)
    await light.turn_on(PilotBuilder(brightness = 100))
    await asyncio.sleep(random.randint(1, 4) * 0.01)
    await light.turn_off()
    await asyncio.sleep(random.randint(1, 4) * 0.01) 
    await light.turn_on(PilotBuilder(brightness = 100))
    await asyncio.sleep(random.randint(1, 4) * 0.01) 

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
    acender_lampada()

def poder():
    call_piscar_lampada_with_subprocess(n_flickers=3)

def terramoto():
    pygame.mixer.music.load('audio/earthquake_big.wav')
    pygame.mixer.music.play(-1)
    call_piscar_lampada_with_subprocess(n_flickers=300)

def mutantes():
    pygame.mixer.music.load('audio/mutantes.mp3')
    pygame.mixer.music.play(-1)

def esfrega():
    pygame.mixer.music.load('audio/esfrega.mp3')
    pygame.mixer.music.play(-1)

def explosao():
    explosao = pygame.mixer.Sound('audio/explosion.mp3')   
    explosao.play() 

async def pressentimento_main():
    global light
    await light.turn_on(PilotBuilder(brightness = 100))

def pressentimento():
    if lampada_a_piscar:
        parar_terramoto()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(pressentimento_main())

async def tensao_main():
    global light
    await light.turn_on(PilotBuilder(rgb = (255, 50, 0), brightness = 255))

def tensao():
    if lampada_a_piscar:
        parar_terramoto()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tensao_main())

async def party_main():
    global light
    await light.turn_on(PilotBuilder(scene = 4))

def party():
    if lampada_a_piscar:
        parar_terramoto()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(party_main())

if __name__ == "__main__":
    button_height = display_height // 13
    button_width = display_width // 4
    button_y = display_height // 5 * 2
    button_margin = button_height // 3 * 2
    left_column_x = display_width // 2 - button_width - button_margin - (button_width // 2)
    middle_column_x = display_width // 2 - (button_width // 2)
    right_column_x = display_width // 2 + button_margin + (button_width // 2)
    print(left_column_x, button_y)
    buttons.append(Button("PODER!", left_column_x, button_y, button_width, button_height, rosa_escuro, black, poder))   
    buttons.append(Button("Mutantes", middle_column_x, button_y, button_width, button_height, rosa_escuro, black, mutantes))
    buttons.append(Button("TERRAMOTO!!!", right_column_x, button_y, button_width, button_height, rosa_escuro, black, terramoto))
    button_y += button_margin + button_height
    buttons.append(Button("Acender lâmpada", left_column_x, button_y, button_width, button_height, rosa_escuro, black, acender_lampada))
    buttons.append(Button("Te(n)são", middle_column_x, button_y, button_width, button_height, rosa_escuro, black, tensao))
    buttons.append(Button("Explosão", right_column_x, button_y, button_width, button_height, rosa_escuro, black, explosao))
    button_y += button_margin + button_height
    buttons.append(Button("Apagar lâmpada", left_column_x, button_y, button_width, button_height, rosa_escuro, black, apagar_lampada))
    buttons.append(Button("Esfrega esfrega", middle_column_x, button_y, button_width, button_height, rosa_escuro, black, esfrega))
    buttons.append(Button("Parar terramoto", right_column_x, button_y, button_width, button_height, rosa_escuro, black, parar_terramoto))
    button_y += button_margin + button_height
    buttons.append(Button("Pressentimento", left_column_x, button_y, button_width, button_height, rosa_escuro, black, pressentimento))
    buttons.append(Button("Luz com bue fade in", middle_column_x, button_y, button_width, button_height, rosa_escuro, black, acender_lampada_fade_in))
    buttons.append(Button("Party?", right_column_x, button_y, button_width, button_height, rosa_escuro, black, party))
    button_y += button_margin + button_height

    pygame.init() 
    gameDisplay = pygame.display.set_mode((display_width,display_height))
    pygame.display.set_caption('A Terça Casa') 
    game_intro()
    pygame.quit()
    quit()