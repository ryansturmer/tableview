try:
    from setuptools import setup
except:
    from distutils.core import setup

import tableview

setup(name='tableview',
      version=tableview.__version__,
      packages=['tableview'],
      description='Library for loading and manipulating tabular data.',
      author='Ryan Sturmer',
      author_email='ryansturmer@gmail.com',
      install_requires=['tablib'],
      url='http://www.github.com/ryansturmer/tableview')
