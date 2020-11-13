"""
Write namelists
"""

from typing import Union, Any
from io import TextIOWrapper

###############################################################################
def _traverse_value(f: TextIOWrapper, path: str, sep: str, path2: str, d: Any):

    if path.strip() != '':
        path2 = "{}{}{}".format(path, sep, path2)  # f"{path}{sep}{path2}"
    _traverse_dict(f, d, path2)

###############################################################################
def _traverse_dict(f: TextIOWrapper, d: Any, path: str = '', sep: str = '%'):
    """
    traverse a dict and print the paths to each variable in namelist style
    """

    if isinstance(d, dict):
        for k, v in d.items():
            if isinstance(v, list):
                index = 0
                for element in v:
                    index += 1
                    _traverse_value(f, path, sep,  # f'{k}({index})',
                                    '{}({})'.format(k, index),
                                    element)
            else:
                _traverse_value(f, path, sep, k, v)
    elif isinstance(d, list):
        for element in d:
            _traverse_dict(f, element, path)
    else:
        path = path.lower()
        if (d is None):
            pass
        elif isinstance(d, str):
            s = d.replace("'", "''")
            # f.write(f" {path} = '{s}',\n")
            f.write(" {} = '{}',\n".format(path, s))
        elif isinstance(d, bool):
            # f.write(f" {path} = {['F', 'T'][int(d)]},\n")
            f.write(" {} = {},\n".format(path, ['F', 'T'][int(d)]))
        elif isinstance(d, int):
            # f.write(f" {path} = {d},\n")
            f.write(" {} = {},\n".format(path, d))
        elif isinstance(d, float):
            # f.write(f" {path} = {d:.17E},\n")
            f.write(" {} = {:.17E},\n".format(path, d))

###############################################################################
def _print_single_namelist(f: TextIOWrapper, namelist_name: str, d: dict):

    # f.write(f'&{namelist_name.lower()}\n')
    f.write('&{}\n'.format(namelist_name.lower()))
    _traverse_dict(f, d)
    f.write('/\n')
    f.write('\n')

###############################################################################
def write_namelist_to_stream(d: dict, file: TextIOWrapper):

    for k, v in d.items():
        if isinstance(v, list):
            for element in v:
                _print_single_namelist(file, k, element)
        elif isinstance(v, dict):
            _print_single_namelist(file, k, v)

###############################################################################
def save_namelist(d: dict, file: Union[str, TextIOWrapper]):
    """
    Print a dict as a namelist file.
    Assumes an `f90nml` namelist style structure
    (a dict of dicts, some of which can be lists).

    This uses the "simple" format, with one variable per line.
    """

    if isinstance(file, str):
        with open(file, 'w') as file:
            write_namelist_to_stream(d, file)
    else:
        write_namelist_to_stream(d, file)
