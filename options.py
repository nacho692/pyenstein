import collections as col


class Options:

    def __init__(self):
        self._debug: bool = False
        self._screen_w: int = 800
        self._screen_h: int = 600
        self._fov: int = 90
        self._internal_screen_w: int = 320
        self._internal_screen_h: int = 240
        self.suscribers = col.defaultdict(list)

    def suscribe(self, property_name: str, observer):
        self.suscribers[property_name].append(observer)

    def notify(self, property_name: str, value):
        for observer in self.suscribers[property_name]:
            observer(value)

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value: bool):
        self._debug = value
        self.notify("debug", value)

    @property
    def test(self):
        return self._test

    @test.setter
    def test(self, value: bool):
        self._test = value

    @property
    def screen_w(self):
        return self._screen_w

    @screen_w.setter
    def screen_w(self, value: int):
        self._screen_w = value
        self.notify("screen_w", value)

    @property
    def screen_h(self):
        return self._screen_h

    @screen_h.setter
    def screen_h(self, value: int):
        self._screen_h = value
        self.notify("screen_h", value)

    @property
    def fov(self):
        return self._fov

    @fov.setter
    def set_fov(self, value: int):
        self._fov = value
        self.notify("fov", value)

    @property
    def internal_screen_w(self):
        return self._internal_screen_w

    @internal_screen_w.setter
    def internal_screen_w(self, value: int):
        self._internal_screen_w = value
        self.notify("internal_screen_w", value)

    @property
    def internal_screen_h(self):
        return self._internal_screen_h

    @internal_screen_h.setter
    def internal_screen_h(self, value: int):
        self._internal_screen_h = value
        self.notify("internal_screen_h", value)
