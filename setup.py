try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = [
    'description': 'OOP Excercise',
    'author': 'Saurabh B',
    'author_email': 'saurabhbansod1992@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['bank'],
    'scripts': [],
    'name': 'OOPExcercise'
]