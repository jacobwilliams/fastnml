
import f90nml
import multiprocessing as mp
import time
import re
import json
import sys

###############################################################################
def get_array_index(str):
    """
        If the variable name represents an array element (e.g., 'VAR(1)'),
        then return the array index (1-based) and the variable name.
        Otherwise, return None.
    """

    # initial quick check:
    if '(' not in str:
        return None, None

    array_rg = re.compile('((?:[a-z][a-z0-9_]*))(\\()(\\d+)(\\))(.*)', re.IGNORECASE | re.DOTALL)

    m = array_rg.search(str.strip())
    if m:
        if (m.group(5) == ''):
            return int(m.group(3)), m.group(1)  # index, arrayname
        else:
            # invalid array string
            return None, None
    else:
        return None, None

###############################################################################
def pathSet(dictionary, path, value, sep='%'):
    '''
        Sets a variable in a dictionary, given the namelist path string.
        Assumes the input path uses Fortran-style 1-based indexing of arrays
    '''

    path = path.split(sep)
    key = path[-1]
    dictionary = pathGet(dictionary, sep.join(path[:-1]), sep=sep)
    i, arrayname = get_array_index(key)
    if (i is not None):
        # it is an array element:
        if (arrayname not in dictionary):
            dictionary[arrayname] = [None]
        if len(dictionary[arrayname])<i:
            # have to add this element
            for j in range(len(dictionary[arrayname]),i):
                dictionary[arrayname].append(None)
        dictionary[arrayname][i - 1] = value
    else:
        # it is just a normal variable:
        dictionary[key] = value

###############################################################################
def pathGet(dictionary, path, sep='%'):
    '''
        Returns an item in a dictionary given the namelist path string.
        Assumes the input path uses Fortran-style 1-based indexing of arrays
    '''

    for item in path.split(sep):
        i, arrayname = get_array_index(item)
        if (i is not None):
            # it is an array element:
            # create this item since it isn't there
            if (arrayname not in dictionary):
                dictionary[arrayname] = [None]
            if len(dictionary[arrayname])<i:
                # have to add this element
                for j in range(len(dictionary[arrayname]),i):
                    dictionary[arrayname].append(None)

            # make sure it's a dict:
            if (not isinstance(dictionary[arrayname][i - 1],dict)):
                dictionary[arrayname][i - 1] = f90nml.Namelist({})

            dictionary = dictionary[arrayname][i - 1]

        else:
            # it is just a normal variable:

            # make sure it's a dict:
            if (not isinstance(dictionary,dict)):
                dictionary = f90nml.Namelist({})

            if (item not in dictionary):
                dictionary[item] = f90nml.Namelist({})

            dictionary = dictionary[item]

    return dictionary

#####################################
def read_a_namelist(str,parser):
    """ using f90nml """
    try:
        nml = parser.reads(str)  # f90nml 1.1
    except:
        nml = parser._readstream(iter(str.splitlines()),{})  # previous version
    return nml

#####################################
def string_to_number(s):
    try:
        return int(s)
    except:
        try:
            return float(s)
        except:
            return None

#####################################
def nml_value_to_python_value(value):

    value_str = value.strip()

    value_str_bool = value_str.lower().strip('.')

    if (value_str_bool=='t' or value_str_bool=='true'):
        # logical
        value = True
    elif (value_str_bool=='f' or value_str_bool=='false'):
        # logical
        value = False
    elif (value_str[0]=='"' and value_str[-1]=='"'):
        # string
        value = value_str.strip('"')
    elif (value_str[0]=="'" and value_str[-1]=="'"):
        # string
        value = value_str.strip("'")
    else:
        # int or double:
        value_num = string_to_number(value_str)
        if value_num != None:
            value = value_num # int or double
        else:
            value = value_str # just keep it as a string

    return value

#####################################
def read_a_namelist_simple(lines):

    """ simple parser. assumes each variable is declared on a single line.
        For example: `val%a(2)%b = value,`

        Note that comment lines and blank lines have already been removed.
    """

    nml = None

    for i,line in enumerate(lines):

        if i==0:
            # create namelist dict:
            namelist_name = line.lstrip('&').strip().lower()
            nml = f90nml.Namelist({namelist_name: f90nml.Namelist({})})
        else:

            d = line.split('=', 1)

            if (len(d)<2):
                continue

            path = d[0].strip()

            # convert the string to a Python value:
            value = nml_value_to_python_value(d[1].rstrip(', '))

            # add this value to the namelist:
            pathSet(nml[namelist_name], path, value)

    return nml

#####################################
def split_namelist_str(str):
    """ alternate version of split_namelist_file with the string as an input """
    namelists = []
    i = -1
    started=False
    f = str.split('\n')
    for line in f:
        line = line.strip()
        if (len(line)>0):
            if (line[0]!='!'):
                if (line[0]=='&'): # start a namelist
                    i = i + 1
                    namelists.append([])
                    started = True
                elif (line[0:1]=='/'): # end a namelist
                    started = False
                    namelists[i].append( line )
                    continue
                if started:
                    namelists[i].append( line )
    return namelists

#####################################
def split_namelist_file(filename):
    """ split a namelist file into an array of namelist strings """
    namelists = []
    i = -1
    started=False
    with open(filename,'r') as f:
        for line in f:
            line = line.strip()
            if (len(line)>0):
                if (line[0]!='!'):
                    if (line[0]=='&'): # start a namelist
                        i = i + 1
                        namelists.append([])
                        started = True
                    elif (line[0:1]=='/'): # end a namelist
                        started = False
                        namelists[i].append( line )
                        continue
                    if started:
                        namelists[i].append( line )

    print(str(len(namelists))+' namelists found in file.')
    return namelists

#####################################
def read_namelist_fast(filename,n_threads=4):

    parser = f90nml.Parser()
    parser.global_start_index = 1  # need this for my use cases

    namelists = split_namelist_file(filename)
    # with open(filename,'r') as f:
    #     full_namelist_str = f.read()
    # namelists = split_namelist_str(full_namelist_str)

    n_threads = max(1,min(mp.cpu_count(),n_threads))
    print('using '+str(n_threads)+' threads.')
    pool = mp.Pool(processes=n_threads)
    results = []
    for s in namelists:
        #results.append(pool.apply_async(read_a_namelist,(s,parser)))
        results.append(pool.apply_async(read_a_namelist_simple,(s,)))   ## test ##

    pool.close()
    pool.join()

    # create a single namelist from the results:
    nml = f90nml.Namelist({})
    for r in results:
        for key, value in r.get().items():
            if key in nml:
                # array of namelists:
                if isinstance(nml[key],list):
                    nml[key].append(value)
                else:
                    nml[key] = [nml[key], value]
            else:
                nml[key] = value

    return nml

#####################################
def read_namelist_fast_nothreads(filename):

    """ alternate version of read_namelist_fast that doesn't
        use threads.
    """

    parser = f90nml.Parser()
    parser.global_start_index = 1  # need this for my use cases

    #... example run times:
    # split: 0.0310819149017334 sec
    # parse: 1.3101840019226074 sec
    # join: 0.0004949569702148438 sec

    #start_time = time.time()

    namelists = split_namelist_file(filename)

    #end_time = time.time()
    #print('  split: ' + str(end_time-start_time) + ' sec')

    # with open(filename,'r') as f:
    #     full_namelist_str = f.read()
    # namelists = split_namelist_str(full_namelist_str)

    #start_time = time.time()

    results = []
    for s in namelists:
        #results.append(read_a_namelist(s,parser))
        results.append(read_a_namelist_simple(s))    ## test ##

    #end_time = time.time()
    #print('  parse: ' + str(end_time-start_time) + ' sec')

    #start_time = time.time()

    # create a single namelist from the results:
    nml = f90nml.Namelist({})
    for r in results:
        for key, value in r.items():
            if key in nml:
                # array of namelists:
                if isinstance(nml[key],list):
                    nml[key].append(value)
                else:
                    nml[key] = [nml[key], value]
            else:
                nml[key] = value

    #end_time = time.time()
    #print('  join: ' + str(end_time-start_time) + ' sec')

    return nml


#####################################
def traverse_dict(f,d,path='',sep='%'):

    """ traverse a dict and print the paths to each variable in namelist style """

    if isinstance(d, dict):
        for k,v in d.items():
            if isinstance(v, list):
                index = 0
                for element in v:
                    index = index + 1
                    path_tmp = k+'('+str(index)+')'
                    if path.strip() != '':
                        path_tmp = path+sep+path_tmp
                    traverse_dict(f,element,path_tmp)
            else:
                path_tmp = k
                if path.strip() != '':
                    path_tmp = path+sep+path_tmp
                traverse_dict(f,v,path_tmp)
    elif isinstance(d, list):
        for element in d:
            traverse_dict(f,element,path)
    else:
        path = path.lower()
        if (d == None):
            pass
        elif isinstance(d, str):
            f.write(' '+path+" = '"+d+"'"+',\n')
        elif isinstance(d, bool):
            f.write(' '+path+' = '+['F','T'][int(d)]+',\n')
        elif isinstance(d, int):
            f.write(' '+path+' = '+str(d)+',\n')
        elif isinstance(d,float):
            f.write(' '+path+' = '+'{:.17E}'.format(d)+',\n')

#####################################
def print_namelist(f,namelist_name, d):

    #f.write('!=========================================================================================\n')
    f.write('&'+namelist_name.lower()+'\n')
    traverse_dict(f,d)
    f.write('/\n')
    #f.write('!=========================================================================================\n')
    f.write('\n')

#####################################
def print_namelists(d,filename):

    """ Print a dict as a namelist file.
        Assumes an f90nml namelist style structure.
        It is a dict of dicts (some of which can be lists)

        This uses the "simple" format, with one variable per line.
    """

    with open (filename,'w') as f:
        for k,v in d.items():
            if isinstance(v, list):
                for element in v:
                    print_namelist(f,k,element)
            elif isinstance(v, dict):
                print_namelist(f,k,v)


########################################################################
if __name__ == "__main__":

    """ test case """

    filename = 'files/test.nml'       # 112 namelists -- all strings [8 sec]
    #filename = 'files/test4.nml'       # 112 namelists -- all strings -- longer keys w/ (2) [42 sec]
    #filename = 'files/test4b.nml'     # 112 namelists -- all strings -- longer keys no array  [9 sec]
    #filename = 'files/test4c.nml'     # 112 namelists -- all strings -- longer keys w/ %  [12 sec]

    #filename = 'files/test2.ideck'

    ##################

    print('')
    print('-----------------------------')
    print(' print a sample namelist:')
    print('-----------------------------')
    print('')

    d = {  "globvars": {
        "a": {
            "TF": True,
            "REAL": 2.0,
            "int": 146,
            "array1": [1,2],
            "array2": [1,2],
            "array3": [1,2],
            "str": "string",
            "list": [
                "a",
                "b",
                None,
                "d",
                "e"
                ]
            }
        },
        "morevars": [{"name":1},{"name":2}]
    }

    print_namelists(d,'sample.nml')

    ##################

    print('')
    print('-----------------------------')
    print(' reading it all at once from file:')
    print('-----------------------------')
    print('')
    start_time = time.time()

    p = f90nml.Parser()
    p.global_start_index = 1
    nml = p.read(filename)

    end_time = time.time()

    # print('')
    # print(nml)
    print_namelists(nml,filename+'_reprint')

    print(str(end_time-start_time) + ' sec')

    with open('dump_f90nml.json', 'w') as f:
        json.dump(nml,f,indent=2)

    ##################

    # print('')
    # print('-----------------------------')
    # print(' reading it all at once from string:')
    # print('-----------------------------')
    # print('')
    # start_time = time.time()

    # p = f90nml.Parser()
    # p.global_start_index = 1
    # with open(filename,'r') as f:
    #     s = f.read()
    #     nml = p._readstream(iter(s.splitlines()),{})

    # end_time = time.time()
    # print(str(end_time-start_time) + ' sec')

    # with open('dump_f90nml.json', 'w') as f:
    #     json.dump(nml,f,indent=2)

    # # print('')
    # # print(nml)

    # ##################


    print('')
    print('-----------------------------')
    print(' reading chunks without threads:')
    print('-----------------------------')
    print('')
    start_time = time.time()

    nml = read_namelist_fast_nothreads(filename)

    end_time = time.time()
    print(str(end_time-start_time) + ' sec')

    with open('dump_simple.json', 'w') as f:
        json.dump(nml,f,indent=2)

    #print('')
    #print(nml)

    #sys.exit(-1)

    ##################

    for n_threads in range(1,7):

        print('')
        print('-----------------------------')
        print(' reading chunks in parallel:')
        print('-----------------------------')
        print('')
        start_time = time.time()

        nml = read_namelist_fast(filename, n_threads=n_threads)
        end_time = time.time()
        print(str(end_time-start_time) + ' sec')

        # print('')
        # print(nml)

        print('')
