# -*- coding: utf-8 -*-
# native
import os
from setuptools import find_packages, setup


def read(fname):
    """Utility function to read the some file.

    Args:
        fname (str): File name.
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='petrofab',
    version='0.0.1',
    author='Petr Zelenin',
    author_email='po.zelenin@gmail.com',
    license='BSD',
    description='Tasks based on Fabric for work with my project',
    packages=find_packages(),
    # long_description=read('README'),
    setup_requires=[
        'fabric',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License',
    ],
)
