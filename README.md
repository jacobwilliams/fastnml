# fastnml

Just some experiments using Python to read Fortran namelists.

Uses [f90nml](https://github.com/marshallward/f90nml).
Forked from [fast-namelist](https://github.com/jacobwilliams/fast-namelist).

The `fastnml` code only works with a specific subset of the namelist format.
It is not nearly as general or robust as f90nml, but it is much faster when
reading very large namelists. Also, both codes are tested using multiprocessing
to read many namelists in parallel.

## Test results

Each test was repeated 10 times using `timeit`.  Reported times are averages.

```plaintext
-----------------------------
test.nml
-----------------------------

f90nml: Read all at once from file (0 threads) :       11.39822994 sec
f90nml: Read in chunks (0 threads) :                   8.0026944 sec
f90nml: Read in chunks (1 threads) :                   9.166170519999998 sec
f90nml: Read in chunks (2 threads) :                   8.475483100000002 sec
f90nml: Read in chunks (3 threads) :                   6.027403049999998 sec
f90nml: Read in chunks (4 threads) :                   4.881079269999998 sec
fastnml: Read in chunks (0 threads) :                  0.8839235100000054 sec
fastnml: Read in chunks (1 threads) :                  1.0518486800000004 sec
fastnml: Read in chunks (2 threads) :                  0.959316849999999 sec
fastnml: Read in chunks (3 threads) :                  0.8456391800000006 sec
fastnml: Read in chunks (4 threads) :                  0.8256730300000072 sec

-----------------------------
test4.nml
-----------------------------

f90nml: Read all at once from file (0 threads) :       51.986049560000005 sec
f90nml: Read in chunks (0 threads) :                   35.282788670000016 sec
f90nml: Read in chunks (1 threads) :                   32.513629689999995 sec
f90nml: Read in chunks (2 threads) :                   21.438530609999997 sec
f90nml: Read in chunks (3 threads) :                   21.555509570000005 sec
f90nml: Read in chunks (4 threads) :                   21.915612649999957 sec
fastnml: Read in chunks (0 threads) :                  1.4239283299999896 sec
fastnml: Read in chunks (1 threads) :                  1.9683789400000022 sec
fastnml: Read in chunks (2 threads) :                  2.06403435000002 sec
fastnml: Read in chunks (3 threads) :                  2.1923845300000266 sec
fastnml: Read in chunks (4 threads) :                  2.2809260200000154 sec

-----------------------------
test4b.nml
-----------------------------

f90nml: Read all at once from file (0 threads) :       11.531519650000018 sec
f90nml: Read in chunks (0 threads) :                   13.162259780000023 sec
f90nml: Read in chunks (1 threads) :                   13.558090099999982 sec
f90nml: Read in chunks (2 threads) :                   8.623293990000002 sec
f90nml: Read in chunks (3 threads) :                   8.23252736999998 sec
f90nml: Read in chunks (4 threads) :                   8.187213680000013 sec
fastnml: Read in chunks (0 threads) :                  0.6564446500000031 sec
fastnml: Read in chunks (1 threads) :                  0.8659501000000092 sec
fastnml: Read in chunks (2 threads) :                  0.7474567600000228 sec
fastnml: Read in chunks (3 threads) :                  0.6686316899999838 sec
fastnml: Read in chunks (4 threads) :                  0.7651420700000017 sec

-----------------------------
test4c.nml
-----------------------------

f90nml: Read all at once from file (0 threads) :       15.820417150000003 sec
f90nml: Read in chunks (0 threads) :                   47.74203072 sec
f90nml: Read in chunks (1 threads) :                   42.154343699999984 sec
f90nml: Read in chunks (2 threads) :                   27.76226171999997 sec
f90nml: Read in chunks (3 threads) :                   25.114536729999962 sec
f90nml: Read in chunks (4 threads) :                   25.53975565999999 sec
fastnml: Read in chunks (0 threads) :                  1.6068046299999879 sec
fastnml: Read in chunks (1 threads) :                  2.2724403799999893 sec
fastnml: Read in chunks (2 threads) :                  2.1315237799999522 sec
fastnml: Read in chunks (3 threads) :                  2.2340645100000076 sec
fastnml: Read in chunks (4 threads) :                  2.2631622900000368 sec
```
