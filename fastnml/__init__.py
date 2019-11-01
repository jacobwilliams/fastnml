__version__ = '1.0.0'

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
    write_namelist_to_stream,
)  # noqa: E402
assert all((
    save_namelist,
    write_namelist_to_stream,
))
