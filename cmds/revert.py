#!/usr/bin/env python

import db.dump
from db.table import Database
import cmds.init
import repo.revision
import sys

def run (args):
  """Reverts repository to its last commited state"""
  cmds.init.require_init()
  if not len(args):
    print "Comparing current database state to latest commited revision."
    src = Database().parseString(repo.revision.latest())
    dest = Database().parseString(db.dump.dump())
    revertSQL = str(src - dest)
    if revertSQL == '':
      print "Nothing to revert since revision #%s." % repo.revision.latest_number()
      sys.exit()
    print """Reverting to last committed revision: #%s.""" % repo.revision.latest_number()
    db.dump.load(revertSQL)
