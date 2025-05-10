from setuptools import setup
from setuptools.extension import Extension

from distutils.core import setup
from Cython.Build import cythonize
import numpy
import traceback
import os

extensions = cythonize(
    "samplerbox_src/samplerbox_audio.pyx",
    compiler_directives={"language_level": "3"},
)

output_dir = "SamplerBox/samplerbox_src"
os.makedirs(output_dir, exist_ok=True)

try:
    setup(
        name="samplerbox_audio",
        ext_modules=extensions,
        include_dirs=[numpy.get_include()],
        zip_safe=False,
    )
except:
    traceback.print_exc()