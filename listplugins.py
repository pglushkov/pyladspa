import traceback
import argparse
import ctypes
import sys
import os

from ladspa.dtypes import LADSPA_Descriptor, LADSPA_PortRangeHint, ladspa_descriptor, LadspaConsts

DEFAULT_LADSPA_ENV_VAR = "LADSPA_PATH"
DEFAULT_LADSPA_PATH = "/usr/lib/ladspa/" # should be OS-dependent, but in LADSPA SDK it is hardcoded


def setup_cli(arg_parser):
    arg_parser.add_argument("--path", "-p", required=False, default=None, help="Path to directory in which to search for libraries with LADSPA plugins")
    arg_parser.add_argument("--lib", "-l", required=False, default=None, help="Path to indiviual library in which to list LADSPA plugins")
    return arg_parser


def list_plugins_in_path(path):
    return None


def list_plugins_in_lib(lib):
    # Get a handle to the sytem C library
    try:
        ladspa_lib = ctypes.CDLL(lib)
        get_plugin = ladspa_descriptor(ladspa_lib)
        ladspa_dtors = []
        idx = 0
        while True:
            d = get_plugin(idx)
            if d:
                ladspa_dtors.append(d)
                idx += 1
            else:
                break
        
        print("=== Plugins found:")
        for plug_idx, d in enumerate(ladspa_dtors):
            print("  {} : {}, is_realtime={}".format(plug_idx, d.contents.Label, LadspaConsts.is_realtime(d.contents.Properties)))
    except:
        print("=== ERROR occured while working with library {}".format(lib))
        print("  Exception details and back-trace:\n{}".format(traceback.format_exc()))

    return None


def main_cli(input_args = None):
    arg_parser = argparse.ArgumentParser()
    setup_cli(arg_parser)
    args = arg_parser.parse_args(input_args) # when called with 'None' will go through sys.args

    if args.path:
        assert os.path.exists(args.path) and os.path.isdir(args.path), "ERROR: specified input path {} is either non-existent or not a directory!".format(args.path)
        list_plugins_in_path(args.path)
    elif args.lib:
        assert os.path.exists(args.lib) and os.path.isfile(args.lib), "ERROR: specified input library {} is either non-existent or its not a file!".format(args.lib)
        list_plugins_in_lib(args.lib)
    else:
        # Check if LADSPA_PATH is set and search there. If not - last resort is the default path.
        ladspa_path = os.getenv(DEFAULT_LADSPA_ENV_VAR)
        if ladspa_path:
            list_plugins_in_path(ladspa_path)
        else:
            list_plugins_in_path(DEFAULT_LADSPA_PATH)


if __name__ == "__main__":
    main_cli()