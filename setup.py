#!/usr/bin/env python

from distutils.core import setup
setup(name=u'Jira Report',
      version=u'0.1',
      description=u'',
      author=u'skliarpawlo',
      author_email=u'skliarpawlo@gmail.com',
      packages=['jirareport', 'jirareport.utils', 'jirareport.utils.presenters'],
      scripts=['make.py'],
)