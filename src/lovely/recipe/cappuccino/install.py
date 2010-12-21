import logging
import os
import shutil
import subprocess
import urllib2
import zipfile
import StringIO

import zc.buildout

logger = logging.getLogger(__name__)

REQUIRED_PACKAGES = ('browserjs', 'jake', 'shrinksafe', 'narwhal-jsc')

NARWHAL_USER = '280north'
NARWHAL_REF = 'master'
CAPPUCCINO_USER = '280north'
CAPPUCCINO_REF = 'master'

class Install(object):

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        self.path = options.get('path', 'parts')
        self.narwhalPath = os.path.join(self.path, 'narwhal')
        self.narwhalUser = options.get('narwhal-user', NARWHAL_USER)
        self.narwhalRef = options.get('narwhal-ref', NARWHAL_REF)
        self.narwhalRequired = options.get('narwhal-required', ())
        self.cappuccinoDevelop = options.get('cappuccino-develop', None)
        # for others to reference our narwhal installation directory:
        self.buildout[name]['narwhal-directory'] = self.narwhalPath

    def install(self):
        os.environ['PATH'] =   os.path.join(self.narwhalPath, 'bin') \
                             + ':' \
                             + os.environ['PATH']
        zip_ball="http://github.com/%s/narwhal/zipball/%s"% (
                                        self.narwhalUser, self.narwhalRef)
        narwhalZip, isTemp = zc.buildout.download.Download(
                                self.buildout.get('buildout'),
                                hash_name = True,
                                logger = logger,
                                )(zip_ball)
        if not os.path.exists(self.narwhalPath):
            cmd = subprocess.Popen(('unzip', narwhalZip, '-d', '/tmp'))
            stdout, stderr = cmd.communicate()
            files = [f for f in os.listdir('/tmp') if f.startswith('280north')]
            shutil.move(os.path.join('/tmp', files[0]), self.narwhalPath)

            tusk = os.path.join(self.narwhalPath, 'bin', 'tusk')
            if self.cappuccinoDevelop is None:
                # install standard package
                self.narwhalRequired += ('cappuccino',)
            cmd = subprocess.Popen(  (tusk, 'install',)
                                   + REQUIRED_PACKAGES
                                   + self.narwhalRequired,)
            stdout, stderr = cmd.communicate()
            cmd = subprocess.Popen((tusk, 'list'),)
            stdout, stderr = cmd.communicate()
            if os.uname()[0] == 'Darwin':
                # build jsc for webkit
                os.environ['NARWHAL_ENGINE'] = 'jsc'
                wd = os.getcwd()
                os.chdir(os.path.join(self.narwhalPath, 'packages', 'narwhal-jsc'))
                cmd = subprocess.Popen(('make', 'webkit',))
                stdout, stderr = cmd.communicate()
                os.chdir(wd)


        # at this point we have a narwhal installation
        if self.cappuccinoDevelop is not None:
            # install cappuccino from a git clone
            os.environ['NARWHAL_ENGINE'] = 'jsc'
            os.environ['CAPP_BUILD'] = os.path.join(
                                        self.cappuccinoDevelop, 'Build')
            jake = os.path.join(self.narwhalPath, 'bin', 'jake')
            wd = os.getcwd()
            os.chdir(self.cappuccinoDevelop)
            cmd = subprocess.Popen((jake, 'install',))
            stdout, stderr = cmd.communicate()
            os.chdir(wd)

        return (self.narwhalPath,)

    def update(self):
        pass

