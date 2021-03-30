import ctypes
import numpy

from . import dtypes

def ladspa_descriptor(ladspa_lib):
    res = ladspa_lib.ladspa_descriptor
    res.argtypes = [ctypes.c_ulong]
    res.restype = ctypes.POINTER(dtypes.LADSPA_Descriptor)
    return res


def calc_default_port_value(hint):
    props = hint.HintDescriptor
    lbnd = hint.LowerBound
    ubnd = hint.UpperBound
    d = 0
    if dtypes.LadspaConsts.is_hint_default_min(props):
        d = lbnd
    elif dtypes.LadspaConsts.is_hint_default_low(props):
        if dtypes.LadspaConsts.is_hint_logarithmic(props):
            d = numpy.exp(numpy.log(lbnd)*0.75 + numpy.log(ubnd)*0.25)
        else: 
            d = (lbnd*0.75 + ubnd*0.25)
    elif dtypes.LadspaConsts.is_hint_default_middle(props):
        if dtypes.LadspaConsts.is_hint_logarithmic(props):
            d = numpy.sqrt(lbnd * ubnd)
        else:
            d = 0.5*(lbnd + ubnd)
    elif dtypes.LadspaConsts.is_hint_default_high(props):
        if dtypes.LadspaConsts.is_hint_logarithmic(props):
            d = numpy.exp(numpy.log(lbnd)*0.25 + numpy.log(ubnd)*0.75)
        else: 
            d = (lbnd*0.25 + ubnd*0.75)
    elif dtypes.LadspaConsts.is_hint_default_max(props):
        d = ubnd
    elif dtypes.LadspaConsts.is_hint_default_0(props):
        d = 0.0
    elif dtypes.LadspaConsts.is_hint_default_1(props):
        d = 1.0
    elif dtypes.LadspaConsts.is_hint_default_100(props):
        d = 100.0
    elif dtypes.LadspaConsts.is_hint_default_440(props):
        d = 440.0

    return d