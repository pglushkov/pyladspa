import ctypes

from . import dtypes

def ladspa_descriptor(ladspa_lib):
    res = ladspa_lib.ladspa_descriptor
    res.argtypes = [ctypes.c_ulong]
    res.restype = ctypes.POINTER(dtypes.LADSPA_Descriptor)
    return res