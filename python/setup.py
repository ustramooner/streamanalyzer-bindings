#!/usr/bin/env python

"""
setup.py file for strigi bindings
"""

from distutils.core import setup, Extension

streamanalyzer_module = Extension('_streamanalyzer',
                                  sources=['strigiPYTHON_wrap.cxx'],
                                  libraries = ['streams', 'streamanalyzer'],
                                  include_dirs= ['include']
                                 )

setup(
    name='python-streamanalyzer',
    version='0.1',
    author      = "Ben van Klinken",
    author_email= "ustramooner@users.sourceforge.net",
    description="Python bindings to Strigi's libanalyzer libraries",
    license='GPLv2',
    long_description="""
    StreamAnalyzer is a wrapper around Strigi's libanalyzer libraries.
    StreamAnalyzer exposes Strigi's capabilities for extracting meta data (such as the length of an audio clip or the resolution of a picture) 
    and full text of documents and from within archives (zips, tarballs, etc).
    Strigi's goals are to be fast, use a small amount of RAM. 
    """,
    ext_modules = [streamanalyzer_module],
    py_modules = ["streamanalyzer"],
    url='http://strigi.sourceforge.net',
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

