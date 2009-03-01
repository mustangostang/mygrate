#!/usr/bin/env python

import repo
import repo.revision
import repo.migration
import cmds.init
import db.dump
from db import MigrationFailedError
from optparse import OptionParser

def run (args = []):
  """Updates database to given revision"""
  cmds.init.require_init()
  (options, args) = optargs (args)
  try:
    revision = int(args[0])
  except IndexError:
    revision = repo.migration.latest_number()

  current = repo.revision.current()
  if current == revision and not options.abandon_current:
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

  if outstanding_changes and not options.abandon_current:
    print """Reapplying outstanding changes."""
    db.dump.load (apply_after_update)

def optargs(args):
  """Parses options for current command."""
  parser = OptionParser()
  parser.add_option("", "--abandon", dest="abandon_current", default=False, action="store_true",
                  help="Abandon outstanding changes when updating to migration")
  (options, args) = parser.parse_args(args)
  return (options, args)