from setuptools import setup, find_packages
from os.path import abspath, dirname, join as ospjoin

here = abspath(dirname(__file__))

# Get the long description from the README file
with open(ospjoin(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fastnml',
    version='0.1.0',
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
