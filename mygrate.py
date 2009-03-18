#!/usr/bin/env python

import sys
import cmds
from cmds import *
import os


Commands = {
  'diff': cmds.diff.run,
  'revert': cmds.revert.run,
  'init': cmds.init.run,
  'commit': cmds.commit.run,
  'test': cmds.test.run,
  'update': cmds.update.run,
  'checkout': cmds.update.run,
  'status': cmds.status.run,
  'log': cmds.log.run,
  'tip': cmds.tip.run,
  'rollback': cmds.rollback.run,
}

Aliases = { }

for cmd in Commands.keys():
  for alias in [cmd[:i+1] for i in range(len(cmd) - 1)]:
    Aliases[alias] = Aliases[alias] + [cmd] if (alias in Aliases) else [cmd]

Aliases['ci'] = ["commit"]
Aliases['co'] = ["update"]

if __name__ == '__main__':
  # print os.getcwd()
  command = ""
  try:
    command = sys.argv[1]
    try:
      args = sys.argv[2:]
    except IndexError:
      args = []
    if command in Aliases.keys():
      if len (Aliases[command]) > 1:
        print """Mygrate: command '%s' is ambiguous: \n         %s""" % (command, " ".join (Aliases[command]))
        sys.exit()
      [command] = Aliases[command]
    if Commands[command]:
      Commands[command](args)
  except IndexError:
    print """Unknown command: %s""" % command
    print """Mygrate - MySQL Sexy Migration Tool\n"""
    print """Available commands are:\n"""
    
    for cmd in sorted(Commands.keys()):
      if cmd in ['checkout']: continue
      print " %s %s" % (cmd.ljust(10, ' '), Commands[cmd].__doc__)

    print
    sys.exit()