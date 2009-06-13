#!/usr/bin/env python

import cmds.init
import db.dump
import sys
import cPickle
import repo.migration
import os.path
import repo

HISTORY_PATH = ".mygrate/store/history"
HISTORY_PATH = os.path.join (repo.repopath(), HISTORY_PATH)

def load():
  return History()

def refresh():
  History().get_fresh_from_migrations().save()

class History:
  def __init__ (self):
    try:
      self.History = cPickle.load(open(HISTORY_PATH))
    except:
      self.get_fresh_from_migrations().save()
      self.History = cPickle.load(open(HISTORY_PATH))
      
  def save (self):
    cPickle.dump (self.History, open(HISTORY_PATH, 'w'))
    
  def get_fresh_from_migrations (self):
    self.History = { }
    for migration_number in repo.migration.all():
      self.History[migration_number] = repo.migration.Migration (migration_number)
    return self
  
  def __str__ (self):
    return self.out ()
  
  def tip (self):
    return self.out (min = max(self.History.keys()))
  
  def out(self, max = None, min = 0):
    Out = []
    for k in reversed(sorted(self.History.keys())):
      if k < min: continue
      if max and k > max: continue
      Migration = self.History[k]
      Out.append("""changeset:   %s\nuser:        %s\ndate:        %s\nsummary:     %s""" % (k, Migration.author, Migration.date, Migration.message))
    return "\n\n".join (Out) + "\n"

  
  def row_format (migration):
    newrow = { }
    newrow["no"] = migration["number"]
    newrow['user'] = row["user"]
    newrow["summary"] = row["summary"]
    newrow["date"] = row["date"]
    return newrow
