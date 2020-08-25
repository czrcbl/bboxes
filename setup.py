# from distutils.core import setup
from setuptools import setup

setup(
    name='bboxes',
    license='MIT',
    author='Cézar Lemos',
    author_email='cezarcbl@pm.me',
    version='0.0.ssggcnn1',
    packages=['bboxes',],
    install_requires=['numpy', 'matplotlib', 'opencv-python'],
    description='Some utils to work with bounding boxes',
    long_description=open('README.md').read(),
)