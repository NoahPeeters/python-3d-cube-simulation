__author__ = 'Noah'


from distutils.core import setup
from Cython.Build import cythonize

setup(
  name = 'my custom engine',
  ext_modules = cythonize("__init__.pyx"),
)