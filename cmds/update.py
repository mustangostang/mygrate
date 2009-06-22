#!/usr/bin/env python

import db.dump
from db.table import Database
import sys
import repo.revision
import repo.migration
import cmds.init

def run (args):
  """Updates database to given revision"""
  cmds.init.require_init()
  try:
    revision = int(args[0])
  except IndexError:
    revision = repo.migration.latest_number()

  current = repo.revision.current()
  if current == revision:
    print """Nothing to update."""
    return

  print """Updating to migration #%s.""" % revision
  
  if revision < current:
    # Downgrading
    while current > revision:
      Migration = repo.migration.Migration (current)
      print """Downgrading migration #%s: %s.""" % (current, Migration.message)
      Migration.down()
      current = current - 1
      repo.revision.set_current (current)
    print """Updated to revision #%s.""" % current
    return
    
  if revision > current:
    # Upgrading
    while current < revision:
      current = current + 1
      Migration = repo.migration.Migration (current)
      print """Upgrading migration #%s: %s.""" % (current, Migration.message)
      Migration.up()
      repo.revision.save_to_file(current)
      repo.revision.set_current (current)
    print """Updated to revision #%s.""" % current
