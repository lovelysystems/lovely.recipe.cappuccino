import logging
import os

import zc.buildout


class Builder(object):

    def __init__(self, buildout, name, options):
        self.logger = logging.getLogger(name)
        self.buildout = buildout
        self.buildoutOptions = buildout['buildout']
        self.name = name
        self.options = options
        self.narwhal = options.get('narwhal', None)
        if self.narwhal is None:
            zc.buildout.UserError('Option "narwhal" not provided')
        self.binName = options.get('name', name)
        self.nib2cib = options.get('nib2cib', '')
        self.datamodel = options.get('datamodel', '')

    def install(self):
        nib2cib = os.path.join(self.narwhal, 'bin', 'nib2cib')
        if not os.path.exists(nib2cib):
            pass
        os.environ['PATH'] =   os.path.join(self.narwhal, 'bin') \
                             + ':' \
                             + os.environ['PATH']
        tplParams = {}
        tplParams['pythonpath'] = self.buildoutOptions.get('executable')
        tplParams['narwhal'] = self.narwhal
        tplParams['nib2cib'] = self.nib2cib
        tplParams['datamodel'] = self.datamodel
        template = BUILD_TEMPLATE% tplParams
        binPath = os.path.join(self.buildoutOptions.get('bin-directory'),
                               self.binName)
        with file(binPath, 'w') as f:
            f.write(template)
        os.chmod(binPath, 0755)
        return (binPath,)

    def update(self):
        pass


BUILD_TEMPLATE = """#!%(pythonpath)s

import os
import subprocess

NARWHAL_PATH = '%(narwhal)s'
NIB2CIB_PATH = \"\"\"%(nib2cib)s\"\"\"
DATAMODEL_PATH = \"\"\"%(datamodel)s\"\"\"

nib2cib = os.path.join(NARWHAL_PATH, 'bin', 'nib2cib')
if not os.path.exists(nib2cib):
    print 'nib2cib not found at "%%s"'%% nib2cib
    exit(1);

def process(*args):
    print ' Executing:', ' '.join(args)
    cmd = subprocess.Popen(args)
    stdout, stderr = cmd.communicate()
    if cmd.returncode:
        print '  returned with error code', cmd.returncode
        print stderr
    return cmd.returncode

# process xib files::
os.environ['PATH'] =   os.path.join(NARWHAL_PATH, 'bin') \\
                    + ':' \\
                    + os.environ['PATH']
for path in NIB2CIB_PATH.split():
    print 'nib2cib: Processing path:', path
    for root, dirs, files in os.walk(path):
        for fname in files:
            if not fname.endswith('.xib'):
                continue
            xibName = os.path.join(root, fname)
            cibName = os.path.join(root, fname[:-3]+'cib')
            create = True
            if os.path.exists(cibName):
                xibStat = os.stat(xibName)
                cibStat = os.stat(cibName)
                create = xibStat.st_mtime >= cibStat.st_mtime
            if create:
                process(nib2cib, xibName)
            else:
                print ' File "%%s" is up to date'%% xibName

# process data models
for path in DATAMODEL_PATH.split():
    print 'datamodel: Searching path "%%s" for datamodels'%% path
    for root, dirs, files in os.walk(path):
        for fname in dirs:
            if not fname.endswith('.xcdatamodel'):
                continue
            xcName = os.path.join(root, fname)
            cxcName = os.path.join(root, fname[:-11] + 'cxcdatamodel')
            create = True
            if os.path.exists(cxcName):
                xcStat = os.stat(xcName)
                cxcStat = os.stat(cxcName)
                create = xcStat.st_mtime >= cxcStat.st_mtime
            if create:
                result = process('/Developer/usr/bin/momc',
                                 xcName, cxcName
                                )
                if (not result):
                    process('plutil', '-convert', 'xml1', cxcName)
            else:
                print ' File "%%s" is up to date'%% cxcName

"""

