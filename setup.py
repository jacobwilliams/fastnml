from setuptools import setup, find_packages
from os.path import abspath, dirname, join as ospjoin
import re

here = abspath(dirname(__file__))


def find_version(filename):
    with open(filename, 'r') as f:
        version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


project_version = find_version(ospjoin(here, 'fastnml', '__init__.py'))

# Get the long description from the README file
with open(ospjoin(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fastnml',
    version=project_version,
    description='A simple fast namelist parser',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/emanspeaks/fastnml',
    author='Randy Eckman',
    author_email='emanspeaks@gmail.com',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
    ],
    keywords='namelist fortran',
    packages=find_packages(exclude=['docs', 'tests']),
    python_requires='>=3.5',
    install_requires=['f90nml>=1.0.2'],
)
