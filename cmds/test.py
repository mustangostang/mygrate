#!/usr/bin/env python

import db.dump
from db.table import Database
import sys
import repo.revision
import cmds.init

def run (args):
  """Test current repository changes"""
  cmds.init.require_init()
  print "Testing current changes."
  src = Database().parseString(repo.revision.latest())
  dest =  Database().parseString(db.dump.dump())
  
  restore = db.dump.restore_point()
  
  if src == dest:
    print """No changes, nothing to test."""
    sys.exit()
    
  testUp = str(dest - src)
  testDown = str(src - dest)
  
  print """Downgrading..."""
  out = db.dump.load (testDown)
  print """MySQL said: %s""" % out
  
  print """Upgrading..."""
  out = db.dump.load (testUp)
  print """MySQL said: %s""" % out
  
  newState = Database().parseString(db.dump.dump())
  if newState == dest:
    print """DB is stable, changes are ready for migration."""
    sys.exit()
    
  print """There were unexpected changes:"""
  print newState - dest
  print """Attempting automatic restore"""
  out = db.dump.load (restore)
  print """MySQL said: %s""" % out
