#!/usr/bin/env python

import db.dump
from db.table import Database
import sys
import repo
import repo.revision
import repo.migration
import cmds.init

def run (args):
  """Commits current repository changes."""
  cmds.init.require_init()
  repo.allow_if_at_tip()
  try:
    message = args[0]
  except IndexError:
    print """== No message specified. Using the following message to commit: ==\n"""
    message = auto_commit_message()
    print message
  print "Commiting current changes."
  
  src = Database().parseString(repo.revision.latest())
  dest = Database().parseString(db.dump.dump())
  
  if src == dest:
    print """No changes, nothing to commit."""
    sys.exit()
  
  number = repo.revision.latest_number() + 1
  repo.migration.add (number, dest - src, src - dest, message)
  repo.revision.save()
    
  print """Migration #%s successfully created.""" % number
  
  if cmds.init.config()["vcs"] == "hg":
    add_to_hg (number)
  
  
def add_to_hg (number):
  Migration = repo.migration.Migration (number)
  Migration.add_to_hg()
  
def auto_commit_message():
  Diff = Database().parseString(db.dump.dump()) - Database().parseString(repo.revision.latest())
  CommitMsg = []
  for tbl in Diff.TablesAdded:
    CommitMsg.append ("Added `%s`" % tbl.name)
  for tbl in Diff.TablesDropped:
    CommitMsg.append ("Dropped `%s`" % tbl.name)
  for (tbl, dstTable) in Diff.TablesModified:
    CommitMsg.append ("Modified `%s`:" % tbl.name)
    diffSt = dstTable - tbl
    for (field, prev) in diffSt.FieldsAdded:
      CommitMsg.append ("  + added `%s`" % field.name)
    for field in diffSt.FieldsDropped:
      CommitMsg.append ("  - dropped `%s`" % field.name)
    for field in diffSt.FieldsModified:
      CommitMsg.append ("    modified `%s` to %s%s" % (field.name, field.type, "(%s)" % field.options if field.options else ""))
  return "\n".join (CommitMsg)
