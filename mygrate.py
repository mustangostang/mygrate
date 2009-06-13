#!/usr/bin/env python

import sys
import cmds
import os

Aliases = { }

for cmd in cmds.__all__:
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
    if command in cmds.__all__:
      module = "cmds.%s" % command
      __import__ (module)
      sys.modules[module].run(args)
  except IndexError:
    if command:
      print """Unknown command: %s""" % command
    print """Mygrate - MySQL Sexy Migration Tool\n"""
    print """Available commands are:\n"""
    
    for cmd in sorted(cmds.__all__):
      if cmd in ['checkout']: continue
      module = "cmds.%s" % cmd
      __import__ (module)
      print " %s %s" % (cmd.ljust(10, ' '), sys.modules[module].run.__doc__)

    print
    sys.exit()