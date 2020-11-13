"""
Read namelists
"""

from f90nml import Namelist, Parser
import multiprocessing as mp
import re
from typing import List, Union

_nml_types = Union[int, float, bool, str]
_array_rg = re.compile('((?:[a-z][a-z0-9_]*))(\\()(\\d+)(\\))(.*)',
                       re.IGNORECASE | re.DOTALL)

###############################################################################
def _get_array_index(s: str) -> (int, str):
    """
    If the variable name represents an array element (e.g., 'VAR(1)'),
    then return the array index (1-based) and the variable name.
    Otherwise, return None.
    """

    # initial quick check:
    if '(' not in s:
        return None, None

    m = _array_rg.search(s.strip())
    if m:
        if (m.group(5) == ''):
            return int(m.group(3)), m.group(1)  # index, arrayname
        else:
            # invalid array string
            return None, None
    else:
        return None, None

###############################################################################
def _pathSet(dictionary: dict, path: str, value: _nml_types, sep: str = '%'):
    '''
    Sets a variable in a dictionary, given the namelist path string.
    Assumes the input path uses Fortran-style 1-based indexing of arrays
    '''

    path = path.split(sep)
    key = path[-1]
    dictionary = _pathGet(dictionary, sep.join(path[:-1]), sep=sep)
    i, arrayname = _get_array_index(key)
    if (i is not None):
        # it is an array element:
        if (arrayname not in dictionary):
            dictionary[arrayname] = [None]
        x = dictionary[arrayname]
        lenx = len(x)
        if lenx < i:
            # have to add this element
            for j in range(lenx, i):
                x.append(None)
        x[i - 1] = value
    else:
        # it is just a normal variable:
        dictionary[key] = value

###############################################################################
def _pathGet(dictionary: dict, path: str,
             sep: str = '%') -> Union[_nml_types, dict, list]:
    '''
    Returns an item in a dictionary given the namelist path string.
    Assumes the input path uses Fortran-style 1-based indexing of arrays
    '''

    for item in path.split(sep):
        i, arrayname = _get_array_index(item)
        if (i is not None):
            # it is an array element:
            # create this item since it isn't there
            if (arrayname not in dictionary):
                dictionary[arrayname] = [None]
            d = dictionary[arrayname]
            lenx = len(d)
            if lenx < i:
                # have to add this element
                for j in range(lenx, i):
                    d.append(None)

            # make sure it's a dict:
            if (not isinstance(d[i - 1], dict)):
                d[i - 1] = Namelist({})
            dictionary = d[i - 1]
        else:
            # it is just a normal variable:
            # make sure it's a dict first
            if (not isinstance(dictionary, dict)):
                dictionary = Namelist({})
            if (item not in dictionary):
                dictionary[item] = Namelist({})
            dictionary = dictionary[item]

    return dictionary

###############################################################################
def _nml_value_to_python_value(value: str) -> _nml_types:
    """
    Convert the namelist value to a Python value.
    """

    value_str = value.strip()
    value_str_bool = value_str.lower().strip('.')
    if (value_str_bool == 't' or value_str_bool == 'true'):
        # logical
        return True
    elif (value_str_bool == 'f' or value_str_bool == 'false'):
        # logical
        return False
    elif (value_str[0] == '"' and value_str[-1] == '"'):
        # string
        # fortran to python convention
        return value_str[1:-1].replace('""', '"')
    elif (value_str[0] == "'" and value_str[-1] == "'"):
        # string
        # fortran to python convention
        return value_str[1:-1].replace("''", "'")
    else:
        # int or double:
        try:
            return int(value_str)
        except ValueError:
            return float(value_str)

###############################################################################
def _read_single_namelist(lines: List[str], parser: Parser,
                          simple: bool) -> Namelist:
    """
    Read a namelist.

    * Simple parser. Assumes one array element per line.
        For example: `val%a(2)%b = value,`
    * Otherwise (or if the simple parser fails) it defaults
        to using f90nml to read it.

    Note that comment lines and blank lines have already been removed.
    """

    nml = None
    if simple:
        try:

            namelist_name = lines[0].lstrip('&').strip().lower()
            nml = Namelist({namelist_name: Namelist({})})
            for line in lines[1:]:
                d = line.split('=', 1)
                if (len(d) == 1):
                    if d[0].strip()=='/':
                        break # end of the namelist
                    else:
                        raise Exception('invalid line') # something else - not valid
                elif (len(d) >= 2):
                    if d[0][0]=="'" or d[0][0]=='"':
                        raise Exception('invalid line') # = in a string - not valid
                    else:
                        path = d[0].strip()

                        if ':' in path:
                            raise Exception('invalid line') # can't read multiple entries at once - not valid
                        else:
                            # warning: it will still read lines like
                            # this: `a = 1,2,3` as a single string

                            # convert the string to a Python value:
                            value = _nml_value_to_python_value(d[1].rstrip(', '))

                            # add this value to the namelist:
                            _pathSet(nml[namelist_name], path, value)

        except Exception:
            nml = None

    if nml is None:
        nml = parser.reads('\n'.join(lines))  # f90nml 1.1 and above

    return nml

###############################################################################
# def split_namelist_str(s: str):
#     """alternate version of split_namelist_file with a string as an input"""
#     namelists = []
#     i = -1
#     started = False
#     f = s.split('\n')
#     for line in f:
#         line = line.strip()
#         if (len(line) > 0):
#             if (line[0] != '!'):
#                 if (line[0] == '&'):  # start a namelist
#                     i = i + 1
#                     namelists.append([])
#                     started = True
#                 elif (line[0:1] == '/'):  # end a namelist
#                     started = False
#                     namelists[i].append(line)
#                     continue
#                 if started:
#                     namelists[i].append(line)
#     return namelists

###############################################################################
def _split_namelist_file(filename: str) -> List[str]:
    """ split a namelist file into an array of namelist strings """

    namelists = list()
    i = -1
    started = False
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if (len(line) > 0):
                if (line[0] != '!'):
                    if (line[0] == '&'):  # start a namelist
                        i = i + 1
                        namelists.append(list())
                        started = True
                    elif (line[0:1] == '/'):  # end a namelist
                        started = False
                        namelists[i].append(line)
                        continue
                    if started:
                        namelists[i].append(line)

    return namelists

###############################################################################
def read_namelist(filename: str, *, n_threads: int = 0,
                  parser: Parser = None,
                  simple: bool = True) -> Namelist:
    """
    Read a namelist quickly.

    For threaded use, set `n_threads` to the number of threads.
    """

    nml = Namelist({})

    def _loop_over_results(r):
        for key, value in r.items():
            if key in nml:
                # array of namelists:
                if isinstance(nml[key], list):
                    nml[key].append(value)
                else:
                    nml[key] = [nml[key], value]
            else:
                nml[key] = value

    if not parser:
        parser = Parser()

    namelists = _split_namelist_file(filename)
    results = list()
    results_append = results.append

    if n_threads:
        n_threads = max(1, min(mp.cpu_count(), n_threads))
        pool = mp.Pool(processes=n_threads)
        pool_apply_async = pool.apply_async

        for lines in namelists:
            results_append(pool_apply_async(_read_single_namelist,
                                            (lines, parser, simple)))

        pool.close()
        pool.join()

        for r in results:
            _loop_over_results(r.get())
    else:
        for lines in namelists:
            results_append(_read_single_namelist(lines, parser, simple))
        for r in results:
            _loop_over_results(r)

    return nml
