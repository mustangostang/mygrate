#!/usr/bin/env python

import db.dump
from db.table import Database
import sys
import repo.revision
import repo.migration
import cmds.init
from subprocess import Popen, PIPE

def run (args):
  """Commits current repository changes to file"""
  cmds.init.require_init()
  try:
    message = args[0]
  except IndexError:
    print """Correct usage: mygrate commit "message to commit" """
    sys.exit()
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
  print """Adding migration to Mercurial..."""
  output = "hg add %s" % (Migration.filename)
  output = Popen(output, shell=True, stdout=PIPE).stdout.read()
  print output
