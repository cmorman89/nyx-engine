import glob
from setuptools import setup
from Cython.Build import cythonize
import numpy as np

pyx_files = glob.glob("**/*.pyx", recursive=True)


setup(
    ext_modules=cythonize(pyx_files),
    include_dirs=[np.get_include()]
)