#!/usr/bin/env python

import db.dump
from db.table import Database
import repo.history
import cmds.init
import sys
from optparse import OptionParser

def run (args):
  """Show all changes of repository."""
  cmds.init.require_init()
  (options, args) = optargs (args)
  History = repo.history.load()
  print History

def optargs(args):
  """Parses options for current command."""
  parser = OptionParser()
  parser.add_option("-r", "--rev", dest="revision",
                  help="Start from revision number")
  (options, args) = parser.parse_args(args)
  return (options, args)

