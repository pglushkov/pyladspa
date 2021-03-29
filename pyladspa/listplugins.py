import traceback
import argparse
import ctypes
import sys
import os

if __name__ == "__main__":
    from .ladspa.dtypes import LADSPA_Descriptor, LADSPA_PortRangeHint, ladspa_descriptor, LadspaConsts
    from .utils import filesystem as fs
else:
    from pyladspa.ladspa.dtypes import LADSPA_Descriptor, LADSPA_PortRangeHint, ladspa_descriptor, LadspaConsts
    from pyladspa.utils import filesystem as fs

DEFAULT_LADSPA_ENV_VAR = "LADSPA_PATH"
DEFAULT_LADSPA_PATH = "/usr/lib/ladspa/" # should be OS-dependent, but in LADSPA SDK it is hardcoded


def setup_cli(arg_parser):
    arg_parser.add_argument("--path", "-p", required=False, default=None, help="Path to directory in which to search for libraries with LADSPA plugins.")
    arg_parser.add_argument("--lib", "-l", required=False, default=None, help="Path to indiviual library in which to list LADSPA plugins.")
    arg_parser.add_argument("--classic_fmt", "-f", required=False, default=False, action="store_true", help="Set this flag to enable 'classic' output formatting as in LADSPA SDK tools.")
    return arg_parser


def list_plugins_in_path(path, classic_fmt=False):

    dynamic_libs = fs.find_dynamic_libs_in_dir(path)
    for dl in dynamic_libs:
        list_plugins_in_lib(dl, classic_fmt=classic_fmt)
        if not classic_fmt:
            print("")


def list_plugins_in_lib(lib, classic_fmt=False):
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
        if classic_fmt:
            print(os.path.abspath(lib))
        else:
            print("\n=== Plugins found in {}:".format(os.path.abspath(lib)))

        for plug_idx, d in enumerate(ladspa_dtors):
            if classic_fmt:
                print("        {} ({}/{})".format(
                    d.contents.Name.decode("utf-8"),
                    d.contents.Label.decode("utf-8"),
                    d.contents.UniqueID
                ))
            else:
                print("    (ID={:8d}) {:20s} : {}\n                  realtime={}, inplace_broken={}, hard_rt_capable={}".format(
                    d.contents.UniqueID,
                    d.contents.Label.decode("utf-8"), 
                    d.contents.Name.decode("utf-8"),
                    LadspaConsts.is_realtime(d.contents.Properties),
                    LadspaConsts.is_inplace_broken(d.contents.Properties),
                    LadspaConsts.is_hard_rt_capable(d.contents.Properties)
                ))

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
        list_plugins_in_path(args.path, classic_fmt=args.classic_fmt)
    elif args.lib:
        assert os.path.exists(args.lib) and os.path.isfile(args.lib), "ERROR: specified input library {} is either non-existent or its not a file!".format(args.lib)
        list_plugins_in_lib(args.lib, classic_fmt=args.classic_fmt)
    else:
        # Check if LADSPA_PATH is set and search there. If not - last resort is the default path.
        ladspa_path = os.getenv(DEFAULT_LADSPA_ENV_VAR)
        if ladspa_path:
            assert os.path.exists(ladspa_path) and os.path.isdir(ladspa_path), "ERROR: dir {} specfieid as LADSPA_PATH does not exist!".format(ladspa_path)
            list_plugins_in_path(ladspa_path, classic_fmt=args.classic_fmt)
        else:
            assert os.path.exists(DEFAULT_LADSPA_PATH) and os.path.isdir(DEFAULT_LADSPA_PATH), "ERROR: default LADSPA search dir {} does not exist!".format(DEFAULT_LADSPA_PATH)
            list_plugins_in_path(DEFAULT_LADSPA_PATH, classic_fmt=args.classic_fmt)


if __name__ == "__main__":
    main_cli()