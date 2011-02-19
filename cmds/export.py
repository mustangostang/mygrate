#!/usr/bin/env python

import cmds.init
import repo
import utils
from optparse import OptionParser
from db.table import Database
import db.dump

def run (args):
  """Exports data"""
  cmds.init.require_init()
  (options, args) = optargs (args)
  current = Database().parseString(db.dump.dump())
  table = current.table(options.table)
  format = options.format or "json"
  if format == "model":
    as_model(table)
  
def as_model (Table):
  fields = [f.name for f in Table.Fields]
  print """<?php

class %s extends ZFast_Model_goDB {

  public $class = __CLASS__;
  public $View;

  public %s;

  const ON_PAGE = 10; const TABLE = '%s';
  const PRIMARY = 'id'; const ORDER_BY = '`id` DESC';

  public function setupFields() {
%s
  } """ % (Table.name, ", ".join (["$%s" % f for f in fields]), Table.name, 
    "\n".join(["      $this->addField ('%s');" % f for f in fields[1:]])
  )
  print """
  /**
   * @param int $id
   */
  public static function byId($id) {
    return parent::byId(__CLASS__, $id);
  }
  
}"""
  
def optargs(args):
  """Parses options for current command."""
  parser = OptionParser()
  parser.add_option("-t", "--table", dest="table",
                  help="Table to export")
  parser.add_option("-f", "--format", dest="format",
                  help="Format to export (available: json)")
                  
  (options, args) = parser.parse_args(args)
  return (options, args)