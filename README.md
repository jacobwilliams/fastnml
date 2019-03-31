Just some experiments using Python multiprocessing to read many namelists in parallel.

Uses [f90nml](https://github.com/marshallward/f90nml).

### Results for sample file

```
-----------------------------
 reading it all at once from file:
-----------------------------

6.814043045043945 sec

-----------------------------
 reading it all at once from string:
-----------------------------

6.754244089126587 sec

-----------------------------
 reading it in parallel:
-----------------------------

using 1 threads.
2.543579339981079 sec


-----------------------------
 reading it in parallel:
-----------------------------

using 2 threads.
1.4157969951629639 sec


-----------------------------
 reading it in parallel:
-----------------------------

using 3 threads.
0.9900557994842529 sec


-----------------------------
 reading it in parallel:
-----------------------------

using 4 threads.
0.8005549907684326 sec


-----------------------------
 reading it in parallel:
-----------------------------

using 5 threads.
0.8011331558227539 sec


-----------------------------
 reading it in parallel:
-----------------------------

using 6 threads.
0.8105840682983398 sec

```