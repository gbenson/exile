from PIL import Image
from py65.devices.mpu6502 import MPU as NMOS6502


class Machine:
    def __init__(self):
        self._mpu = NMOS6502()
        with open("resources/2-stopped-at-0x1715.ram", "rb") as fp:
            self._mpu.memory[:] = fp.read()

    @property
    def _square(self):
        return self._mpu.memory[0x95], self._mpu.memory[0x97]

    @_square.setter
    def _square(self, xy):
        self._mpu.memory[0x95], self._mpu.memory[0x97] = xy

    def background_for(self, xy, bad_pc=0xdead):
        self._square = xy
        start_pc = self._mpu.pc
        self._mpu.stPushWord(self._mpu.pc - 1)
        self._mpu.pc = 0x1715
        while self._mpu.pc != start_pc:
            state = self._mpu.step()
        return state.a


def main():
    m = Machine()
    img = Image.new("L", (256, 256))
    for y in range(img.height):
        for x in range(img.width):
            xy = x, y
            img.putpixel(xy, m.background_for(xy))
    img.save("out.png")
    img.show()


if __name__ == "__main__":
    main()
