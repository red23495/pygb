from sdl2 import *
from ctypes import *


class APU:

    sample_rate = 44100
    buffer_size = 512

    def __init__(self):
        self._sound_1 = Sound1()
        self._sound_2 = Sound2()
        self._sound_3 = Sound3()
        self._sound_4 = Sound4()
        self._sound_5 = Sound4()
        self.channel_1_volume = 0
        self.channel_2_volume = 0
        self._reg_nr52 = 0x00
        self._reg_nr51 = 0x00
        self._reg_nr50 = 0x00
        self._reg_nr11 = 0x00
        self._reg_nr12 = 0x00
        self._init_sdl()

    def _init_sdl(self):
        if SDL_Init(SDL_INIT_AUDIO) < 0:
            print('Audio initialization failed')
        channels = 2
        callback = SDL_AudioCallback(lambda userdata, buffer, length: self._sdl_callback(userdata, buffer, length))
        self.want_audio_spec = SDL_AudioSpec(self.sample_rate, AUDIO_S8, channels, self.buffer_size, callback=callback)
        self.have_audio_spec = SDL_AudioSpec(0, 0, 0, 0)
        self.audio_device = SDL_OpenAudioDevice(None, 0, self.want_audio_spec, self.have_audio_spec, 0)
        SDL_PauseAudioDevice(self.audio_device, 0)

    def _sdl_callback(self, userdata, buffer, length):
        for i in range(length):
            buffer[i] = 0

    def _close_sdl(self):
        SDL_CloseAudioDevice(self.audio_device)
        SDL_Quit()

    def close(self):
        self._close_sdl()

    # sound on/off controller
    @property
    def nr52(self):
        return self._reg_nr52

    # output channel selection
    @property
    def nr51(self):
        return self._reg_nr51

    # output channel control
    @property
    def nr50(self):
        return self._reg_nr50

    # sound 1 sound length/wave pattern
    @property
    def nr11(self):
        return self._reg_nr11

    # sound 1 volume envelop
    @property
    def nr12(self):
        return self._reg_nr12

    @nr50.setter
    def nr50(self, value):
        self._reg_nr50 = value
        self._sound_5.channel_1_enabled = bool(self._reg_nr50 & 0b10000000)
        self._sound_5.channel_2_enabled = bool(self._reg_nr50 & 0b00001000)
        self.channel_1_volume = self._reg_nr50 & 0b00000111
        self.channel_2_volume = (self._reg_nr50 & 0b01110000) >> 4

    @nr51.setter
    def nr51(self, value):
        self._sound_1.channel_1_enabled = bool(value & 0b00000001)
        self._sound_2.channel_1_enabled = bool(value & 0b00000010)
        self._sound_3.channel_1_enabled = bool(value & 0b00000100)
        self._sound_4.channel_1_enabled = bool(value & 0b00001000)
        self._sound_1.channel_2_enabled = bool(value & 0b00010000)
        self._sound_2.channel_2_enabled = bool(value & 0b00100000)
        self._sound_3.channel_2_enabled = bool(value & 0b01000000)
        self._sound_4.channel_2_enabled = bool(value & 0b10000000)
        self._reg_nr51 = value

    @nr52.setter
    def nr52(self, value):
        is_sound_enabled = (value & 0b10000000) >> 7
        val = 0b10001111 if is_sound_enabled else 0b00000000
        self._sound_1.enabled = is_sound_enabled
        self._sound_2.enabled = is_sound_enabled
        self._sound_3.enabled = is_sound_enabled
        self._sound_4.enabled = is_sound_enabled
        self._reg_nr52 = val

    @nr11.setter
    def nr11(self, value):
        self._reg_nr11 = value
        self._sound_1.sound_length = self._reg_nr11 & 0b00111111
        self._sound_1.wave_pattern = self._reg_nr11 >> 6

    @nr12.setter
    def nr12(self, value):
        self._reg_nr12 = value
        self._sound_1.envelop_sweep = self._reg_nr12 & 0b00000111
        self._sound_1.envelop_direction = (self._reg_nr12 & 0b00001000) >> 3
        self._sound_1.envelop_volume = self._reg_nr12 >> 4


class Sound:

    wave_patterns = {
        0b00: 0b00000001,
        0b01: 0b10000001,
        0b10: 0b10000111,
        0b11: 0b01111110,
    }

    def __init__(self):
        self.enabled = 0
        self.channel_1_enabled = False
        self.channel_2_enabled = False


class Sound1(Sound):

    def __init__(self):
        super().__init__()
        self.envelop_sweep = 0
        self.envelop_direction = 0
        self.envelop_volume = 0
        self.sound_length = 0
        self.wave_pattern = 0


class Sound2(Sound):

    def __init__(self):
        super().__init__()


class Sound3(Sound):

    def __init__(self):
        super().__init__()


class Sound4(Sound):

    def __init__(self):
        super().__init__()


class Sound5(Sound):

    def __init__(self):
        super().__init__()
