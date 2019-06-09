
import f90nml
import multiprocessing as mp
import time

#####################################
def read_a_namelist(str,parser):
    try:
        nml = parser.reads(str)  # f90nml 1.1
    except:
        nml = parser._readstream(iter(str.splitlines()),{})  # previous version
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
            if (line[0:1]!='!'):
                if (line[0:1]=='&'): # start a namelist
                    i = i + 1
                    namelists.append('')
                    started = True
                elif (line[0:1]=='/'): # end a namelist
                    started = False
                    namelists[i] = namelists[i] + line + '\n'
                    continue
                if started:
                    namelists[i] = namelists[i] + line + '\n'
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
                if (line[0:1]!='!'):
                    if (line[0:1]=='&'): # start a namelist
                        i = i + 1
                        namelists.append('')
                        started = True
                    elif (line[0:1]=='/'): # end a namelist
                        started = False
                        namelists[i] = namelists[i] + line + '\n'
                        continue
                    if started:
                        namelists[i] = namelists[i] + line + '\n'
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
        results.append(pool.apply_async(read_a_namelist,(s,parser)))
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

    namelists = split_namelist_file(filename)
    # with open(filename,'r') as f:
    #     full_namelist_str = f.read()
    # namelists = split_namelist_str(full_namelist_str)

    results = []
    for s in namelists:
        results.append(read_a_namelist(s,parser))

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

    return nml

########################################################################
if __name__ == "__main__":

    """ test case """

    filename = 'files/test.nml'

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
    print(str(end_time-start_time) + ' sec')

    # print('')
    # print(nml)

    ##################


    print('')
    print('-----------------------------')
    print(' reading it all at once from string:')
    print('-----------------------------')
    print('')
    start_time = time.time()

    p = f90nml.Parser()
    p.global_start_index = 1
    with open(filename,'r') as f:
        s = f.read()
        nml = p._readstream(iter(s.splitlines()),{})

    end_time = time.time()
    print(str(end_time-start_time) + ' sec')

    # print('')
    # print(nml)

    ##################


    print('')
    print('-----------------------------')
    print(' reading chunks without threads:')
    print('-----------------------------')
    print('')
    start_time = time.time()

    nml = read_namelist_fast_nothreads(filename)

    end_time = time.time()
    print(str(end_time-start_time) + ' sec')

    # print('')
    # print(nml)


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
