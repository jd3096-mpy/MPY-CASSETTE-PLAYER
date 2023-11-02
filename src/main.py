import gc
gc.enable()
import uasyncio as asyncio
from lib.cassette import CASSETTE

tape=CASSETTE()

asyncio.run(tape.main())