#!/usr/bin/env python

import db.dump
from db.table import Database
import cmds.init

def run (args):
  """Reverts repository to its last commited state"""
  cmds.init.require_init()
  if not len(args):
    print "Comparing current version to latest commited revision."
    src = Database().parseString(repo.revision.latest())
    dest = Database().parseString(db.dump.dump())
    revertSQL = str(src - dest)
    db.dump.load(revertSQL)
