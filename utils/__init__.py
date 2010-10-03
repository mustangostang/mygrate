#!/usr/bin/env python
from subprocess import Popen, PIPE

def shell(cmd):
	"""Run shell command"""
	return Popen(cmd, shell=True, stdout=PIPE).stdout.read()