import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "dmr5200",
    version = "0.0.1",
    author = "Andrew MacIsaac",
    author_email = "macisaac.andrew@gmail.com",
    description = ("A small library and utility to read data from a Circuit-Test DMR-5200 multimeter."),
    license = "BSD",
    keywords = "electronics serial meter",
    url = "https://github.com/awm/dmr5200",
    py_modules=['dmr5200'],
    packages=['scripts'],
    scripts=['scripts/dmr5200'],
    requires=['pyserial'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
