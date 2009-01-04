#!/usr/bin/env python

import cmds.init
import db.dump
import sys
import os.path
import repo


REV_PATH = ".mygrate/store/%s.sql"
REV_PATH = os.path.join (repo.repopath(), REV_PATH)

def set_current(number):
  revisions = cmds.init.revisions()
  revisions["current"] = number
  revisions.write()  

def current():
  return latest_number()

def latest_number():
  """Returns number of latest revision."""
  revisions = cmds.init.revisions()
  return int(revisions["current"])

def latest():
  """Returns latest state of SQL saved or empty string if there are no revisions yet."""
  current = latest_number()
  if current <= 0:
   return ''
  return open (REV_PATH % current).read()
  
def by_number(rev_no):
  """Returns state of SQL saved for a given revision or raises an Exception"""
  if rev_no == "0" or rev_no == 0:
    return ""
  if int (rev_no) == 0:
    print """abort: Wrong revision number: %s""" % rev_no
    sys.exit()
  return open (REV_PATH % rev_no).read()
  
def save():
  """Increments revision number and saves current"""
  current = latest_number() + 1
  open (REV_PATH % current, 'w').write(db.dump.dump())
  set_current (current)
