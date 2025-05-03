<h1 align="center">
<img src="https://raw.githubusercontent.com/jacobwilliams/fastnml/master/media/fastnml.png" width=800">
</h1><br>

A Python library to quickly read Fortran namelists.

[![CI Status](https://github.com/jacobwilliams/fastnml/actions/workflows/CI.yml/badge.svg)](https://github.com/jacobwilliams/fastnml/actions)
[![PyPI Downloads](https://img.shields.io/pypi/dm/fastnml.svg?label=PyPI%20downloads)](https://pypi.org/project/fastnml/)
[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/fastnml.svg?label=Conda%20downloads)](
https://anaconda.org/conda-forge/fastnml)

### Description

The `fastnml` code only works with a specific subset of the namelist format. It is not nearly as general or robust as [f90nml](https://github.com/marshallward/f90nml), but it is much faster when reading very large namelists. Also, both codes are tested using multiprocessing to read many namelists in parallel.

### Installing

* Install from [PyPI](https://pypi.org/project/fastnml/) using pip: `pip install fastnml`
* Install from [conda-forge](https://anaconda.org/conda-forge/fastnml) using conda: `conda install -c conda-forge fastnml`

### Documentation

The API documentation for the current `master` branch can be found [here](https://jacobwilliams.github.io/fastnml/). This is generated with `pdoc3` by running `pdoc --html fastnml --force`.

### Dependencies

 * [f90nml](https://github.com/marshallward/f90nml) -- the more general library

 ### Other links

  * [Fastnml on PyPI](https://pypi.org/project/fastnml/)
  * [Fastnml on conda-forge](https://anaconda.org/conda-forge/fastnml)
  * [fastnml-feedstock for conda-forge](https://github.com/conda-forge/fastnml-feedstock)
