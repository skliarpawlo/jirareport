#!/usr/bin/env python

from distutils.core import setup


with open("README.md", "r") as f:
    long_description = f.read()

setup(name='Jira Report',
      version='0.1',
      description='Tiny tool for making jira monthly reports + some additional features',
      long_description=long_description,
      license="MIT",
      author='skliarpawlo',
      author_email='skliarpawlo@gmail.com',
      keywords = "jira report",
      url = "https://github.com/skliarpawlo/jirareport",
      packages=['jirareport', 'jirareport.utils', 'jirareport.utils.presenters'],
      scripts=['make.py'],
)