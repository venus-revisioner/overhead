# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Path: overhead\cryptooh\apps.py
# Compare this snippet from overhead\__init__.py:

from setuptools import setup, find_packages
packages = find_packages(),

package_data = {
	'overhead': ['README.rst', 'LICENSE'],
}

setup(name             = "overhead",
      version          = "0.7.1",
      author           = "venus-revisioner",
      author_email     = "johan.uhd@gmail.com",
      url              = "https://github.com/venus-revisioner/overhead.git",
      description      = "'Overhead' tools of mixed-bag-distribution, self-organized.",
      readme 	       = "README.rst",
      license   	   =  "LICENSE",
      long_description = "'TL;DR'",
      py_modules       = ["overhead.aioh", "overhead.cryptooh", "overhead.opengloh"],
      include_package_data=True,
      zip_safe=False
      )

# Path: overhead\cryptooh\apps.py
# Compare this snippet from overhead\__init__.py:


# Path: overhead\setup.py
# import os
# import sys

# from setuptools.command.test import test as TestCommand
# from setuptools.command.install import install as InstallCommand
# Path: overhead\setup.py

# def read(fname):
# 	return open(os.path.join(os.path.dirname(__file__), fname)).read()

# Path: overhead\setup.py
# setup(
# 	name = "overhead",
# 	version = "0.6.9",
# 	author = "venus-revisioner",
# 	author_email = "johan.uhd@gmail.com",
# 	description ="Overhead is fun!",
# 	license = "MIT",
# 	keywords = "overhead", "venus-revisioner",
# 	url = "https://github.com/venus-revisioner/overhead.git",
# 	packages = find_packages(),
# 	long_description = read('README.md'),
# 	classifiers = [
# 		"Development Status :: 3 - Alpha",
# 		"Topic :: Utilities",
# 		"License :: OSI Approved :: MIT License",
# 	],








# setup()

# Path: overhead\overhead\__init__.py



# cd overhead
# python setup.py sdist
# python setup.py bdist_wheel
# python setup.py bdist_egg
# python setup.py bdist_rpm
# python setup.py bdist_dumb
# python setup.py bdist_wininst
# python setup.py bdist_msi
# python setup.py bdist
# python setup.py install
# python setup.py install_lib
# python setup.py install_headers
# python setup.py install_scripts
# python setup.py install_data
# python setup.py register
# python setup.py upload
# python setup.py sdist upload
# python setup.py bdist_wheel upload
# python setup.py bdist_egg upload
# python setup.py bdist_rpm upload
# python setup.py bdist_dumb upload
# python setup.py bdist_wininst upload
# python setup.py bdist_msi upload
# python setup.py bdist upload
# python setup.py register upload
# python setup.py check
# python setup.py clean
# python setup.py test
# python setup.py test --test-suite=tests.test_suite
# python setup.py test --test-suite=tests.test_suite --test-runner=unittest.TextTestRunner
# python setup.py test --test-suite=tests.test_suite --test-runner=unittest.TextTestRunner --test-args="--verbose"

