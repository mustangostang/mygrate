import subprocess
import shutil
import sys
import os

tempdir = "/usr/local/share/mygrate"

def test_for_git():
  """Testing if Git binary is available"""
  try:
    subprocess.Popen(["git", "--version"], stdout=subprocess.PIPE).communicate()[0]
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
  subprocess.call(["git", "clone", "https://github.com/mustangostang/mygrate.git", tempdir])

def create_bin():
  """Create executable file for mygrate"""
  f = open ('/usr/local/bin/mygrate', 'w')
  f.writelines(['#! /bin/sh\n', 'python %s/mygrate.py "$@"' % tempdir])
  f.close()
  os.chmod('/usr/local/bin/mygrate', 0755)

def main():
  if not test_for_git():
    print ("Error: Git is not installed on your machine.")
    return
  update_to_temp()
  create_bin()
  test_for_mygrate()

if __name__ == '__main__':
  sys.exit (main())