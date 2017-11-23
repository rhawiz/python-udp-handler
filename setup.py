import os

from setuptools import setup


def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read()


def readlines(f):
    return open(os.path.join(os.path.dirname(__file__), f)).readlines()


setup(
    name="python-udp-handler",
    version="0.1",
    include_package_data=True,
    author="Rawand Hawiz",
    author_email="rhawiz@geophy.com",
    description="UDP Handler for logging to logstash.",
    license="BSD",
    keywords="python udp handler logging",
    url="https://github.com/rhawiz/python-udp-handler",
    packages=['logmodule'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=[
    ]

)
