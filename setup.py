import os
from setuptools import setup


setup(
    name='hg-number',
    version='0.0.3',
    description='a python script that allows you to use numbers instead of file names in mercurial commands',
    url='https://github.com/gsingh93/hg-number',
    author='Gulshan Singh',
    author_email='gsingh2011@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='hg mercurial vcs',
    py_modules=['hg_number'],
    install_requires=['termcolor'],
    entry_points={
        'console_scripts': [
            'hg-number=hg_number:main',
        ]
    },
)
