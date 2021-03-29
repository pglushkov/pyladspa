import sys
import os

_extensions = {
    "linux" : [".so"],
    "win32" : [".dll"],
    "darwin" : [".dylib", ".so", "bundle"]
}


def find_dynamic_libs_in_dir(dirpath):
    extensions_list = _extensions.get(sys.platform, [".so"])
    res = [
        os.path.join(dirpath, e) for e in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath,e)) and os.path.splitext(e)[1] in extensions_list
    ]
    return res
