==================================
The ``cappuccino`` Buildout Recipe
==================================


Cappuccino Installer
--------------------

Let's create a sample buildout to install it:

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = cappuccino
    ...
    ... [cappuccino]
    ... recipe = lovely.recipe.cappuccino:install
    ... """)

When running buildout, cappuccino is installed

#    >>> print system('bin/buildout')
#    Installing cappuccino.


Cappuccino Build Tool
---------------------

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = cappuccino-build
    ...
    ... [cappuccino-build]
    ... recipe = lovely.recipe.cappuccino:builder
    ... narwhal = ${buildout:directory}/narwhal
    ... """)

    >>> print system('bin/buildout')
    Installing cappuccino-build.

    >>> ls(sample_buildout)
    -  .installed.cfg
    d  bin
    -  buildout.cfg
    d  develop-eggs
    d  eggs
    d  parts

    >>> import os
    >>> ls(os.path.join(sample_buildout, 'bin'))
    -  buildout
    -  cappuccino-build

    >>> cat(os.path.join(sample_buildout, 'bin', 'cappuccino-build'))
    #!.../Python
    <BLANKLINE>
    import os
    import subprocess
    <BLANKLINE>
    NARWHAL_PATH = '.../sample-buildout/narwhal'
    NIB2CIB_PATH = """"""
    DATAMODEL_PATH = """"""
    ...

By default the name of the script is set to the name of the buildout section
but we can overwrite this.

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = cappuccino-build
    ...
    ... [cappuccino-build]
    ... recipe = lovely.recipe.cappuccino:builder
    ... narwhal = ${buildout:directory}/narwhal
    ... name = builder
    ... nib2cib = path1
    ...           path2
    ... datamodel = modelpath
    ... """)
    >>> print system('bin/buildout')
    Uninstalling cappuccino-build.
    Installing cappuccino-build.
    >>> ls(os.path.join(sample_buildout, 'bin'))
    -  builder
    -  buildout
    >>> cat(os.path.join(sample_buildout, 'bin', 'builder'))
    #!.../Python
    <BLANKLINE>
    import os
    import subprocess
    <BLANKLINE>
    NARWHAL_PATH = '.../sample-buildout/narwhal'
    NIB2CIB_PATH = """path1
    path2"""
    DATAMODEL_PATH = """modelpath"""
    ...

Running the generated tool
--------------------------

First we build a dummy nib2cib application.

    >>> mkdir(sample_buildout, 'narwhal')
    >>> mkdir(sample_buildout, 'narwhal', 'bin')
    >>> write(sample_buildout, 'narwhal', 'bin', 'nib2cib',
    ... """#!/bin/sh
    ... echo nib2cib $1
    ... """)
    >>> os.chmod(os.path.join(sample_buildout, 'narwhal', 'bin', 'nib2cib'), 0755)
    >>> print system(os.path.join(sample_buildout, 'bin', 'builder'))
    nib2cib: Processing path: path1
    nib2cib: Processing path: path2
    datamodel: Searching path "modelpath" for datamodels

    >>> mkdir(sample_buildout, 'path1')
    >>> write(sample_buildout, 'path1', 'dummy1.xib', 'dummycontent')
    >>> print system(os.path.join(sample_buildout, 'bin', 'builder'))
    nib2cib path1/dummy1.xib
    nib2cib: Processing path: path1
     Executing: .../sample-buildout/narwhal/bin/nib2cib path1/dummy1.xib
    nib2cib: Processing path: path2
    datamodel: Searching path "modelpath" for datamodels

