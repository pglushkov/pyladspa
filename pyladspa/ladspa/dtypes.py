from ctypes import Structure, c_float, POINTER, c_char_p, c_ulong, c_void_p, c_int


class LadspaConsts:
    LADSPA_PROPERTY_REALTIME = 0x1
    LADSPA_PROPERTY_INPLACE_BROKEN  = 0x2
    LADSPA_PROPERTY_HARD_RT_CAPABLE  = 0x4

    @classmethod
    def is_realtime(cls, inp):
        return bool(inp & cls.LADSPA_PROPERTY_REALTIME)

    @classmethod
    def is_inplace_broken(cls, inp):
        return bool(inp & cls.LADSPA_PROPERTY_INPLACE_BROKEN)

    @classmethod
    def is_hard_rt_capable(cls, inp):
        return bool(inp & cls.LADSPA_PROPERTY_HARD_RT_CAPABLE)

    LADSPA_PORT_INPUT = 0x1
    LADSPA_PORT_OUTPUT = 0x2
    LADSPA_PORT_CONTROL = 0x4
    LADSPA_PORT_AUDIO = 0x8

    @classmethod
    def is_port_input(cls, inp):
        return bool(inp & cls.LADSPA_PORT_AUDIO)
    
    @classmethod
    def is_port_output(cls, inp):
        return bool(inp & cls.LADSPA_PORT_OUTPUT)
    
    @classmethod
    def is_port_control(cls, inp):
        return bool(inp & cls.LADSPA_PORT_CONTROL)
    
    @classmethod
    def is_port_audio(cls, inp):
        return bool(inp & cls.LADSPA_PORT_AUDIO)
    
    LADSPA_HINT_BOUNDED_BELOW = 0x1
    LADSPA_HINT_BOUNDED_ABOVE = 0x2
    LADSPA_HINT_TOGGLED = 0x4
    LADSPA_HINT_SAMPLE_RATE = 0x8
    LADSPA_HINT_LOGARITHMIC = 0x10
    LADSPA_HINT_INTEGER = 0x20

    @classmethod
    def is_hint_bounded_bellow(cls, inp):
        return bool(inp & cls.LADSPA_HINT_BOUNDED_BELOW)
    
    @classmethod
    def is_hint_bounded_above(cls, inp):
        return bool(inp & cls.LADSPA_HINT_BOUNDED_ABOVE)

    @classmethod
    def is_hint_toggled(cls, inp):
        return bool(inp & cls.LADSPA_HINT_TOGGLED)

    @classmethod
    def is_hint_samplerate(cls, inp):
        return bool(inp & cls.LADSPA_HINT_SAMPLE_RATE)

    @classmethod
    def is_hint_logarithmic(cls, inp):
        return bool(inp & cls.LADSPA_HINT_LOGARITHMIC)

    @classmethod
    def is_hint_integer(cls, inp):
        return bool(inp & cls.LADSPA_HINT_INTEGER)

    LADSPA_HINT_DEFAULT_MASK = 0x3C0
    LADSPA_HINT_DEFAULT_NONE = 0x0
    LADSPA_HINT_DEFAULT_MINIMUM = 0x40
    LADSPA_HINT_DEFAULT_LOW = 0x80
    LADSPA_HINT_DEFAULT_MIDDLE = 0xC0
    LADSPA_HINT_DEFAULT_HIGH = 0x100
    LADSPA_HINT_DEFAULT_MAXIMUM = 0x140
    LADSPA_HINT_DEFAULT_0 = 0x200
    LADSPA_HINT_DEFAULT_1 = 0x240
    LADSPA_HINT_DEFAULT_100 = 0x280
    LADSPA_HINT_DEFAULT_440 = 0x2C0

    @classmethod
    def hint_has_default(cls, inp):
        return bool(inp & cls.LADSPA_HINT_DEFAULT_MASK)

    @classmethod
    def is_hint_default_min(cls, inp):
        return (inp & cls.LADSPA_HINT_DEFAULT_MASK) == cls.LADSPA_HINT_DEFAULT_MINIMUM

    @classmethod
    def is_hint_default_low(cls, inp):
        return (inp & cls.LADSPA_HINT_DEFAULT_MASK) == cls.LADSPA_HINT_DEFAULT_LOW

    @classmethod
    def is_hint_default_middle(cls, inp):
        return (inp & cls.LADSPA_HINT_DEFAULT_MASK) == cls.LADSPA_HINT_DEFAULT_MIDDLE

    @classmethod
    def is_hint_default_high(cls, inp):
        return (inp & cls.LADSPA_HINT_DEFAULT_MASK) == cls.LADSPA_HINT_DEFAULT_HIGH

    @classmethod
    def is_hint_default_max(cls, inp):
        return (inp & cls.LADSPA_HINT_DEFAULT_MASK) == cls.LADSPA_HINT_DEFAULT_MAXIMUM

    @classmethod
    def is_hint_default_0(cls, inp):
        return (inp & cls.LADSPA_HINT_DEFAULT_MASK) == cls.LADSPA_HINT_DEFAULT_0

    @classmethod
    def is_hint_default_1(cls, inp):
        return (inp & cls.LADSPA_HINT_DEFAULT_MASK) == cls.LADSPA_HINT_DEFAULT_1

    @classmethod
    def is_hint_default_100(cls, inp):
        return (inp & cls.LADSPA_HINT_DEFAULT_MASK) == cls.LADSPA_HINT_DEFAULT_100

    @classmethod
    def is_hint_default_440(cls, inp):
        return (inp & cls.LADSPA_HINT_DEFAULT_MASK) == cls.LADSPA_HINT_DEFAULT_440


class LADSPA_PortRangeHint(Structure):
    _fields_ = [
        ("HintDescriptor",c_int),
        ("LowerBound", c_float),
        ("UpperBound", c_float)
    ]


class LADSPA_Descriptor(Structure):
    _fields_=[
        ("UniqueID",c_ulong), # expected to be bellow 16'777'215 (0x1000000)
        ("Label",c_char_p),
        ("Properties",c_int),
        ("Name", c_char_p),
        ("Maker", c_char_p),
        ("Copyright", c_char_p),
        ("PortCount", c_ulong),
        ("PortDescriptors", c_void_p), # actually an int*
        ("PortNames", c_void_p), # actually a const* char*
        ("PortRangeHints", POINTER(LADSPA_PortRangeHint)),
        ("ImplementationData", c_void_p),
        ("instantiate", c_void_p),
        ("connect_port", c_void_p),
        ("activate", c_void_p),
        ("run", c_void_p),
        ("run_adding", c_void_p),
        ("set_run_adding_gain", c_void_p),
        ("deactivate", c_void_p),
        ("cleanup", c_void_p)
    ]


def ladspa_descriptor(ladspa_lib):
    res = ladspa_lib.ladspa_descriptor
    res.argtypes = [c_ulong]
    res.restype = POINTER(LADSPA_Descriptor)
    return res