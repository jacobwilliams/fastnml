# fast-namelist

A Python library to quickly read Fortran namelists.

The `fastnml` code only works with a specific subset of the namelist format. It is not nearly as general or robust as [f90nml](https://github.com/marshallward/f90nml), but it is much faster when reading very large namelists. Also, both codes are tested using multiprocessing to read many namelists in parallel.

### Test results

Each test was repeated 10 times using `timeit`.  Reported times are averages.

```plaintext
-----------------------------
test.nml
-----------------------------

f90nml: Read all at once from file (0 threads) :       8.583405899999999 sec
f90nml: Read in chunks (0 threads) :                   4.6838695999999995 sec
f90nml: Read in chunks (1 threads) :                   4.937748499999998 sec
f90nml: Read in chunks (2 threads) :                   2.5980871000000008 sec
f90nml: Read in chunks (3 threads) :                   1.9029447000000026 sec
f90nml: Read in chunks (4 threads) :                   1.5512989000000026 sec
fastnml: Read in chunks (0 threads) :                  0.4889088999999984 sec
fastnml: Read in chunks (1 threads) :                  0.6726308000000003 sec
fastnml: Read in chunks (2 threads) :                  0.49938099999999963 sec
fastnml: Read in chunks (3 threads) :                  0.4068599000000006 sec
fastnml: Read in chunks (4 threads) :                  0.39626249999999885 sec

-----------------------------
test4.nml
-----------------------------

f90nml: Read all at once from file (0 threads) :       33.611139800000004 sec
f90nml: Read in chunks (0 threads) :                   24.9464172 sec
f90nml: Read in chunks (1 threads) :                   22.7366057 sec
f90nml: Read in chunks (2 threads) :                   11.587078000000005 sec
f90nml: Read in chunks (3 threads) :                   8.443905700000016 sec
f90nml: Read in chunks (4 threads) :                   6.226133799999985 sec
fastnml: Read in chunks (0 threads) :                  1.0096473000000117 sec
fastnml: Read in chunks (1 threads) :                  1.3259695000000136 sec
fastnml: Read in chunks (2 threads) :                  1.036898100000002 sec
fastnml: Read in chunks (3 threads) :                  1.159534999999977 sec
fastnml: Read in chunks (4 threads) :                  1.0741505999999958 sec

-----------------------------
test4b.nml
-----------------------------

f90nml: Read all at once from file (0 threads) :       7.980078500000019 sec
f90nml: Read in chunks (0 threads) :                   8.990785700000004 sec
f90nml: Read in chunks (1 threads) :                   9.161885600000005 sec
f90nml: Read in chunks (2 threads) :                   4.726017299999995 sec
f90nml: Read in chunks (3 threads) :                   3.553860500000013 sec
f90nml: Read in chunks (4 threads) :                   2.7503221000000053 sec
fastnml: Read in chunks (0 threads) :                  0.37847529999999097 sec
fastnml: Read in chunks (1 threads) :                  0.677776300000005 sec
fastnml: Read in chunks (2 threads) :                  0.5017527999999913 sec
fastnml: Read in chunks (3 threads) :                  0.5212353000000007 sec
fastnml: Read in chunks (4 threads) :                  0.41918479999998226 sec

-----------------------------
test4c.nml
-----------------------------

f90nml: Read all at once from file (0 threads) :       11.072592100000008 sec
f90nml: Read in chunks (0 threads) :                   40.973017 sec
f90nml: Read in chunks (1 threads) :                   28.69594159999997 sec
f90nml: Read in chunks (2 threads) :                   14.902919899999972 sec
f90nml: Read in chunks (3 threads) :                   10.096066500000006 sec
f90nml: Read in chunks (4 threads) :                   8.136358200000018 sec
fastnml: Read in chunks (0 threads) :                  1.1177955999999654 sec
fastnml: Read in chunks (1 threads) :                  1.526128500000027 sec
fastnml: Read in chunks (2 threads) :                  1.060428600000023 sec
fastnml: Read in chunks (3 threads) :                  0.9990597000000321 sec
fastnml: Read in chunks (4 threads) :                  1.0846950000000106 sec
```

### Dependencies

 * [f90nml](https://github.com/marshallward/f90nml) -- the more general library
