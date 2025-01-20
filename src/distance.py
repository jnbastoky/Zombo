import asyncio

from adafruit_bus_device.i2c_device import I2CDevice


class Distance:
    def __init__(self, address, i2c):
        self._bus = i2c
        self._address = address
        # Device does not response to probes
        self._device = I2CDevice(i2c, address, probe=False)
        self._callbacks = []
        self.value = 0.0
        i2c.try_lock()
        # time.sleep(10)
        i2c.probe(address)  # Only works if this is present
        i2c.unlock()
        # This is similar to probe but seems to actually wake the device up
        # with self._device as dev:
        #     dev.write(bytes([0x00]))

    def set_callback(self, callback, is_async=False):
        self._callbacks.append((callback, is_async))

    async def read(self):
        '''
        returns micrometers
        https://www.adafruit.com/product/4742#tab-description-heading
        # '''
        with self._device as device:
            # device.write(bytearray([1]))
            device.write(bytes([0x01]))
        # This sleep can't be too short or the read will produce an exception
        await asyncio.sleep(0.5)
        response = bytearray(3)
        with self._device as device:
            device.readinto(response)
        
        return int.from_bytes(response, 'big') / 1000

    async def task(self):
        while True:
            self.value = await self.read()
            # print(self._callbacks)
            if len(self._callbacks):
                for callback, is_async in self._callbacks:
                    # print(f'calling {callback}')
                    if is_async:
                        # print('coroutine')
                        await callback(self.value)
                    else:
                        callback(self.value)
