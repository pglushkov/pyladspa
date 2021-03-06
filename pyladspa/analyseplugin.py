import traceback
import argparse
import numpy
import sys
import os

from ctypes import *

if __name__ == "__main__":
    from ladspa.dtypes import LADSPA_Descriptor, LADSPA_PortRangeHint, LadspaConsts
    from ladspa.routines import calc_default_port_value
    from utils.common import find_plugins_in_lib
else:
    from pyladspa.ladspa.dtypes import LADSPA_Descriptor, LADSPA_PortRangeHint, LadspaConsts
    from pyladspa.ladspa.routines import calc_default_port_value
    from pyladspa.utils.common import find_plugins_in_lib


def setup_cli(arg_parser):
    arg_parser.add_argument("lib", metavar="LADSPA_LIBRARY", help="Path to LADSPA library in which to search for plugin.")
    arg_parser.add_argument("plug", metavar="PLUGIN_LABEL", help="Label (string id) of the plugin to analyse.")
    arg_parser.add_argument("--classic_fmt", "-f", required=False, default=False, action="store_true", help="Set this flag to enable 'classic' output formatting as in LADSPA SDK tools.")
    return arg_parser


def print_port_description(port_descr, port_name, port_range_hints):

    """
    This abomination is slightly improved version of the code that you can actually find
    in LADSPA SDK. Did not have time to make a proper re-factoring, sorry :(
    """

    def port_type_str(port_descr):
        res = ""
        if LadspaConsts.is_port_input(port_descr) and LadspaConsts.is_port_output(port_descr):
            res += "ERROR: INPUT AND OUTPUT, "
        elif LadspaConsts.is_port_input(port_descr):
            res += "input, "
        elif LadspaConsts.is_port_output(port_descr):
            res += "output, "
        else:
            res += "ERROR: NEITHER INPUT NOR OUTPUT, "

        if LadspaConsts.is_port_audio(port_descr) and LadspaConsts.is_port_control(port_descr):
            res += "ERROR: CONTROL AND AUDIO"
        elif LadspaConsts.is_port_audio(port_descr):
            res += "audio"
        elif LadspaConsts.is_port_control(port_descr):
            res += "control"
        else:
            res += "ERROR: NEITHER CONTROL NOR AUDIO"
        return res

    def range_hint_str(hint):
        props = hint.HintDescriptor
        lbnd = hint.LowerBound
        ubnd = hint.UpperBound
        res = ""

        # step 1 : deal with boundaries
        if LadspaConsts.is_hint_bounded_above(props) or LadspaConsts.is_hint_bounded_bellow(props):
            res += ", "
            if LadspaConsts.is_hint_bounded_bellow(props):
                res += "{}*srate".format(lbnd) if LadspaConsts.is_hint_samplerate(props) else "{}".format(lbnd)
            else:
                res += "..."
            res += " to "
            if LadspaConsts.is_hint_bounded_above(props):
                res += "{}*srate".format(ubnd) if LadspaConsts.is_hint_samplerate(props) else "{}".format(ubnd)
            else:
                res += "..."
        
        # step 2 : toggled
        if LadspaConsts.is_hint_toggled(props):
            if LadspaConsts.is_hint_properly_toggled(props):
                res += ", toggled"
            else:
                res += ", ERROR: TOGGLED INCOMPATIBLE WITH OTHER HINT"

        # step 3 : default values ...
        if LadspaConsts.hint_has_default(props):
            if (LadspaConsts.is_hint_default_min(props) or 
                LadspaConsts.is_hint_default_low(props) or
                LadspaConsts.is_hint_default_middle(props) or
                LadspaConsts.is_hint_default_high(props) or
                LadspaConsts.is_hint_default_max(props)
            ):
                d = calc_default_port_value(hint)
                if LadspaConsts.is_hint_samplerate(props) and d != 0:
                    res += ", default {}*srate".format(d)
                else:
                    res += ", default {}".format(d)
            elif LadspaConsts.is_hint_default_0(props):
                res += ", default 0"
            elif LadspaConsts.is_hint_default_1(props):
                res += ", default 1"
            elif LadspaConsts.is_hint_default_100(props):
                res += ", default 100"
            elif LadspaConsts.is_hint_default_440(props):
                res += ", default 440"
            else:
                res += ", UNKNOWN DEFAULT CODE"

        # step 4 : leftovers ...
        if LadspaConsts.is_hint_logarithmic(props):
            res += ", logarithmic"
        if LadspaConsts.is_hint_integer(props):
            res += ", integer"

        return res

    print("\t\"{}\", {}{}".format(port_name.decode("utf-8"), port_type_str(port_descr), range_hint_str(port_range_hints)))


def print_plugin_contents(plugin, classif_fmt=False):
    if classif_fmt:
        print("\nPlugin Name: {}".format(plugin.Name.decode("utf-8")))
        print("Plugin Label: {}".format(plugin.Label.decode("utf-8")))
        print("Plugin Unique ID: {}".format(plugin.UniqueID))
        print("Maker: {}".format(plugin.Maker.decode("utf-8")))
        print("Copyright: {}".format(plugin.Copyright.decode("utf-8")))
        print("Must Run Real-Time: {}".format("Yes" if LadspaConsts.is_realtime(plugin.Properties) else "No"))
        print("Has activate() Function: {}".format("Yes" if plugin.activate else "No"))
        print("Has deactivate() Function: {}".format("Yes" if plugin.deactivate else "No"))
        print("Has run_adding() Function: {}".format("Yes" if plugin.run_adding else "No"))

        if not plugin.instantiate:
	        print("ERROR: PLUGIN HAS NO INSTANTIATE FUNCTION.")
        if not plugin.connect_port:
	        print("ERROR: PLUGIN HAS NO CONNECT_PORT FUNCTION.")
        if not plugin.run:
	        print("ERROR: PLUGIN HAS NO RUN FUNCTION.")
        if plugin.run_adding and not plugin.set_run_adding_gain:
	        print("ERROR: PLUGIN HAS RUN_ADDING FUNCTION BUT NOT SET_RUN_ADDING_GAIN.")
        if not plugin.run_adding and plugin.set_run_adding_gain:
	        print("ERROR: PLUGIN HAS SET_RUN_ADDING_GAIN FUNCTION BUT NOT RUN_ADDING.")
        if not plugin.cleanup:
	        print("ERROR: PLUGIN HAS NO CLEANUP FUNCTION.")

        print("Environment: {}".format("Normal or Hard Real-Time" if LadspaConsts.is_hard_rt_capable(plugin.Properties) else "Normal"))
        if LadspaConsts.is_inplace_broken(plugin.Properties):
            print("This plugin cannot use in-place processing. It will not work with all hosts.")

        print("Ports:")
        if not plugin.PortCount:
            print("\tERROR: PLUGIN HAS NO PORTS.")
        pdescrs = pointer(cast(plugin.PortDescriptors, POINTER(c_int)))

        pnames = pointer(cast(plugin.PortNames, POINTER(c_char_p)))

        prange_hints = pointer(plugin.PortRangeHints)
        # prange_hints = plugin.PortRangeHints

        for idx in range(plugin.PortCount):
            print_port_description(pdescrs[0][idx], pnames[0][idx], prange_hints[0][idx])

    else:
        print("{}".format(plugin.Name.decode("utf-8")))


def main_cli(input_args = None):
    arg_parser = argparse.ArgumentParser("Print properties of specified LADSPA plugin in specified LADSPA library")
    setup_cli(arg_parser)
    args = arg_parser.parse_args(input_args) # when called with 'None' will go through sys.args

    assert os.path.exists(args.lib) and os.path.isfile(args.lib), "ERROR: cannot locate specified LADSPA library {}".format(args.lib)
    plugs = find_plugins_in_lib(args.lib)
    the_one = [p for p in filter(lambda x: x.Label.decode("utf-8") == args.plug, plugs)]
    assert len(the_one), "ERROR: could not find plugin with label {} in specified LADSPA library!".format(args.plug)
    assert len(the_one) == 1, "ERROR: found several plugins with label {}, non-standard compliant LADSPA library!".format(args.plug)
    print_plugin_contents(the_one[0], classif_fmt=args.classic_fmt)


if __name__ == "__main__":
    main_cli()