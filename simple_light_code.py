import asyncio
import time
import random
import sys

from pywizlight import wizlight, PilotBuilder, discovery

async def main():
    """Sample code to work with bulbs."""

    args = sys.argv[1:]
    # Set up a standard light
    light = wizlight("192.168.1.4")


    for i in range(int(args[0])):
        await light.turn_off()
        time.sleep(random.randint(1, 10) * 0.01)
        await light.turn_on(PilotBuilder(brightness = 255))
        time.sleep(random.randint(1, 10) * 0.01)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())