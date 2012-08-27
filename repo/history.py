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
    self.History = { }
    try:
      self.History = cPickle.load(open(HISTORY_PATH))
      current_history = self.History
      self.get_fresh_from_migrations()
      if current_history != self.History:
        self.save()
    except:
      pass
      
  def save (self):
    cPickle.dump (self.History, open(HISTORY_PATH, 'w'))
    
  def get_fresh_from_migrations (self, force_refresh = False):
    for migration_number in repo.migration.all():
      if not force_refresh and self.History.has_key (migration_number):
        continue
      self.History[migration_number] = repo.migration.Migration (migration_number)
      del (self.History[migration_number].state_to_rollback)
    return self
  
  def __str__ (self):
    return self.out ()
  
  def tip (self):
    return self.out (revision_from = max(self.History.keys()))
  
  def out(self, revision_to = None, revision_from = 0, reversing = False):
    Out = []
    iterlist = sorted(self.History.keys())
    if revision_to is None:
      revision_to = max(self.History.keys())
    if revision_to < revision_from:
      (revision_to, revision_from) = (revision_from, revision_to)
      reversing = not reversing
    iterlist = [v for (k, v) in enumerate(iterlist) if v >= revision_from and v <= revision_to]
    if reversing:
      iterlist = reversed (iterlist)
    for k in iterlist:
      Migration = self.History[k]
      Out.append("""changeset:   %s\nuser:        %s\ndate:        %s\nsummary:     %s""" % (Migration.number, Migration.author, Migration.date, Migration.message))
    return "\n\n".join (Out) + "\n"

  
  def row_format (migration):
    newrow = { }
    newrow["no"] = migration["number"]
    newrow['user'] = row["user"]
    newrow["summary"] = row["summary"]
    newrow["date"] = row["date"]
    return newrow
