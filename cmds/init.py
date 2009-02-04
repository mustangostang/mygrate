#!/usr/bin/env python

import os
import os.path
import sys
from repo.configobj import ConfigObj
import repo

PATH_CONF_MAIN = ".mygrate/main.conf"
PATH_REV_MAIN  = ".mygrate/revisions"

def require_init():
  if not is_initialized():
    print """abort: Repository not initialized in current directory. Run mygrate init."""
    sys.exit()

def is_initialized():
  if config():
    return True
  return False

def config():
  path = os.path.join (repo.repopath(), PATH_CONF_MAIN)
  try:
    config = ConfigObj(path)
    return config
  except IOError:
    return False
  return False
  
def revisions():
  path = os.path.join (repo.repopath(), PATH_REV_MAIN)

  try:
    config = ConfigObj(path)
    return config
  except IOError:
    return False
  return False

def run (args):
  """Initializes a mygrate repository"""
  if is_initialized():
    print """abort: Mygrate repository is already initialized in this directory"""
    sys.exit()
  try:
    os.makedirs (".mygrate/store")
  except:
    pass
  migration_dir_exists = False
  dir_default = "migrations"
  dir = dir_default
  if os.path.isdir(dir):
    migration_dir_exists = True
  if not os.path.isdir (dir_default):
    dir = raw_input ("The directory to store the migration files (default: %s): " % dir_default)
    if not dir:
      dir = dir_default
    os.mkdir (dir)
  db_host_default = "localhost"
  db_host = raw_input ("The MySQL host (default: %s): " % db_host_default)
  if not db_host:
    db_host = db_host_default
  db_user = raw_input ("The user for MySQL DB: ")
  db_pass = raw_input ("The password for %s@%s: " % (db_user, db_host))  
  db_db = raw_input ("The MySQL database name at %s: " % db_host)
  vcs   = raw_input ("Version control system you are using (svn/hg/git/?): ")
  
  mysql = "mysql"
  mysqldump = "mysqldump"
  
  config = ConfigObj(PATH_CONF_MAIN)
  config["migrations_dir"] = dir
  config["db_host"]        = db_host
  config["db_user"]        = db_user
  config["db_pass"]        = db_pass
  config["db_db"]          = db_db
  config["vcs"]            = vcs
  config["mysql"]          = mysql
  config["mysqldump"]      = mysqldump
  config.write()
  
  revisions = ConfigObj (PATH_REV_MAIN)
  revisions["current"] = "0"
  revisions.write()
  
  print """Migration repos initialized successfully."""

  if migration_dir_exists:
    import cmds.update
    cmds.update.run()
