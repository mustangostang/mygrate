class DatabaseDiff:
  def __init__ (self):
    self.TablesAdded = []
    self.TablesDropped = []
    self.TablesModified = []
    
  def compare (self, src, dest):
    for table in src.tables:
      if not dest.tableExists (table):
        self.TablesDropped.append(table)
        continue
      if dest.table (table.name) != table:
        self.TablesModified.append ((table, dest.table (table.name)))
      
    for table in dest.tables:
      if not src.tableExists (table):
        self.TablesAdded.append(table)
        
    return self

  def __str__ (self):
    out = []
    for table in self.TablesAdded:
      out.append(str(table))
    for table in self.TablesDropped:
      out.append(table.removeSQL())
    for (srctable, desttable) in self.TablesModified:
      out.append(str(desttable - srctable))
    return "\n".join (out)

class TableDiff:
  def __init__ (self):
    self.name = ''
    self.FieldsAdded = []
    self.FieldsDropped = []
    self.FieldsModified = []
    self.IndexesAdded = []
    self.IndexesDropped = []
    self.IndexesModified = []
    self.PrimaryKeyAdded = False
    self.PrimaryKeyDropped = False
    self.PrimaryKeyModified = False
    self.OptionsAdded = []
    self.OptionsDropped = []
    self.OptionsModified = []
    
  def compare (self, src, dest):
    self.name = src.name
   
    # Fields
    for field in src.Fields:
      if not dest.fieldExists (field):
        self.FieldsDropped.append(field)
        continue
      if dest.field (field.name) != field:
        self.FieldsModified.append (dest.field (field.name))
    prev = None
    for field in dest.Fields:
      if not src.fieldExists (field):
        self.FieldsAdded.append((field, prev))
      prev = field.name
    
    # Indexes        
    for index in src.Indexes:
      if not dest.indexExists (index):
        self.IndexesDropped.append (index)
        continue
      if dest.index (index.name) != index:
        self.IndexesModified.append (dest.index (index.name))
    for index in dest.Indexes:
      if not src.indexExists (index):
        self.IndexesAdded.append(index)
       
        
    return self
  
  def __str__ (self):
    out = []
    
    # Dropping indexes should go first.
    for index in self.IndexesDropped:
      out.append ("""ALTER TABLE `%s` DROP INDEX `%s`;""" % (self.name, index.name))   

    
    for field in self.FieldsDropped:
      out.append ("""ALTER TABLE `%s` DROP `%s`;""" % (self.name, field.name))
    for field in self.FieldsModified:
      out.append ("""ALTER TABLE `%s` CHANGE `%s` %s;""" % (self.name, field.name, field))
    for (field, prev) in self.FieldsAdded:
      out.append ("""ALTER TABLE `%s` ADD %s%s;""" % (self.name, field, " FIRST" if prev is None else " AFTER `%s`" % prev))

    for index in self.IndexesModified:
      out.append ("""ALTER TABLE `%s` DROP INDEX `%s`
ADD %s;""" % (self.name, index.name, index.forAlteration()))
    for index in self.IndexesAdded:
      out.append ("""ALTER TABLE `%s` ADD %s;""" % (self.name, index.forAlteration()))

      
    # return """Added: %s, Modified: %s, Dropped: %s""" % (self.FieldsAdded, self.FieldsModified, self.FieldsDropped)
    return "\n".join (out)
    
