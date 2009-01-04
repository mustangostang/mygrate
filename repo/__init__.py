#!/usr/bin/env python

import os
import cmds.init
from repo.configobj import ConfigObj

REPO = None

def repopath():
  global REPO
  if REPO is not None:
    return REPO
  curdir = os.path.abspath(os.path.curdir)
  while curdir != "/":
    try:
      repopath = os.path.join (curdir, cmds.init.PATH_CONF_MAIN)
      config = ConfigObj(repopath)
      if config:
        print "Repository found at %s" % curdir
        REPO = curdir
        return curdir
    except IOError:
      REPO = "."
      return "."
    curdir = os.path.realpath ("%s/../" % curdir)
  REPO = "."
  return "."
