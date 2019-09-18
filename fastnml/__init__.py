__version__ = '0.1.2'

import f90nml  # noqa: E402
assert f90nml

from .reader import (
    read_namelist,
)  # noqa: E402
assert all((
    read_namelist,
))

from .writer import (
    save_namelist,
)  # noqa: E402
assert all((
    save_namelist,
))
