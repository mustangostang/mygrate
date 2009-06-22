#!/usr/bin/env python

from subprocess import Popen, PIPE
import os
import datetime
import cmds.init




def restore_point():
  config = cmds.init.config()
  user     = config["db_user"]
  password = config["db_pass"]
  db       = config["db_db"]

  return mysql_command ("-u%s %s%s --default-character-set=utf8 %s" % (user, "-p" if password else "", password, db))

def dump():
  config = cmds.init.config()
  user     = config["db_user"]
  password = config["db_pass"]
  db       = config["db_db"]

  return mysqldump_command ("--no-data --compact -u%s %s%s --default-character-set=utf8 %s" % (user, "-p" if password else "", password, db))

def load (sql):
  config = cmds.init.config()
  user     = config["db_user"]
  password = config["db_pass"]
  db       = config["db_db"]

  tempfile = ".temp-mygrate-%s" % str(datetime.time()).replace (':', '_')
  f = open (tempfile, 'w')
  f.write (sql)
  f.close()
  
  output = mysql_command ("-u%s %s%s --default-character-set=utf8 %s < %s" % (user, "-p" if password else "", password, db, tempfile))
  os.unlink(tempfile)
  return output
  
def mysql_command (cmd):
  config = cmds.init.config()
  mysql_path = config["mysql"] if "mysql" in config else "mysql"
  return Popen("%s %s" % (mysql_path, cmd), shell=True, stdout=PIPE).stdout.read()
  
def mysqldump_command (cmd):
  config = cmds.init.config()
  mysqldump_path = config["mysqldump"] if "mysqldump" in config else "mysqldump"
  return Popen("%s %s" % (mysqldump_path, cmd), shell=True, stdout=PIPE).stdout.read() 
