import os
import setuptools

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setuptools.setup(
    name = "pyladspa",
    version = "0.0.1",
    author = "Peter Glushkov",
    author_email = "pglushkov@gmail.com",
    description = "Python implementation of utilities from LADSPA SDK",
    license = "MIT",
    keywords = "LADSPA audio audio-plugins",
    url = "https://github.com/pglushkov/pyladspa",
    long_description=read('README.md'),
    classifiers=[
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points = {
        'console_scripts': ['listplugins=pyladspa.listplugins:main_cli'],
    },
    packages=setuptools.find_packages()
)