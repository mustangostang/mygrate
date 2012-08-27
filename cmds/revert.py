#!/usr/bin/env python

import db.dump
from db.table import Database
import cmds.init
import repo.revision
import sys
from optparse import OptionParser

def run (args):
  """Reverts repository to its last commited state."""
  cmds.init.require_init()
  (options, args) = optargs (args)
  if not len(args):
    print "Comparing current database state to latest commited revision."
    src = Database().parseString(repo.revision.latest())
    dest = Database().parseString(db.dump.dump())
    revertSQL = str(src - dest)
    if revertSQL == '':
      print "Nothing to revert since revision #%s." % repo.revision.latest_number()
      sys.exit()
    print """Reverting to last committed revision: #%s.""" % repo.revision.latest_number()
    if not options.debug:
      db.dump.load(revertSQL)
      return
    for line in revertSQL.split("\n"):
      print line.strip() + "\n"
      print db.dump.load (line.strip())

def optargs(args):
  """Parses options for current command."""
  parser = OptionParser()
  parser.add_option("-d", "--debug", dest="debug", action="store_true", default = False,
                  help="Run revert line-by-line with debug info")
  (options, args) = parser.parse_args(args)
  return (options, args)