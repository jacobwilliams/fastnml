Just some experiments using Python to read Fortran namelists.

Uses [f90nml](https://github.com/marshallward/f90nml).

The `fast-namelist` code only works with a specific subset of the namelist format. It is not nearly as general or robust as f90nml, but it is much faster when reading very large namelists. Also, both codes are tested using multiprocessing to read many namelists in parallel.

### Test results

```
-----------------------------
files/test.nml
-----------------------------

f90nml: Read all at once from file :                   6.535212993621826 sec
f90nml: Read in chunks (no threads) :                  4.172897815704346 sec
f90nml: Read in chunks (threads) (1 threads) :         4.220002889633179 sec
f90nml: Read in chunks (threads) (2 threads) :         2.226668119430542 sec
f90nml: Read in chunks (threads) (3 threads) :         1.606447696685791 sec
Fast-namelist: Read in chunks (no threads) :           0.3533191680908203 sec
Fast-namelist: Read in chunks (threads) (1 threads) :  0.45674991607666016 sec
Fast-namelist: Read in chunks (threads) (2 threads) :  0.2564396858215332 sec
Fast-namelist: Read in chunks (threads) (3 threads) :  0.2612619400024414 sec

-----------------------------
files/test4.nml
-----------------------------

f90nml: Read all at once from file :                   31.266510248184204 sec
f90nml: Read in chunks (no threads) :                  21.861836671829224 sec
f90nml: Read in chunks (threads) (1 threads) :         19.341630935668945 sec
f90nml: Read in chunks (threads) (2 threads) :         10.51621389389038 sec
f90nml: Read in chunks (threads) (3 threads) :         7.911913871765137 sec
Fast-namelist: Read in chunks (no threads) :           1.2729849815368652 sec
Fast-namelist: Read in chunks (threads) (1 threads) :  1.5219929218292236 sec
Fast-namelist: Read in chunks (threads) (2 threads) :  1.1071321964263916 sec
Fast-namelist: Read in chunks (threads) (3 threads) :  1.088028907775879 sec

-----------------------------
files/test4b.nml
-----------------------------

f90nml: Read all at once from file :                   6.987016916275024 sec
f90nml: Read in chunks (no threads) :                  7.977221965789795 sec
f90nml: Read in chunks (threads) (1 threads) :         8.136826753616333 sec
f90nml: Read in chunks (threads) (2 threads) :         4.201086044311523 sec
f90nml: Read in chunks (threads) (3 threads) :         2.9662628173828125 sec
Fast-namelist: Read in chunks (no threads) :           0.3699190616607666 sec
Fast-namelist: Read in chunks (threads) (1 threads) :  0.46530675888061523 sec
Fast-namelist: Read in chunks (threads) (2 threads) :  0.2625417709350586 sec
Fast-namelist: Read in chunks (threads) (3 threads) :  0.26222896575927734 sec

-----------------------------
files/test4c.nml
-----------------------------

f90nml: Read all at once from file :                   9.853593826293945 sec
f90nml: Read in chunks (no threads) :                  32.57745814323425 sec
f90nml: Read in chunks (threads) (1 threads) :         30.11258316040039 sec
f90nml: Read in chunks (threads) (2 threads) :         14.676537036895752 sec
f90nml: Read in chunks (threads) (3 threads) :         10.478646993637085 sec
Fast-namelist: Read in chunks (no threads) :           1.18827486038208 sec
Fast-namelist: Read in chunks (threads) (1 threads) :  1.6335108280181885 sec
Fast-namelist: Read in chunks (threads) (2 threads) :  1.54339599609375 sec
Fast-namelist: Read in chunks (threads) (3 threads) :  1.2029950618743896 sec
```