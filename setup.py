#!/usr/bin/env python

import setuptools
from distutils.core import setup, Extension
import numpy as np

setup(
    name='DummyBroker',
    version='0.0.x',
    author='Brookhaven National Lab',
    packages=["dummyBroker",
              ],
    include_dirs=[np.get_include()],
    )
