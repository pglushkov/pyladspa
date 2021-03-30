import traceback
import ctypes

from pyladspa.utils import filesystem as fs
from pyladspa.ladspa import dtypes

def find_plugins_in_path(path):
    res = {}
    dynamic_libs = fs.find_dynamic_libs_in_dir(path)
    for dl in dynamic_libs:
        res[dl] = find_plugins_in_lib(dl)
    return res

def find_plugins_in_lib(lib):
    try:
        ladspa_lib = ctypes.CDLL(lib)
        get_plugin_func = dtypes.ladspa_descriptor(ladspa_lib)
        ladspa_dtors = []
        idx = 0
        while True:
            d = get_plugin_func(idx)
            if d:
                d_copy = dtypes.LADSPA_Descriptor()
                ctypes.pointer(d_copy)[0] = d[0]
                ladspa_dtors.append(d_copy)
                idx += 1
            else:
                break

        return ladspa_dtors
    except:
        print("=== ERROR occured while working with library {}".format(lib))
        print("  Exception details and backtrace:\n{}".format(traceback.format_exc()))
        return None

    