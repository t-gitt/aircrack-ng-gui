from setuptools import setup

setup(name='aircrack-ng-gui',
    version='1.0',
    author='Taher Alkamel',
    author_email='taheralkamel@gmail.com',
    description='A GUI for aircrack-ng',
    url='https://github.com/tqk-gh/aircrack-ng-gui',
    license='GNU General Public License v3.0',
    scripts=["build/lib/aircrack-ng-gui/aircrack-ng-gui.py"],
    packages=['aircrack-ng-gui'],
      install_requires=[
          'pygobject',
      ],
    dependency_links=['https://github.com/aircrack-ng/aircrack-ng'])
