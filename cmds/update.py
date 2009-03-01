#!/usr/bin/env python

import repo
import repo.revision
import repo.migration
import cmds.init
import db.dump
from db import MigrationFailedError

def run (args = []):
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

  outstanding_changes = repo.has_outstanding_changes()
  if outstanding_changes:
    apply_after_update = repo.outstanding_changes()
    print """Undoing outstanding changes."""
    db.dump.load (repo.outstanding_changes(undo = True))
  
  if revision < current:
    # Downgrading
    while current > revision:
      try:
        Migration = repo.migration.Migration (current)
        print """Downgrading migration #%s: %s.""" % (current, Migration.message)
        Migration.down()
        current = current - 1
        repo.revision.set_current (current)
      except MigrationFailedError:
        break
    print """Updated to revision #%s.""" % repo.revision.current()
    
  else:
    # Upgrading
    while current < revision:
      try:
        current = current + 1
        Migration = repo.migration.Migration (current)
        print """Upgrading migration #%s: %s.""" % (current, Migration.message)
        Migration.up()
        repo.revision.save_to_file(current)
        repo.revision.set_current (current)
      except MigrationFailedError:
        break
    print """Updated to revision #%s.""" % repo.revision.current()

  if outstanding_changes:
    print """Reapplying outstanding changes."""
    db.dump.load (apply_after_update)
