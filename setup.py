# from distutils.core import setup
from setuptools import setup

setup(
    name='bboxes',
    author='Cézar Bieniek Lemos',
    author_email="cezarcbl@pm.me",
    license="MIT",
    version='0.0.1',
    packages=['bboxes',],
    install_requires=['numpy', 'matplotlib', 'opencv-python'],
    description='Some utils to work with bounding boxes',
    long_description=open('README.md').read(),
)