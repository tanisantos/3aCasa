import pygame
import time
import random
import asyncio
import time
import random
from multiprocessing import Process
import pyautogui
from pywizlight import wizlight, PilotBuilder
import asyncio


def parar_lampada_process(lampada_process):
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

def call_piscar_lampada_with_subprocess(light, n_flickers=10):
    # if lampada_busy:
        # parar_lampada_process(lampada_process)
    lampada_process = Process(target=piscar_lampada, args=[light, n_flickers])
    lampada_process.start()

def poder(light):
    call_piscar_lampada_with_subprocess(light, n_flickers=3)