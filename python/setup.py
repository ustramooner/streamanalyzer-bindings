#!/usr/bin/env python

from setuptools import setup, find_packages, Extension

streamanalyzer_module = Extension('_streamanalyzer',
                                  sources=['strigiPYTHON_wrap.cxx'],
                                  depends=['strigiPYTHON_wrap.h'],
                                  libraries = ['streams', 'streamanalyzer'],
                                  include_dirs=['.'],
                                 )

setup(
    name='python-streamanalyzer',
    version='0.1',
    description="Python bindings to Strigi's libanalyzer libraries",
    author='Ben van Klinken',
    author_email='ustramooner@users.sourceforge.net',
    url='http://strigi.sourceforge.net',
    license='GPLv2',
    packages=['.'],
    script_name = 'strigiPYTHON_wrap.h',
    ext_modules = [streamanalyzer_module],
    long_description="""
    StreamAnalyzer is a wrapper around Strigi's libanalyzer libraries.
    StreamAnalyzer exposes Strigi's capabilities for extracting meta data (such as the length of an audio clip or the resolution of a picture) 
    and full text of documents and from within archives (zips, tarballs, etc).
    Strigi's goals are to be fast, use a small amount of RAM. 
    """,
    classifiers=[
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: GPLv2 License",
    "Environment :: Console",
    "Environment :: Web Environment",
    "Programming Language :: Python",
    "Operating System :: POSIX",
    "Topic :: Internet",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Intended Audience :: Developers",
    ]
)

