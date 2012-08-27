#!/usr/bin/env python

import db.dump
import cmds.init
import db

def run (args):
  """Imports a SQL file to the database."""
  cmds.init.require_init()
  if not len(args):
    print "Specify an SQL file to run."
  file = args[0]
  try:
    sql = open(file, 'rb').read()
  except IOError:
    print "Can't find file: %s" % file
    return
  try:
    db.dump.load(sql)
    print """SQL file imported. You can `commit` or `revert`."""
  except db.SQLLoadError, e:
    print "Can't import file: %s." % file
    print e
    
    
