from distutils.core import setup

setup(
    name='bboxes',
    version='0.1dev',
    packages=['bboxes',],
    install_requires=['numpy', 'matplotlib', 'opencv-python'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    description='Some utils to work with bounding boxes',
    long_description=open('README.md').read(),
)