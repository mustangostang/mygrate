#!/usr/bin/env python

import db.dump
from db.table import Database
import repo.revision
import cmds.init
from optparse import OptionParser


def run (args):
  """Compares current repository state to a revision."""
  cmds.init.require_init()
  
  (options, args) = optargs (args)
  reverse = options.backwards
  revision = repo.revision.latest_number() if not options.revision else int(options.revision)
  if not reverse:
    print "Comparing database state to revision %s." % revision
  else:
    print "Reverse comparing revision %s to database state." % revision
  src = Database().parseString(repo.revision.by_number(revision))
  dest = Database().parseString(db.dump.dump())
  if src == dest:
    print """No changes since revision %s.""" % revision
  else:
    if not reverse:
      print dest - src
    else:
      print src - dest
      
def optargs(args):
  """Parses options for current command."""
  parser = OptionParser()
  parser.add_option("-r", "--rev", dest="revision",
                  help="Revision to compare current status to")
  parser.add_option("-b", "--backwards", dest="backwards", default=False, action="store_true",
                  help="Compare revisions backwards")
  (options, args) = parser.parse_args(args)
  return (options, args)

