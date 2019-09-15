""" test case """

import time
import f90nml


# filenames to test:
# 112 namelists -- all strings [8 sec]
filename = 'files/test.nml'
# 112 namelists -- all strings -- longer keys w/ (2) [42 sec]
filename1 = 'files/test4.nml'
# 112 namelists -- all strings -- longer keys no array  [9 sec]
filename2 = 'files/test4b.nml'
# 112 namelists -- all strings -- longer keys w/ %  [12 sec]
filename3 = 'files/test4c.nml'

filenames = [filename, filename1, filename2, filename3]

# cases to run:
def read_from_file_f90nml(filename):
    p = f90nml.Parser()
    p.global_start_index = 1
    nml = p.read(filename)
    return nml

def read_chunks_without_threads_f90nml(filename):
    nml = read_namelist_fast_nothreads(filename,
                                        simple=False)  # use f90nml
    return nml

def read_chunks_with_threads_f90nml(filename, n_threads):
    nml = read_namelist_fast(filename, n_threads=n_threads, simple=False)
    return nml

def read_chunks_without_threads_simple(filename):
    nml = read_namelist_fast_nothreads(filename, simple=True)
    return nml

def read_chunks_with_threads_simple(filename, n_threads):
    nml = read_namelist_fast(filename, n_threads=n_threads, simple=True)
    return nml

##################

n_threads_to_test = 4  # for threading cases

tests = [('f90nml: Read all at once from file',
          read_from_file_f90nml, 0),
          ('f90nml: Read in chunks (no threads)',
          read_chunks_without_threads_f90nml, 0),
          ('f90nml: Read in chunks (threads)',
          read_chunks_with_threads_f90nml, n_threads_to_test),
          ('Fast-namelist: Read in chunks (no threads)',
          read_chunks_without_threads_simple, 0),
          ('Fast-namelist: Read in chunks (threads)',
          read_chunks_with_threads_simple, n_threads_to_test)]

print('')
print('-----------------------------')
print(' print a sample namelist:')
print('-----------------------------')
print('')

d = {"globvars": {
    "a": {
        "TF": True,
        "REAL": 2.0,
        "int": 146,
        "array1": [1, 2],
        "array2": [1, 2],
        "array3": [1, 2],
        "str": "string 'with quotes'",
        "list": [
            "a",
            "b",
            None,
            "d",
            "e"
            ]
        }
    },
    "morevars": [{"name": 1}, {"name": 2}]
}

print_namelists(d, 'sample.nml')

##################

print('')
print('-----------------------------')
print(' run all the tests:')
print('-----------------------------')
print('')

results = {}

for filename in filenames:
    print('')
    print('-----------------------------')
    print(str(filename))
    print('-----------------------------')
    print('')

    for test in tests:

        start_time = time.time()

        if (test[2] != 0):
            for n_threads in range(1, test[2]):
                start_time = time.time()
                nml = test[1](filename, n_threads)
                end_time = time.time()
                case = test[0] + f' ({n_threads} threads) : '
                print(case.ljust(55) + str(end_time-start_time) + ' sec')
        else:
            start_time = time.time()
            nml = test[1](filename)
            end_time = time.time()
            case = test[0] + ' : '
            print(case.ljust(55) + str(end_time-start_time) + ' sec')

        # print_namelists(nml,filename+'_reprint')
        # with open('dump.json', 'w') as f:
        #     json.dump(nml,f,indent=2)

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
