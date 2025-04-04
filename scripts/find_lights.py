
import asyncio
from pywizlight import wizlight, PilotBuilder, discovery

async def find_lights_main():
    """Sample code to work with bulbs."""
    # Discover all bulbs in the network via broadcast datagram (UDP)
    # function takes the discovery object and returns a list of wizlight objects.
    bulbs = await discovery.discover_lights(broadcast_space="192.168.1.255")
    # Print the IP address of the bulb on index 0
    print(f"Bulb IP address: {bulbs[0].ip}")

    # Iterate over all returned bulbs
    for bulb in bulbs:
        print(bulb.__dict__)
        # Turn off all available bulbs
        # await bulb.turn_off()

    # Set up a standard light
    light = wizlight(bulbs[0].ip)

    await light.turn_on(PilotBuilder(brightness = 255))

    return [wizlight(bulb.ip) for bulb in bulbs]


def find_lights():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(find_lights_main())


if __name__ == '__main__':
    find_lights()