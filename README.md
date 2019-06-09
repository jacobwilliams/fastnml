Just some experiments using Python multiprocessing to read many namelists in parallel.

Uses [f90nml](https://github.com/marshallward/f90nml).

### Results for sample file

```
-----------------------------
 reading it all at once from file:
-----------------------------

7.988389253616333 sec

-----------------------------
 reading it all at once from string:
-----------------------------

7.9564528465271 sec

-----------------------------
 reading chunks without threads:
-----------------------------

3.159278631210327 sec

-----------------------------
 reading chunks in parallel:
-----------------------------

using 1 threads.
3.38427996635437 sec


-----------------------------
 reading chunks in parallel:
-----------------------------

using 2 threads.
1.7325119972229004 sec


-----------------------------
 reading chunks in parallel:
-----------------------------

using 3 threads.
1.227613925933838 sec


-----------------------------
 reading chunks in parallel:
-----------------------------

using 4 threads.
1.0094490051269531 sec


-----------------------------
 reading chunks in parallel:
-----------------------------

using 5 threads.
1.0116667747497559 sec


-----------------------------
 reading chunks in parallel:
-----------------------------

using 6 threads.
1.028597116470337 sec

```