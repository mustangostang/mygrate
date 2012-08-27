#!/usr/bin/env python

class SQLLoadError (Exception):
  """Raised when there is an error in loading SQL code"""
  def __init__ (self, sql, errors):
    self.sql = sql
    self.errors = errors
  def __str__ (self):
    return """MySQL encountered the following error:

%s""" % self.errors

class MigrationFailedError (Exception):
  """Raised when migration has failed"""
  def __init__ (self, migration_number):
    self.migration_number = migration_number
  def __str__ (self):
    return """Migration #%s failed.""" % self.migration_number