# setup.py
import numpy as np
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("./loop_cython.pyx"),
    compiler_directives={"language_level": "3"},
    include_dirs=[np.get_include()],
)
