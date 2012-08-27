#!/usr/bin/env python

import repo.history
import cmds.init
from optparse import OptionParser

def run (args):
  """Show all changes inside a repository."""
  cmds.init.require_init()
  (options, args) = optargs (args)
  History = repo.history.load()
  if not options.revision:
    print History.out (reversing = options.backwards)
    return
  revs = [int(r) for r in options.revision.split (':')]
  if len (revs) > 2:
    revs = revs[:2]
  if len (revs) == 1:
    print History.out (revision_from = revs[0], revision_to = revs[0])
    return
  print History.out (revision_from = revs[0], revision_to = revs[1], reversing = options.backwards)

def optargs(args):
  """Parses options for current command."""
  parser = OptionParser()
  parser.add_option("-r", "--rev", dest="revision",
                  help="Revision number or range")
  parser.add_option("-b", "--backwards", dest="backwards", default=False, action="store_true",
                  help="Revision number or range")
  (options, args) = parser.parse_args(args)
  return (options, args)

