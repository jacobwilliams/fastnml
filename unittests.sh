#!/bin/bash

#
# Run the unit tests.
#

# code coverage
coverage run test.py
coverage html
coverage report

# documentation
pdoc --html fastnml --force