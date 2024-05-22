import pygame
import time
import random
import asyncio
import time
import random
import sys
from multiprocessing import Process
import pyautogui

from pywizlight import wizlight, PilotBuilder, discovery
 
display_width = pyautogui.size().width
display_height = pyautogui.size().height * 0.9
 
black = (0,0,0)
white = (255,255,255)

rosa_claro = (249,132,138)
rosa_escuro = (131,30,64)

red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0) 

light_ip = "192.168.1.9"
light = wizlight(light_ip) 
lampada_process = None

buttons = []

random.seed(42)

def text_objects(text, font, color=white):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

class Button:
    button_count_per_column = {}
    def __init__(self, msg, w, h, x, column_name, buttons_y_start, height_step, ic, ac, text_color, action):
        if isinstance(Button.button_count_per_column.get(column_name, None), int):
            Button.button_count_per_column[column_name] += 1
        else:
            Button.button_count_per_column[column_name] = 0
        self.msg = msg
        self.x = x
        self.y = buttons_y_start + (Button.button_count_per_column[column_name] * height_step)
        self.w = w
        self.h = h
        self.ic = ic
        self.ac = ac
        self.text_color = text_color
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
        text_size = display_width // 50
        # smallText = pygame.font.SysFont("lucidafax", text_size)
        smallText = pygame.font.Font("Segoe UI Symbol.ttf", text_size)
        textSurf, textRect = text_objects(self.msg, smallText, self.text_color)
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
        largetext_size = display_width // 10
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

async def acender_lampada_fade_in_main(light):
    print("acende")
    brightness = 0
    while brightness <= 255:
        await light.turn_on(PilotBuilder(rgb = (255, 255, 255), brightness = brightness))
        brightness += 1

def acender_lampada_fade_in(light):
    parar_lampada()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(acender_lampada_fade_in_main(light))

def call_acender_lampada_fade_in_with_subprocess():
    parar_lampada()
    global lampada_process
    global light
    lampada_process = Process(target=acender_lampada_fade_in, args=[light])
    lampada_process.start()

def acender_lampada():
    parar_lampada()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(acender_lampada_main())

async def apagar_lampada_main():
    global light
    print("apaga")
    await light.turn_off()

def apagar_lampada():
    parar_lampada()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(apagar_lampada_main())

def parar_lampada():
    global lampada_process
    if lampada_process and lampada_process.is_alive():
        lampada_process.terminate()

async def piscar_lampada_main(light):
    await light.turn_off()
    await asyncio.sleep(random.randint(3, 10) * 0.01)
    await light.turn_on(PilotBuilder(brightness = 100))
    await asyncio.sleep(random.randint(1, 4) * 0.01)
    await light.turn_off()
    await asyncio.sleep(random.randint(1, 4) * 0.01) 
    await light.turn_on(PilotBuilder(brightness = 100))
    await asyncio.sleep(random.randint(1, 4) * 0.01) 

def piscar_lampada(light, n_flickers=10):
    loop = asyncio.get_event_loop()
    for i in range(n_flickers):
        print(i)
        loop.run_until_complete(piscar_lampada_main(light))
    

def call_piscar_lampada_with_subprocess(n_flickers=10):
    parar_lampada()
    global lampada_process
    global light
    lampada_process = Process(target=piscar_lampada, args=[light, n_flickers])
    lampada_process.start()


def parar_terramoto():
    # fadeout time is in milliseconds
    pygame.mixer.music.fadeout(3000)
    parar_lampada()
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
    parar_lampada()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(pressentimento_main())

async def tensao_main():
    global light
    await light.turn_on(PilotBuilder(rgb = (255, 50, 0), brightness = 255))

def tensao():
    parar_lampada()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tensao_main())

async def party_main():
    global light
    await light.turn_on(PilotBuilder(scene = 4))

def party():
    parar_lampada()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(party_main())

def sound_stop():
    pygame.mixer.music.stop()

def sound_fade_out():
    pygame.mixer.music.fadeout(3000)

async def discover_bulbs_main():
    global light_ip
    try:
        bulbs = await discovery.discover_lights(broadcast_space="192.168.1.255")
        light_ip = bulbs[0].ip
    except Exception as e:
        print(e)
        light_ip = "192.168.1.9"

def discover_bulbs():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(discover_bulbs_main())

if __name__ == "__main__":

    # """ discover lights """
    # discover_bulbs()
    # print(light_ip)
    # # light = wizlight(light_ip)

    """ page layout settings """
    n_columns = 3
    page_horizontal_margin = display_width // 10
    page_vertical_margin = display_height // 10

    buttons_y_start = display_height // 6 * 2
    button_height = display_height // 13
    button_margin = button_height // 3 * 2
    button_panel_width = display_width - (page_horizontal_margin * 2)
    basic_controls_width = button_height * 2
    button_width = (button_panel_width - (n_columns * button_margin) - basic_controls_width) // n_columns
    height_step = button_height + button_margin

    """ basic controls """
    column_id = "controls"
    x_coord = page_horizontal_margin
    col_kwargs = {"w":basic_controls_width, "h": button_height, "x": x_coord, "column_name": column_id, 
                  "buttons_y_start": buttons_y_start, "height_step": height_step, "ic": white, "ac": black, "text_color": rosa_escuro}
    buttons.append(Button("🔊⏹", **col_kwargs, action=sound_stop))
    buttons.append(Button("🔊▼", **col_kwargs, action=sound_fade_out))
    buttons.append(Button("💡✅", **col_kwargs, action=acender_lampada))
    buttons.append(Button("💡❌", **col_kwargs, action=apagar_lampada))
    # buttons.append(Button("⏹", **col_kwargs, action=parar_terramoto))

    """ action buttons """
    column_id = "musica"
    x_coord += button_margin + basic_controls_width
    col_kwargs = {"w":button_width, "h": button_height, "x": x_coord, "column_name": column_id, 
                  "buttons_y_start": buttons_y_start, "height_step": height_step, "ic": rosa_escuro, "ac": black, "text_color": white}
    buttons.append(Button("Mutantes", **col_kwargs, action=mutantes))
    buttons.append(Button("Musica1", **col_kwargs, action=mutantes))
    buttons.append(Button("Musica2", **col_kwargs, action=mutantes))
    buttons.append(Button("Musica3", **col_kwargs, action=mutantes))
    buttons.append(Button("Esfrega esfrega", **col_kwargs, action=esfrega))

    """"""
    column_id = "luzes"
    x_coord += button_margin + button_width
    col_kwargs = {"w":button_width, "h": button_height, "x": x_coord, "column_name": column_id, 
                  "buttons_y_start": buttons_y_start, "height_step": height_step, "ic": rosa_escuro, "ac": black, "text_color": white}
    buttons.append(Button("Luz tensão", **col_kwargs, action=tensao))
    buttons.append(Button("Luz fade in", **col_kwargs, action=call_acender_lampada_fade_in_with_subprocess))
    buttons.append(Button("Luz fraca", **col_kwargs, action=pressentimento))
    buttons.append(Button("Party?", **col_kwargs, action=party))
    
    """"""
    column_id = "outros"
    x_coord += button_margin + button_width
    col_kwargs = {"w":button_width, "h": button_height, "x": x_coord, "column_name": column_id, 
                  "buttons_y_start": buttons_y_start, "height_step": height_step, "ic": rosa_escuro, "ac": black, "text_color": white}
    buttons.append(Button("PODER!", **col_kwargs, action=poder))
    buttons.append(Button("TERRAMOTO!!!", **col_kwargs, action=terramoto))
    buttons.append(Button("Explosão", **col_kwargs, action=explosao)) # pode-se remover?
    buttons.append(Button("Parar terramoto", **col_kwargs, action=parar_terramoto))

    """"""    
    pygame.init() 
    gameDisplay = pygame.display.set_mode((display_width,display_height))
    pygame.display.set_caption('A Terça Casa') 
    game_intro()
    pygame.quit()
    quit()