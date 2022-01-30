![fastnml](media/fastnml.png)
============

A Python library to quickly read Fortran namelists.

![Build Status](https://github.com/jacobwilliams/fastnml/actions/workflows/unittest.yml/badge.svg)
![Build Status](https://github.com/jacobwilliams/fastnml/actions/workflows/python-publish.yml/badge.svg)

### Description

The `fastnml` code only works with a specific subset of the namelist format. It is not nearly as general or robust as [f90nml](https://github.com/marshallward/f90nml), but it is much faster when reading very large namelists. Also, both codes are tested using multiprocessing to read many namelists in parallel.

### Installing

Fastnml is available on [PyPI](https://pypi.org/project/fastnml/). So just `pip install fastnml`.

### Documentation

The documentation for the current `master` branch can be found [here](https://jacobwilliams.github.io/fastnml/). This is generated with `pdoc3` by running `pdoc --html fastnml --force`.

### Dependencies

 * [f90nml](https://github.com/marshallward/f90nml) -- the more general library

 ### Other links

  * [Fastnml on PyPI](https://pypi.org/project/fastnml/)
