import string
#!/usr/bin/env python
import re
import alter

def parsefile (file):
  DB = Database (file)
  print DB

class Database:
  def __init__ (self):
    self.tables = []
    self.__tableNames = []

  def __sub__ (self, other):
    return alter.DatabaseDiff().compare(other, self)

  def __eq__ (self, other):
    return not (self != other)

  def __ne__ (self, other):
    if len(str(self - other)) > 0:
      return True
    return False

  def parseFile (self, file):
    try:
      string = open (file, 'r').read()
    except IOError:
      print "Can't open file %s." % file
      sys.exit()
    return self.parseString (string)

  def parseString (self, string):
    """Parses a file and returns an instance of Database."""
    string = string.replace("\r\n", "\n");
    return self.parseLines(string.splitlines(True))

  def parseLines (self, Lines):
    Lines = [line for line in Lines if not line.startswith("SET ") and not line.startswith ("--") and not line == "\n"]
    TableData = []
    table = []
    for line in Lines:
      table.append (line)
      # @type line str
      if line.endswith(";\n"):
        TableData.append (table)
        table = []
    Tables = [Table(table) for table in TableData]
    self.tables = Tables
    self.__tableNames = [table.name for table in self.tables]
    return self

  def table (self, name):
    if not name in self.__tableNames:
      return None
    return self.tables[self.__tableNames.index(name)]

  def tableExists (self, Table):
    if Table.name in self.__tableNames:
      return True
    return False

    return self

  def __str__ (self):
    return "\n\n".join ([str(table) for table in self.tables if str(table)])


class Table:
  """Class containing base info for MySQL tables."""
  def __init__ (self, data):
    """Initialiazes a Table class from SQL data."""
    self.name = ''
    self.Fields = []
    self.primaryIndex = ''
    self.Indexes = []
    self.Options = { }

    self.__fieldNames = []
    self.__indexNames = []

    m = re.search ("CREATE TABLE `(.+?)`", data[0]); self.name = m.group(1)
    for m in re.finditer("([\w\d_ ]+?)=([^\s]+)", data[-1].strip()[2:-1]):
      self.Options[m.group(1).strip()] = m.group(2)
    fieldsAndIndexes = [line.strip() for line in data[1:-1]]
    for fieldOrIndex in fieldsAndIndexes:
      if fieldOrIndex.startswith ("PRIMARY"):
        m = re.search ("`(.+?)`", fieldOrIndex); self.primaryIndex = m.group(1)
        continue
      if fieldOrIndex.startswith ("`"):
        self.Fields.append (Field(fieldOrIndex))
        continue
      self.Indexes.append (Index(fieldOrIndex))

    self.__fieldNames = [field.name for field in self.Fields]
    self.__indexNames = [index.name for index in self.Indexes]

  def __sub__ (self, other):
    return alter.TableDiff().compare(other, self)

  def __eq__ (self, other):
    return not (self != other)

  def __ne__ (self, other):
    if len(str(self - other)) > 0:
      return True
    return False

  def __gt__ (self, other):
    if len (self.Fields) > len (other.Fields):
      return True

  def __lt__ (self, other):
    if len (self.Fields) < len (other.Fields):
      return True

  def field (self, name):
    if not name in self.__fieldNames:
      return None
    return self.Fields[self.__fieldNames.index(name)]

  def fieldExists (self, Field):
    if Field.name in self.__fieldNames:
      return True
    return False

  def index (self, name):
    if not name in self.__indexNames:
      return None
    return self.Indexes[self.__indexNames.index(name)]

  def indexExists (self, Index):
    if Index.name in self.__indexNames:
      return True
    return False

  def __str__ (self):
    return self.createSQL()

  def createSQL (self):
    return """CREATE TABLE `%s` (
%s
  PRIMARY KEY (`%s`)%s
  %s
) %s;""" % (self.name, "\n".join(["  %s," % str(f) for f in self.Fields]),
            self.primaryIndex,
            "," if len(self.Indexes) else "",
            ",\n  ".join(["%s" % str(i) for i in self.Indexes]),
            " ".join(["%s=%s" % (k, self.Options[k]) for k in self.Options.keys() if k != "AUTO_INCREMENT"])
            )

  def removeSQL (self):
    return """DROP TABLE `%s`;""" % (self.name)

class Field:
  def __init__ (self, data):
    self.name = ''
    self.type = ''
    self.options = ''
    self.null = True
    self.auto_increment = False
    self.default = ''
    m = re.search ("^`(.+?)`", data); self.name = m.group(1)
    data = data[len ("`%s` " % self.name):]
    m = re.search ("^(.+?)(\((.+?)\))?\s(.+)$", data)
    if m:
      self.type = m.group(1); self.options = m.group(3)
      data = m.group(4)
    else:
      m = re.search ("^([A-z]+)(\s*)(.*)$", data)
      self.type = m.group (1); data = m.group(3)

    if data.startswith ("NOT NULL"):
      self.null = False
    m = re.search ("default '(.+?)'", data);
    if m is not None:
      self.default = "'%s'" % m.group(1)
    else:
      m = re.search ("default ([^\s,]+)", data);
      if m is not None:
       self.default = "%s" % m.group(1)
    m = re.search ("auto_increment", data);
    if m:
      self.auto_increment = True

  def __ne__ (self, other):
    if self.name != other.name:
      return True
    if self.type != other.type:
      return True
    if self.options != other.options:
      return True
    if self.null != other.null:
      return True
    if self.auto_increment != other.auto_increment:
      return True
    if self.default != other.default:
      return True
    return False

  def __eq__ (self, other):
    return not (self != other)

  def __str__ (self):
    return "`%s` %s%s%s%s%s" % (self.name, self.type,
                                "(%s)" % self.options if self.options else "",
                                ' NULL' if self.null else " NOT NULL",
                                " default %s" % self.default if self.default else "",
                                ' auto_increment' if self.auto_increment else ""
                                )

class Index:
  def __init__ (self, data):
    self.type = ''
    self.name = ''
    self.fields = ''
    m = re.search ("^(.+?)\s+`(.+?)`\s+\((.+?)\)", data)
    self.type = m.group(1)
    self.name = m.group(2)
    self.fields = m.group(3)

  def __ne__ (self, other):
    if self.name != other.name:
      return True
    if self.type != other.type:
      return True
    if self.fields != other.fields:
      return True
    return False

  def __eq__ (self, other):
    return not (self != other)

  def __str__ (self):
    return "%s `%s` (%s)" % (self.type, self.name, self.fields)

  def forAlteration(self):
    TypeMap = { 'KEY': 'INDEX', 'UNIQUE KEY': 'UNIQUE', 'FULLTEXT KEY': 'FULLTEXT' }
    return "%s `%s` (%s)" % (TypeMap[self.type], self.name, self.fields)

if __name__ == '__main__':
  parsefile ('../source.sql')
