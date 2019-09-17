__version__ = '0.1.1'

import f90nml  # noqa: E402
assert f90nml

from .process import (
    read_namelist,
    save_namelist,
)  # noqa: E402
assert all((
    read_namelist,
    save_namelist,
))
