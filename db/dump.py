#!/usr/bin/env python

from subprocess import Popen, PIPE
import os
import datetime
import cmds.init
from db import SQLLoadError

def prop_or_null(key, prefix = '', default_null = ''):
  config = cmds.init.config()
  c = config.get(key, False)
  if not c or c == default_null: return ""
  return prefix + c

def connect_credentials():
  config = cmds.init.config()
  user     = config["db_user"]
  return "-u%s %s %s %s %s" % (user, prop_or_null('db_pass', "-p"), prop_or_null('db_host', "-h", 'localhost'), prop_or_null('port', "--port="), prop_or_null('socket', "--socket="))

def restore_point():
  config = cmds.init.config()
  return mysqldump_command ("%s --add-drop-table --default-character-set=utf8 %s" % (connect_credentials(), config["db_db"]))

def dump():
  config = cmds.init.config()
  return mysqldump_command ("--no-data --add-lock=false --compact %s --default-character-set=utf8 %s" % (connect_credentials(), config["db_db"]))

def load (sql):
  config = cmds.init.config()
  tempfile = ".temp-mygrate-%s" % str(datetime.time()).replace (':', '_')
  f = open (tempfile, 'w')
  f.write (sql)
  f.close()
  
  (output, errors) = mysql_command ("%s --default-character-set=utf8 %s < %s" % (connect_credentials(), db, tempfile))
  os.unlink(tempfile)
  if errors:
    raise SQLLoadError (sql = sql, errors = errors)
  return True
  
def mysql_command (cmd):
  config = cmds.init.config()
  mysql_path = config["mysql"] if "mysql" in config else "mysql"
  process = Popen("%s %s" % (mysql_path, cmd), shell=True, stdout=PIPE, stderr=PIPE)
  out = process.stdout.read()
  err = process.stderr.read()
  return (out, err)
  
def mysqldump_command (cmd):
  config = cmds.init.config()
  mysqldump_path = config["mysqldump"] if "mysqldump" in config else "mysqldump"
  process = Popen("%s %s" % (mysqldump_path, cmd), shell=True, stdout=PIPE)
  out = process.stdout.read()
  return out
