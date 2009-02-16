import os.path
#!/usr/bin/env python

import os
import cmds.init
import sys
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

def not_at_tip():
  """Returns True if repo is not currently at tip migration"""
  import repo.migration
  import repo.revision
  latest = repo.migration.latest_number()
  current = repo.revision.current()
  return (current == latest, latest, current)

def allow_if_at_tip():
  """Returns a warning message and exists if repo is not at tip"""
  (at_tip, tip, current) = not_at_tip()
  if (at_tip): return True
  print """Repository is currently not at tip (currently at #%s, tip is #%s).
Run `mygrate up`.""" % (current, tip)
  sys.exit()