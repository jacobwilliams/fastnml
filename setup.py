from setuptools import setup, find_packages
from os.path import abspath, dirname, join as ospjoin
import re

here = abspath(dirname(__file__))


def find_version(filename):
    with open(filename, "r") as f:
        version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


project_version = find_version(ospjoin(here, "fastnml", "__init__.py"))

# Get the long description from the README file
with open(ospjoin(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="fastnml",
    version=project_version,
    description="A simple fast namelist parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jacobwilliams/fastnml",
    author="Jacob Williams",
    author_email="jacob@degenerateconic.com",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    keywords="namelist fortran",
    packages=find_packages(exclude=["docs", "tests"]),
    python_requires=">=3.6",
    install_requires=["f90nml>=1.1.0"],
)
