""" test cases """

import os
import unittest
from timeit import timeit
import f90nml
from fastnml import read_namelist, save_namelist


def read_from_file_f90nml(filename, n_threads, parser):
    "f90nml: Read all at once from file"
    return parser.read(filename)


def read_chunks_f90nml(filename, n_threads, parser):
    "f90nml: Read in chunks"
    return read_namelist(
        filename,
        n_threads=n_threads,
        parser=parser,
        simple=False,
    )  # use f90nml


def read_chunks_simple(filename, n_threads, parser):
    "fastnml: Read in chunks"
    return read_namelist(filename, n_threads=n_threads, parser=parser)


def run_read_tests(filenames, tests, parser, repeats):

    # print(f'Each test will be repeated {repeats} times.  '
    #       f'Reported times are averages.')

    for filename in filenames:
        print("")
        print("-----------------------------")
        print(str(filename))
        print("-----------------------------")
        print("")

        for t in tests:
            func, threads = t
            for n_threads in range(0, threads + 1):
                case = f"{func.__doc__} ({n_threads} threads) : "
                tottime = timeit(
                    lambda: func(filename, n_threads, parser), number=repeats
                )
                print(f"{case.ljust(55)}{tottime/repeats} sec")


class TestFastnml(unittest.TestCase):
    """
    Main unittest class.
    """

    def test_1(self):
        """
        Main unit test case for `fastnml`.
        """

        print("")
        print("---------------------")
        print(" run the save tests:")
        print("---------------------")
        print("")

        outfilename = "sample.nml"
        d = {
            "globvars": {
                "a": {
                    "TF": True,
                    "REAL": 2.0,
                    "int": 146,
                    "array1": [1, 2],
                    "array2": [1, 2],
                    "array3": [1, 2],
                    "str": "string 'with quotes'",
                    "list": ["a", "b", None, "d", "e"],
                }
            },
            "morevars": [{"name": 1}, {"name": 2}],
        }

        save_namelist(d, outfilename)
        with open(outfilename, "r") as f:
            print(f.read())

        print("")
        print("---------------------")
        print(" run the read tests:")
        print("---------------------")
        print("")

        filenames = [
            "test.nml",  # 112 namelists, all strings [8 sec]
            "test4.nml",  # 112 namelists, all strings, long keys w/ (2) [42 sec]
            "test4b.nml",  # 112 namelists, all strings, long keys no array [9 sec]
            "test4c.nml",  # 112 namelists, all strings, long keys w/ %  [12 sec]
        ]
        filenames = [os.path.join("tests", f) for f in filenames]

        n_threads_to_test = 4  # for threading cases
        tests = [
            (read_from_file_f90nml, 0),
            (read_chunks_f90nml, n_threads_to_test),
            (read_chunks_simple, n_threads_to_test),
        ]

        parser = f90nml.Parser()
        parser.global_start_index = 1

        repeats = 1

        run_read_tests(filenames, tests, parser, repeats)


if __name__ == "__main__":
    unittest.main()
