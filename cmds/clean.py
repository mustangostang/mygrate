#!/usr/bin/env python

import cmds.init
import repo
import utils

def run (args):
  """Removes all Mygrate data (cancels mygrate init)."""
  cmds.init.require_init()
  path = repo.repopath() + '/.mygrate'
  print "Removing everything under %s." % path
  utils.shell ('rm -rf %s' % path)
  print "Mygrate repo successfully removed. Use mygrate init to reinitialize it."