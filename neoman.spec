# -*- mode: python -*-
# -*- encoding: utf-8 -*-
import os
import sys
from glob import glob
from getpass import getpass

NAME = "YubiKey NEO Manager"

WIN = sys.platform in ['win32', 'cygwin']
OSX = sys.platform in ['darwin']

ICON = os.path.join('neoman', 'neoman.png')
if WIN:
    ICON = os.path.join('resources', 'neoman.ico')

elif OSX:
    ICON = os.path.join('resources', 'neoman.icns')

a = Analysis(['scripts/neoman'],
             pathex=[''],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)

# DLLs and dylibs should go here.
libs = glob('lib/*.dll') + glob('lib/*.dylib') + glob('lib/*.so')
for filename in libs:
    a.datas.append((filename[4:], filename, 'BINARY'))
a.datas.append(('neoman.png', 'neoman/neoman.png', 'DATA'))

# Read version information on Windows.
VERSION = None
if WIN:
    VERSION = 'build/file_version_info.txt'

    #Read version string
    with open('neoman/__init__.py', 'r') as f:
        import re
	match = re.search(r"(?m)^__version__\s*=\s*['\"](.+)['\"]$", f.read())
    ver_str = match.group(1)
    ver_tup = tuple(map(int, ver_str.split('.')))
    while len(ver_tup) < 4:
        ver_tup += (0,)
    assert len(ver_tup) == 4

    #Write version info.
    with open(VERSION, 'w') as f:
        f.write("""
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four
    # items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=%(ver_tup)r,
    prodvers=%(ver_tup)r,
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x0,
    # Contains a bitmask that specifies the Boolean attributes
    # of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x4,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904E4',
        [StringStruct(u'FileDescription', u'YubiKey NEO Manager'),
        StringStruct(u'FileVersion', u'%(ver_str)s'),
        StringStruct(u'InternalName', u'neoman'),
        StringStruct(u'LegalCopyright', u'Copyright © 2013 Yubico'),
        StringStruct(u'OriginalFilename', u'%(exe_name)s'),
        StringStruct(u'ProductName', u'YubiKey NEO Manager'),
        StringStruct(u'ProductVersion', u'%(ver_str)s')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1252])])
  ]
)""" % {
            'ver_tup': ver_tup,
            'ver_str': ver_str,
            'exe_name': '%s.exe' % NAME
        })

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name=NAME if not WIN else '%s.exe' % NAME,
          debug=False,
          strip=None,
          upx=True,
          console=False,
          version=VERSION,
          icon=ICON)

if WIN:
    if not os.path.isfile("neoman.pfx"):
        print "neoman.pfx not found, not signing executable!"
    else:
        os.system("signtool.exe sign /f neoman.pfx /p %s /t http://timestamp.verisign.com/scripts/timstamp.dll \"%s\"" %
                 (getpass('Enter password for PFX file: '), exe.name))

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=NAME)

if OSX:
    app = BUNDLE(coll,
                 name="%s.app" % NAME,
                 icon=ICON)
