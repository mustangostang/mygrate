#!/usr/bin/env python

import cmds.init
import repo.revision
import sys
import repo.migration

def run (args):
  """Rolls back last commit"""
  cmds.init.require_init()
  if not repo.revision.latest():
    print "There are no commits yet."
    sys.exit()
  current = repo.revision.current()
  Migration = repo.migration.Migration (current)
  Migration.delete()
  repo.revision.set_current(current - 1)
  print "Rolled back migration #%s." % current
  if cmds.init.config()["vcs"] == "hg":
    Migration.remove_from_hg()
