import traceback
import argparse
import ctypes
import sys
import os

if __name__ == "__main__":
    from ladspa.dtypes import LADSPA_Descriptor, LADSPA_PortRangeHint, LadspaConsts
    from ladspa import DEFAULT_LADSPA_ENV_VAR, DEFAULT_LADSPA_PATH
    from utils.common import find_plugins_in_lib, find_plugins_in_path
else:
    from pyladspa.ladspa.dtypes import LADSPA_Descriptor, LADSPA_PortRangeHint, LadspaConsts
    from pyladspa.ladspa import DEFAULT_LADSPA_ENV_VAR, DEFAULT_LADSPA_PATH
    from pyladspa.utils.common import find_plugins_in_lib, find_plugins_in_path


def setup_cli(arg_parser):
    arg_parser.add_argument("--path", "-p", required=False, default=None, help="Path to directory in which to search for libraries with LADSPA plugins.")
    arg_parser.add_argument("--lib", "-l", required=False, default=None, help="Path to indiviual library in which to list LADSPA plugins.")
    arg_parser.add_argument("--classic_fmt", "-f", required=False, default=False, action="store_true", help="Set this flag to enable 'classic' output formatting as in LADSPA SDK tools.")
    return arg_parser


def print_found_plugins(plugins_dict, classic_fmt=False):
    for lib, plug_list in plugins_dict.items():
        if classic_fmt:
            print(os.path.abspath(lib))
        else:
            print("\n=== Plugins found in {}:".format(os.path.abspath(lib)))
        
        if not plug_list:
            print("    Parsing plugins in this library ended with error!")
            continue

        for plug in plug_list:
            if classic_fmt:
                print("        {} ({}/{})".format(
                    plug.Name.decode("utf-8"),
                    plug.Label.decode("utf-8"),
                    plug.UniqueID
                ))
            else:
                print("    (ID={:8d}) {:20s} : {}\n                  realtime={}, inplace_broken={}, hard_rt_capable={}".format(
                    plug.UniqueID,
                    plug.Label.decode("utf-8"), 
                    plug.Name.decode("utf-8"),
                    LadspaConsts.is_realtime(plug.Properties),
                    LadspaConsts.is_inplace_broken(plug.Properties),
                    LadspaConsts.is_hard_rt_capable(plug.Properties)
                ))


def main_cli(input_args = None):
    arg_parser = argparse.ArgumentParser("List all LADSPA plugins found is specified directory or library.")
    setup_cli(arg_parser)
    args = arg_parser.parse_args(input_args) # when called with 'None' will go through sys.args

    if args.path:
        assert os.path.exists(args.path) and os.path.isdir(args.path), "ERROR: specified input path {} is either non-existent or not a directory!".format(args.path)
        # list_plugins_in_path(args.path, classic_fmt=args.classic_fmt)
        plugs_dict = find_plugins_in_path(args.path)
    elif args.lib:
        assert os.path.exists(args.lib) and os.path.isfile(args.lib), "ERROR: specified input library {} is either non-existent or its not a file!".format(args.lib)
        # list_plugins_in_lib(args.lib, classic_fmt=args.classic_fmt)
        plugs_dict = { args.lib : find_plugins_in_lib(args.lib) }
    else:
        # Check if LADSPA_PATH is set and search there. If not - last resort is the default path.
        ladspa_path = os.getenv(DEFAULT_LADSPA_ENV_VAR)
        if ladspa_path:
            assert os.path.exists(ladspa_path) and os.path.isdir(ladspa_path), "ERROR: dir {} specfieid as LADSPA_PATH does not exist!".format(ladspa_path)
            # list_plugins_in_path(ladspa_path, classic_fmt=args.classic_fmt)
            plugs_dict = find_plugins_in_path(ladspa_path)
        else:
            assert os.path.exists(DEFAULT_LADSPA_PATH) and os.path.isdir(DEFAULT_LADSPA_PATH), "ERROR: default LADSPA search dir {} does not exist!".format(DEFAULT_LADSPA_PATH)
            # list_plugins_in_path(DEFAULT_LADSPA_PATH, classic_fmt=args.classic_fmt)
            plugs_dict = find_plugins_in_path(DEFAULT_LADSPA_PATH)

    print_found_plugins(plugs_dict, classic_fmt=args.classic_fmt)

if __name__ == "__main__":
    main_cli()