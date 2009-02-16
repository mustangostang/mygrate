import os.path
#!/usr/bin/env python

import os
import cmds.init
from repo.configobj import ConfigObj

REPO = None

def repopath():
  """Determines path to actual repository by scanning upper level directories.
  After being run once, stores repo info in REPO."""
  global REPO
  if REPO is not None:
    return REPO
  curdir = os.path.abspath(os.path.curdir)
  while os.path.splitdrive(curdir)[1] != os.sep:
    try:
      repopath = os.path.join (curdir, cmds.init.PATH_CONF_MAIN)
      config = ConfigObj(repopath)
      if config:
        REPO = curdir
        return curdir
    except IOError:
      REPO = "."
      return "."
    curdir = os.path.realpath ("%s/../" % curdir)
  REPO = "."
  return "."
