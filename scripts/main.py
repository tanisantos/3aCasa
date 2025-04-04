import pygame
import random
import time
import random
from multiprocessing import Process
import pyautogui
from pywizlight import wizlight, PilotBuilder
import asyncio

from find_lights import find_lights
from button import Button, text_objects
from light_functions import poder


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

light_ip = "192.168.1.89" #dev
light_ip = "192.168.1.182" #dev2
light_ip = "192.168.1.4" #prod

light_ips = {
    "cozinha": '192.168.1.89',
    "sala"   : '192.168.1.154',
    "lustre" : '192.168.1.182',
}

lampadas_nomes = ("Cozinha", "Sala", "Lustre")

lampada_busy = False

light = wizlight(light_ip)
lampada_process = None

buttons = []

random.seed(42)


def display_base():
    gameDisplay.fill(rosa_claro)
    largetext_size = display_width // 8
    largeText = pygame.font.SysFont("portugalbolditalic", largetext_size)
    TextSurf, TextRect = text_objects("A Terça Casa", largeText, rosa_escuro)
    TextRect.center = ((display_width/2), (display_height/2) - display_width // 6)
    gameDisplay.blit(TextSurf, TextRect)


def quitgame():
    pygame.quit()
    quit()

# def intro_loop():

#     display_base()

#     mediumtext = pygame.font.SysFont("portugalbolditalic", display_width // 20)
#     TextSurf2, TextRect2 = text_objects("À procura das lâmpadas...", mediumtext, rosa_escuro)
#     TextRect2.center = ((display_width/2), (display_height/2))

#     gameDisplay.blit(TextSurf2, TextRect2)

#     pygame.display.update()

#     lights = find_lights
    
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 quit()
                
#         display_base()

#         for i in range(len(lampadas_nomes)):
            
#             column_id = f"luz{i}"
#             x_coord = page_horizontal_margin
#             col_kwargs = {"w":button_width, "h": button_height, "x": x_coord, "column_name": column_id, "buttons_y_start": buttons_y_start, 
#                           "height_step": height_step, "ic": rosa_escuro, "ac": black, "text_color": white, "text_size": display_width // 33, "game_display": gameDisplay}
#             # buttons.append(Button(lampadas_nomes[i], **col_kwargs, action=piscar_lampada, args=[lights[i]]))




def main_loop():
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


if __name__ == '__main__':

    pygame.init() 
    gameDisplay = pygame.display.set_mode((display_width,display_height))

    luz_cozinha = wizlight(light_ips['cozinha'])

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
    # buttons.append(Button("🔊⏹", **col_kwargs, action=sound_stop))
    # buttons.append(Button("🔊▼", **col_kwargs, action=sound_fade_out))
    # buttons.append(Button("💡✅", **col_kwargs, action=acender_lampada))
    # buttons.append(Button("💡❌", **col_kwargs, action=apagar_lampada))
    # buttons.append(Button("⏹", **col_kwargs, action=parar_terramoto))

    """ action buttons """
    column_id = "Cozinha"
    x_coord += button_margin + basic_controls_width
    col_kwargs = {"w":button_width, "h": button_height, "x": x_coord, "column_name": column_id, 
                  "buttons_y_start": buttons_y_start, "height_step": height_step, "ic": rosa_escuro, "ac": black, "text_color": white}
    # buttons.append(Button("Mutantes", **col_kwargs, action=mutantes))
    # buttons.append(Button("Musica1", **col_kwargs, action=mutantes))
    # buttons.append(Button("Musica2", **col_kwargs, action=mutantes))
    # buttons.append(Button("Musica3", **col_kwargs, action=mutantes))
    # buttons.append(Button("Esfrega esfrega", **col_kwargs, action=esfrega))

    """"""
    column_id = "luzes"
    x_coord += button_margin + button_width
    col_kwargs = {"w":button_width, "h": button_height, "x": x_coord, "column_name": column_id, "buttons_y_start": buttons_y_start, "height_step": height_step, 
                  "ic": rosa_escuro, "ac": black, "text_color": white, "text_size": display_width // 33, "game_display": gameDisplay, "args": [luz_cozinha]}
    buttons.append(Button("Luz tensão", **col_kwargs, action=poder))
    # buttons.append(Button("Luz fade in", **col_kwargs, action=call_acender_lampada_fade_in_with_subprocess))
    # buttons.append(Button("Luz fraca", **col_kwargs, action=pressentimento))
    # buttons.append(Button("Party?", **col_kwargs, action=party))
    
    """"""
    column_id = "outros"
    x_coord += button_margin + button_width
    col_kwargs = {"w":button_width, "h": button_height, "x": x_coord, "column_name": column_id, 
                  "buttons_y_start": buttons_y_start, "height_step": height_step, "ic": rosa_escuro, "ac": black, "text_color": white}
    # buttons.append(Button("PODER!", **col_kwargs, action=poder))
    # buttons.append(Button("TERRAMOTO!!!", **col_kwargs, action=terramoto))
    # buttons.append(Button("Explosão", **col_kwargs, action=explosao)) # pode-se remover?
    # buttons.append(Button("Parar terramoto", **col_kwargs, action=parar_terramoto))


    pygame.display.set_caption('A Terça Casa') 
    main_loop()
    pygame.quit()
    quit()

