#!/usr/bin/python

import os
import sys
import getpass
import subprocess
from datetime import date

from fabricate import *


MAXOSDIR = os.environ['MAXELEROSDIR']
MAXCOMPILERDIR = os.environ['MAXCOMPILERDIR']


MAXFILE = 'PacketFilter.max'
DESIGN_NAME = MAXFILE.replace('.max', '')
sources = ['filter.c']
target = 'filter'
includes = [] 
MAXPOWER_LIBS = []



def sliccompile():
	"""Compiles a maxfile in to a .o file"""
	run("%s/bin/sliccompile" % (MAXCOMPILERDIR), MAXFILE, MAXFILE.replace('.max', '.o'))


def get_maxcompiler_inc():
    """Return the includes to be used in the compilation."""
    return ['-I.', '-I%s/include' % MAXOSDIR, '-I%s/include/slic' % MAXCOMPILERDIR]

def get_maxcompiler_libs():
    """Return the libraries to be used in linking."""
    return ['-L%s/lib' % MAXCOMPILERDIR, '-L%s/lib' % MAXOSDIR, '-lslic', '-lmaxeleros', '-lm', '-lpthread']

def get_ld_libs():
    """Returns the libraries to be used for linking."""
    return MAXPOWER_LIBS + get_maxcompiler_libs() +  [MAXFILE.replace('.max', '.o')]


cflags = ['-ggdb', '-O2', '-fPIC', 
		  '-std=gnu99', '-Wall', '-Werror', 
		  '-DDESIGN_NAME=%s' % (DESIGN_NAME)] + includes + get_maxcompiler_inc() 

def build():
    compile()
    link()

def rebuild():
	maxfile()
	compile()
	link()


def compile():
	sliccompile()
	for source in sources:
		run('gcc', cflags, '-c', source, '-o', source.replace('.c', '.o'))

def link():
    objects = [s.replace('.c', '.o') for s in sources]
    run('gcc', objects, get_ld_libs(), '-o', target)


def maxfile():
	print "Buidling maxfile..."
	os.environ["CLASSPATH"]="../bitstream/bin/:" + os.environ["CLASSPATH"] + ":" + os.environ["MAXPOWERDIR"] + "/bin/:"; 
	subprocess.call(['maxJavaRun' , 'com/maxeler/packetfilter/FilterManager'])
	now = date.today().strftime("%d-%m-%y")
	run('cp', '-f', '-v', '/scratch/itay/maxdc_builds/%s/PacketFilter_ISCA_DFE_SIM/results/PacketFilter.max' % (now), 'PacketFilter.max')

def clean():
    autoclean()

def getSimName():
	return getpass.getuser() + 'Sim'


def maxcompilersim():
	return '%s/bin/maxcompilersim' % MAXCOMPILERDIR

def run_sim():
	build()
	start_sim()
	subprocess.call(['./%s' % (target)])

def start_sim():
	subprocess.call([maxcompilersim(), '-n', getSimName(), '-c', 'ISCA', 
		'-e', 'QSFP_TOP_10G_PORT1:172.20.50.10:255.255.255.0', 
		'-e', 'QSFP_BOT_10G_PORT1:172.30.50.10:255.255.255.0',
		'-p', 'QSFP_TOP_10G_PORT1:top1.pcap', 'restart'])

def stop_sim():
	subprocess.call([maxcompilersim(), '-n', getSimName(), 'stop'])

def restart_sim():
	start_sim()	
	
def sim_debug():
	subprocess.call(['maxdebug', '-g', 'graph_%s' % getSimName(), '-d',  '%s0:%s' % (getSimName(), getSimName()), MAXFILE])


main()
