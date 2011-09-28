from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("backend.pyback", ["backend/pyback.pyx"],extra_compile_args=['-msse2', '-O3'],extra_link_args=['-lrt'])]
)
