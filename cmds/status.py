#!/usr/bin/env python

import db.dump
from db.table import Database
import repo.revision
import cmds.init
import sys
from optparse import OptionParser

def run (args):
  """Show changed tables since latest commit."""
  cmds.init.require_init()

  (options, args) = optargs (args)

  revision = repo.revision.latest_number() if not options.revision else int(options.revision)

  src = Database().parseString(repo.revision.by_number(revision))
  dest = Database().parseString(db.dump.dump())
  if src == dest:
    print """No changes since revision %s.""" % (revision)
    sys.exit()
  Diff = dest - src
  Status = { }
  Info = { }
  
  for tbl in Diff.TablesAdded:
    Status[tbl.name] = "A"
  for tbl in Diff.TablesDropped:
    Status[tbl.name] = "R"
  for (tbl, dstTable) in Diff.TablesModified:
    Status[tbl.name] = "M"
    if dstTable > tbl:
      Status[tbl.name] = "M+"
    if dstTable < tbl:
      Status[tbl.name] = "M-"
    diffSt = dstTable - tbl
    Info[tbl.name] = { }
    for (field, prev) in diffSt.FieldsAdded:
      Info[tbl.name][field.name] = "+"
    for field in diffSt.FieldsDropped:
      Info[tbl.name][field.name] = "-"
    for field in diffSt.FieldsModified:
      Info[tbl.name][field.name] = "m"
     
    
  for tbl in sorted(Status.keys()):
    print " %s %s" % (Status[tbl].ljust (2, " "), tbl)
    if not tbl in Info.keys():
      continue
    for info in Info[tbl].keys():
      print "    %s %s" % (Info[tbl][info], info)

def optargs(args):
  """Parses options for current command."""
  parser = OptionParser()
  parser.add_option("-r", "--rev", dest="revision",
                  help="Revision to compare current status to")
  (options, args) = parser.parse_args(args)
  return (options, args)

