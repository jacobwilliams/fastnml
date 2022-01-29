"""
FastNml -- Read and write Fortran namelists fast.

## About

The `fastnml` code only works with a specific subset of the namelist format. It is not nearly as general or robust as [f90nml](https://github.com/marshallward/f90nml), but it is much faster when reading very large namelists. Also, both codes are tested using multiprocessing to read many namelists in parallel.

This library assumes the namelist is written one value per line.
This includes all types and array elements.  For example:
```fortran
&nml
 a = 1,
 c%a(1)%b = 1.0,
 c%a(2)%b = 1.0,
 d(1) = 2,
 d(2) = 3
/
```
If the simple parser fails, it defaults to using `f90nml` to read it.

## Public routines

 * `fastnml.reader.read_namelist`
 * `fastnml.writer.save_namelist`

## See also

 * [f90nml](https://github.com/marshallward/f90nml) -- the more general library
"""

__appname__ = 'fastnml'
__version__ = '2.0.0'
__credits__ = ['Jacob Williams', 'Randy Eckman']
__license__ = 'BSD'

import f90nml

from .reader import read_namelist
from .writer import save_namelist
