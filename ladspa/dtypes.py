from ctypes import Structure, c_float, POINTER, c_char_p, c_ulong, c_void_p, c_int


class LadspaConsts:
    LADSPA_PROPERTY_REALTIME = 0x1
    LADSPA_PROPERTY_INPLACE_BROKEN  = 0x2
    LADSPA_PROPERTY_HARD_RT_CAPABLE  = 0x4

    @classmethod
    def is_realtime(cls, inp):
        return inp & cls.LADSPA_PROPERTY_REALTIME

    @classmethod
    def is_inplace_broken(cls, inp)
        return inp & cls.LADSPA_PROPERTY_INPLACE_BROKEN

    @classmethod
    def is_hard_rt_capable(cls, inp)
        return inp & cls.LADSPA_PROPERTY_HARD_RT_CAPABLE

    LADSPA_PORT_INPUT = 0x1
    LADSPA_PORT_OUTPUT = 0x2
    LADSPA_PORT_CONTROL = 0x4
    LADSPA_PORT_AUDIO = 0x8

    @classmethod
    def ... stopped here ...
    

class LADSPA_PortRangeHint(Structure):
    _fields_ = [
        ("HintDescriptor",c_int),
        ("LowerBound", c_float),
        ("UpperBound", c_float)
    ]


class LADSPA_Descriptor(Structure):
    _fields_=[
        ("UniqueID",c_ulong),
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