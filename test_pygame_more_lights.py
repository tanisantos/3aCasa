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
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

display_width = int(pyautogui.size().width * 0.7)
display_height = int(pyautogui.size().height * 0.7)
 
black = (0,0,0)
white = (255,255,255)

rosa_claro = (249,132,138)
rosa_escuro = (131,30,64)

red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0) 

light_ips = {
             "Lustre"    : "192.168.1.145",
             "Luz3"      : "192.168.1.144",
             "Cozinha"   : "192.168.1.143",
             "Sala 1"    : "192.168.1.148",
             "Sala 2"    : "192.168.1.149",
            #  "Foco"      : "192.168.1.222",
             }

light_names = light_ips.keys()

cold_rgb = (175, 255, 255)
warm_rgb = (255, 255, 255)
dim_rgb  = (255, 75, 75)
# blue_rgb  = (10, 10, 255)
blue_rgb  = (0, 0, 255)
red_rgb  = (255, 25, 25)

lights = {key: wizlight(value) for key, value in light_ips.items()}

lampadas_processes = {key: None for key, _ in light_ips.items()}

buttons = []

random.seed(42)

def text_objects(text, font, color=white):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

class Button:
    button_count_per_column = {}
    def __init__(self, msg, w, h, x, column_name, buttons_y_start, height_step, ic, ac, text_color, action, args=[]):
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
        self.args = args
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
                    self.action(*self.args)
            else:
                self.was_clicked = False
            
        else:
            pygame.draw.rect(gameDisplay, self.ic,(self.x, self.y, self.w, self.h))
        text_size = display_width // 50
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
        largetext_size = display_width // 8
        largeText = pygame.font.SysFont("portugalbolditalic", largetext_size)
        TextSurf, TextRect = text_objects("A Terça Casa", largeText, rosa_escuro)
        TextRect.center = ((display_width/2), (display_height/2) - display_width // 6)
        gameDisplay.blit(TextSurf, TextRect)

        for button in buttons:
            button.draw()

        pygame.display.update()

async def acender_lampada_main(lampada, rgb):
    global lights
    light = lights[lampada]
    print(f"acende {lampada}")
    
    if lampada == 'Luz3':
        if (rgb == cold_rgb or rgb == blue_rgb):
            # await light.turn_on(PilotBuilder(cold_white=100, brightness = 255))
            print("KJyfkugkjhfg")
            await light.turn_on(PilotBuilder(warm_white=100, cold_white=0, brightness = 255))
        elif rgb == dim_rgb or rgb == red_rgb:
            await light.turn_on(PilotBuilder(warm_white=100, brightness = 255))
        else:
            await light.turn_on(PilotBuilder(warm_white=100, cold_white=100, brightness = 255))
    else:
        await light.turn_on(PilotBuilder(rgb = rgb, brightness = 255))

def acender_lampada(lampada, rgb):
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(acender_lampada_main(lampada, rgb))
    except:
        print(f"Erro: {lampada} não acendeu")

def acender_lampadas(lampadas, rgb):
    parar_lampadas_processes(lampadas)
    global light_names
    apagar_lampadas([l for l in light_names if l not in lampadas])
    for lampada in lampadas:
        lampadas_processes[lampada] = Process(target=acender_lampada, args=[lampada, rgb])
        lampadas_processes[lampada].start()

async def apagar_lampada_main(lampada):
    global lights
    light = lights[lampada]
    print(f"apaga {lampada}")
    await light.turn_off()

def apagar_lampada(lampada):
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(apagar_lampada_main(lampada))
    except:
        print(f"Erro: {lampada} não apagou")

def apagar_lampadas(lampadas):
    parar_lampadas_processes(lampadas)
    for lampada in lampadas:
        lampadas_processes[lampada] = Process(target=apagar_lampada, args=[lampada])
        lampadas_processes[lampada].start()

def parar_lampadas_processes(lampadas):
    global lampadas_processes
    for lampada in lampadas:
        lampada_process = lampadas_processes[lampada]
        if lampada_process and lampada_process.is_alive():
            lampadas_processes[lampada].terminate()

async def piscar_lampada_main(lampada, rgb):
    global lights
    print(f"piscando {lampada} {rgb}")
    light = lights[lampada]
    try:
        await light.turn_off()
        await asyncio.sleep(random.randint(3, 10) * 0.02)

        if lampada == 'Luz3':
            if (rgb == cold_rgb or rgb == blue_rgb):
                # await light.turn_on(PilotBuilder(cold_white=100, brightness = 255))   
                await light.turn_on(PilotBuilder(warm_white=100, brightness = 255))
            elif rgb == dim_rgb or rgb == red_rgb:
                await light.turn_on(PilotBuilder(warm_white=100, brightness = 255))
            else:
                await light.turn_on(PilotBuilder(warm_white=100, cold_white=100, brightness = 255))
        else:
            await light.turn_on(PilotBuilder(rgb = rgb, brightness = 255))

        await asyncio.sleep(random.randint(1, 4) * 0.02)
        await light.turn_off()
        await asyncio.sleep(random.randint(1, 4) * 0.02) 

        if lampada == 'Luz3':
            if (rgb == cold_rgb or rgb == blue_rgb):
                # await light.turn_on(PilotBuilder(cold_white=100, brightness = 255))
                await light.turn_on(PilotBuilder(warm_white=100, brightness = 255))
            elif rgb == dim_rgb or rgb == red_rgb:
                await light.turn_on(PilotBuilder(warm_white=100, brightness = 255))
            else:
                await light.turn_on(PilotBuilder(warm_white=100, cold_white=100, brightness = 255))
        else:
            await light.turn_on(PilotBuilder(rgb = rgb, brightness = 255))

        await asyncio.sleep(random.randint(1, 4) * 0.02) 
    except:
        print(f"Erro: {lampada} não piscou")


def piscar_lampada(lampada, rgb, n_flickers=10):
    loop = asyncio.get_event_loop()
    for i in range(n_flickers):
        print(i)
        loop.run_until_complete(piscar_lampada_main(lampada, rgb))

def call_piscar_lampadas_with_subprocess(lampadas, rgb, n_flickers=10):
    global lampadas_processes
    parar_lampadas_processes(lampadas)
    print("parar lampada process")
    for lampada in lampadas:
        print("piscando:", lampada)
        lampadas_processes[lampada] = Process(target=piscar_lampada, args=[lampada, rgb, n_flickers])
        lampadas_processes[lampada].start()

def parar_terramoto(lampadas, rgb):
    print("parar terramoto", lampadas)
    parar_lampadas_processes(lampadas)
    acender_lampadas(lampadas, rgb)

def poder(lampadas, rgb):
    call_piscar_lampadas_with_subprocess(lampadas, rgb, n_flickers=3)

async def pressentimento_main(lampada):
    global lights
    light = lights[lampada]
    await light.turn_on(PilotBuilder(brightness = 100))

async def tensao_main(lampada):
    global lights
    light = lights[lampada]
    await light.turn_on(PilotBuilder(rgb = (255, 50, 0), brightness = 255))

def terramoto(lampadas, rgb):
    call_piscar_lampadas_with_subprocess(lampadas, rgb, n_flickers=400)

def cozinha_azul():
    # apagar_lampadas(['Luz3'])
    # acender_lampadas(['Lustre', 'Cozinha'], blue_rgb)
    acender_lampadas(light_names, blue_rgb)

    
def sala():
    apagar_lampadas(['Cozinha'])
    acender_lampadas(['Lustre', 'Luz3'], warm_rgb)

if __name__ == "__main__":

    """ page layout settings """
    n_columns = 4
    page_horizontal_margin = display_width // 8
    page_vertical_margin = display_height // 10

    buttons_y_start = display_height // 6 * 2
    button_height = display_height // 13
    button_margin = button_height // 3 * 2
    button_panel_width = display_width - (page_horizontal_margin * 2)
    # basic_controls_width = button_height * 2
    button_width = (button_panel_width - (n_columns * button_margin)) // n_columns
    # button_width = (button_panel_width - (n_columns * button_margin) - 2 * ()) // n_columns

    height_step = button_height + button_margin

    light_names = light_ips.keys()
    light_names_cozinha = ["Cozinha"]
    light_names_sala = ["Lustre", "Luz3", "Sala 1", "Sala 2"]


    """ light """
    column_id = "xxx"
    x_coord = page_horizontal_margin - button_margin - button_margin
    # Button.button_count_per_column[column_id] = 0
    col_kwargs = {"w": button_margin, "h": button_height, "x": x_coord, "column_name": column_id, 
                  "buttons_y_start": buttons_y_start, "height_step": height_step, "ic": rosa_escuro, "ac": black, "text_color": white}
    buttons.append(Button("✅", **col_kwargs, action=acender_lampadas, args=[['Lustre'], warm_rgb]))
    # buttons.append(Button("Luz4 (Foco)", **col_kwargs, action=poder, args=[['Foco'], cold_rgb]))

    """ Setup """
    column_id = "setup"
    x_coord = page_horizontal_margin
    # Button.button_count_per_column[column_id] = 0
    col_kwargs = {"w": button_width, "h": button_height, "x": x_coord, "column_name": column_id, 
                  "buttons_y_start": buttons_y_start, "height_step": height_step, "ic": rosa_escuro, "ac": black, "text_color": white}
    buttons.append(Button("Luz1 (Lustre)", **col_kwargs, action=poder, args=[['Lustre'], warm_rgb]))
    buttons.append(Button("Luz2 (Cozinha)", **col_kwargs, action=poder, args=[['Cozinha'], warm_rgb]))
    buttons.append(Button("Luz3 (Cand. Pé)", **col_kwargs, action=poder, args=[['Luz3'], cold_rgb]))
    buttons.append(Button("Luz4 (Sala 1)", **col_kwargs, action=poder, args=[['Sala 1'], warm_rgb]))
    buttons.append(Button("Luz5 (Sala 2)", **col_kwargs, action=poder, args=[['Sala 2'], warm_rgb]))
    # buttons.append(Button("Luz4 (Foco)", **col_kwargs, action=poder, args=[['Foco'], cold_rgb]))

    """ Essentials """
    column_id = "controls"
    x_coord += button_margin + button_width
    col_kwargs = {"w":button_width, "h": button_height, "x": x_coord, "column_name": column_id, 
                  "buttons_y_start": buttons_y_start, "height_step": height_step, "ic": white, "ac": black, "text_color": rosa_escuro}
    buttons.append(Button("💡💡💡✅", **col_kwargs, action=acender_lampadas, args=[light_names, warm_rgb]))
    buttons.append(Button("💡💡💡❌", **col_kwargs, action=apagar_lampadas, args=[light_names]))
    buttons.append(Button("PODER!", **col_kwargs, action=poder, args=[["Lustre", "Luz3"], warm_rgb]))
    buttons.append(Button("TERRAMOTO!!!", **col_kwargs, action=terramoto, args=[light_names, warm_rgb]))
    buttons.append(Button("Terramoto ❌", **col_kwargs, action=parar_terramoto, args=[light_names, warm_rgb]))

    """ Cenas """
    column_id = "Cozinha"
    # Button.button_count_per_column[column_id] = 0
    x_coord += button_margin + button_width
    col_kwargs = {"w":button_width, "h": button_height, "x": x_coord, "column_name": column_id, 
                  "buttons_y_start": buttons_y_start, "height_step": height_step, "ic": rosa_escuro, "ac": black, "text_color": white}
    buttons.append(Button("Cozinha ✅", **col_kwargs, action=acender_lampadas, args=[light_names_cozinha, cold_rgb]))
    buttons.append(Button("Cozinha ❌", **col_kwargs, action=apagar_lampadas, args=[light_names_cozinha]))
    buttons.append(Button("Cozinha dim", **col_kwargs, action=acender_lampadas, args=[light_names_cozinha, dim_rgb]))
    buttons.append(Button("Cozinha azul", **col_kwargs, action=acender_lampadas, args=[[*light_names_cozinha, 'Lustre', 'Luz3'], blue_rgb]))

    column_id = "Sala"
    # Button.button_count_per_column[column_id] = 0
    x_coord += button_margin + button_width
    col_kwargs = {"w":button_width, "h": button_height, "x": x_coord, "column_name": column_id, 
                  "buttons_y_start": buttons_y_start, "height_step": height_step, "ic": rosa_escuro, "ac": black, "text_color": white}
    buttons.append(Button("Sala ✅", **col_kwargs, action=acender_lampadas, args=[light_names_sala, warm_rgb]))
    buttons.append(Button("Sala ❌", **col_kwargs, action=apagar_lampadas, args=[light_names_sala]))
    buttons.append(Button("Sala dim", **col_kwargs, action=acender_lampadas, args=[light_names_sala, dim_rgb]))
    buttons.append(Button("Sala red", **col_kwargs, action=acender_lampadas, args=[light_names_sala, red_rgb]))

    # column_id = "Dama das Neves"
    # # Button.button_count_per_column[column_id] = 0
    # x_coord += button_margin + button_width
    # col_kwargs = {"w":button_width, "h": button_height, "x": x_coord, "column_name": column_id, 
    #               "buttons_y_start": buttons_y_start, "height_step": height_step, "ic": rosa_escuro, "ac": black, "text_color": white}
    # buttons.append(Button("Foco ✅", **col_kwargs, action=acender_lampadas, args=[['Foco'], warm_rgb]))
    # buttons.append(Button("Foco ❌", **col_kwargs, action=apagar_lampadas, args=[['Foco']]))

    """"""
    pygame.init() 
    gameDisplay = pygame.display.set_mode((display_width,display_height))
    pygame.display.set_caption('A Terça Casa') 
    game_intro()
    pygame.quit()
    quit()