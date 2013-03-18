import tableview

try:
    from setuptools import setup, Command
except:
    from distutils.core import setup, Command


class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import sys,subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


setup(name='tableview',
      version=tableview.__version__,
      packages=['tableview'],
      cmdclass = {'test':PyTest},
      description='Library for loading and manipulating tabular data.',
      author='Ryan Sturmer',
      author_email='ryansturmer@gmail.com',
      install_requires=['tablib'],
      tests_require=['pytest'],
      url='http://www.github.com/ryansturmer/tableview')
