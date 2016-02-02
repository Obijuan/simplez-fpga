#!/usr/bin/env python3

from setuptools import setup

import toolchain_simplez

setup(name='toolchain-simplez',
      version=toolchain_simplez.__version__,
      description=toolchain_simplez.__doc__,
      author=toolchain_simplez.__author__,
      author_email=toolchain_simplez.__email__,
      url='https://github.com/Obijuan/simplez-fpga',
      download_url='https://pypi.python.org/pypi/toolchain-simplez',
      license=toolchain_simplez.__license__,
      py_modules=['toolchain_simplez', 'sasm', 'sreset', 'sboot', 'vmem',
                  'consola_io', 'ssim'],
      entry_points={'console_scripts': ['sasm=sasm:main',
                                        'sreset=sreset:main',
                                        'sboot=sboot:main']},
      install_requires=['pyserial', 'ply'],
      classifiers=[
          'Development Status :: 1 - Planning',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
          'Programming Language :: Python :: 3.4'
      ])
