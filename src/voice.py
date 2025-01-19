import asyncio

import DFRobot_DF2301Q
from DFRobot_DF2301Q_Commands import CommandWord


class Voice(DFRobot_DF2301Q.DFRobot_DF2301Q_I2C):
    CommandWords = CommandWord
    
    def __init__(self, i2c, address):

        # Inspect instance members
        # print(dir(CommandWord))

        # Inspect instance methods and attributes
        self.commands = {
            getattr(CommandWord, attr): attr
            for attr in dir(CommandWord)
            if not callable(getattr(CommandWord, attr)) and not attr.startswith("__")  # Exclude methods and special attributes
        }
        self.callbacks = {}
        print("Available Commands:", self.commands)
        super().__init__(i2c, address)

    # def getCommandString:
    #     pass

    def set_callback(self, command, callback):
        self.callbacks[command] = callback

    async def task(self):
        while True:
            cmd = self.get_CMDID()
            callback = self.callbacks.get(cmd)
            if callback:
                callback()
            await asyncio.sleep(0.5)
