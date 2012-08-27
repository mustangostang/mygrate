import subprocess
import shutil
import sys
import os

tempdir = "%s/mygrate" % os.getcwd()
bindir  = '/opt/local/bin'

def test_for_svn():
  """Testing if SVN binary is available"""
  try:
    subprocess.Popen(["svn", "--version"], stdout=subprocess.PIPE).communicate()[0]
    return True
  except OSError:
    return False

def test_for_mygrate():
  """Testing if mygrate binary is available"""
  subprocess.Popen(["mygrate"], stdout=subprocess.PIPE).communicate()[0]
  print "Mygrate installed successfully."

def update_to_temp():
  try:
    os.makedirs(tempdir)
  except OSError:
    shutil.rmtree(tempdir, ignore_errors = True)
  print "Updating mygrate from Google Code"
  subprocess.call(["svn", "co", "http://mygrate.googlecode.com/svn/trunk/", tempdir])

def create_bin():
  """Create executable file for mygrate"""
  f = open ('%s/mygrate' % bindir, 'w')
  f.writelines(['#! /bin/sh\n', 'python %s/mygrate.py "$@"' % tempdir])
  f.close()
  os.chmod('%s/mygrate' % bindir, 0755)

def main():
  if not test_for_svn():
    print ("Error: Subversion is not installed on your machine.")
    return
  update_to_temp()
  create_bin()
  test_for_mygrate()

if __name__ == '__main__':
  sys.exit (main())