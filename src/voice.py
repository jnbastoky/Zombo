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
        self._cmd_callbacks = {}
        self._all_callback = None
        print("Available Commands:", self.commands)
        super().__init__(i2c, address)

    # def getCommandString:
    #     pass

    def set_cmd_callback(self, command, callback, is_async=False):
        self._cmd_callbacks[command] = (callback, is_async)

    def set_all_callback(self, callback, is_async=False):
        self._all_callback = (callback, is_async)
 
    async def task(self):
        while True:
            cmd = self.get_CMDID()

            # callback for all commands
            if self._all_callback:
                callback, is_async = self._all_callback
                if is_async:
                    await callback(cmd)
                else:
                    callback(cmd)

            # callback for current command
            callback, is_async = self._cmd_callbacks.get(cmd)
            if callback:
                if is_async:
                    await callback(cmd)
                else:
                    callback(cmd)

            await asyncio.sleep(0.01)
