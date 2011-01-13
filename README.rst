========================
lovely.recipe.cappuccino
========================

This recipe allows you to

 - install cappuccino as a local installation inside your development environment
 - setup a build tool to support cibs and data models


Cappuccino Installer
====================

Creates a local cappuccino installation for your project.

Buildout options
----------------

 - path : where to install narwhal (default: parts)
 - narwhal-user : github user from which to get narwhal (default: 280north)
 - narwhal-ref : reference of the version/branch to use (default: master)
 - narwhal-required : additional packages to install into narwhal

 - cappuccino-develop : path to a cappuccino checkout (default: None)


What happens
------------

download narwahl from github using the options::

  http://github.com/<narwhal-user>/narwhal/zipball/<narwhal-ref>

The downloaded file is cached using the standard buildout cache.

if the path <path>/narwhal doesn't exist::

  - extract narwhal to <path>/narwhal
  - run "tusk install browserjs jake shrinksafe narwhal-jsc"
  - run "make webkit" in <path>/narwhal/packages/narwhal-jsc
  - run "tusk install cappuccino"
  - run "tusk install <required>" for every <narwahl-reqired> package

If we are installing on a MAC (uname == 'Darwin') narwhal-jsc is compiled.

At this point of the installation we have narwhal installed at <path>/narwahl
with the latest released cappuccino version.


Using a Development Version of cappuccino
-----------------------------------------

If you provide a path to a cappuccino checkout then "jake install" is run to
install the dev-version into narwhal.

To get a cappuccino checkout we suggest to use mr.developer to get cappuccino
from git.

Here's a sample buildout setup to install a cappuccino checkout at
${buildout-directory}/js/cappuccino

::
    [buildout]

    extensions = mr.developer

    # mr.developer options
    auto-checkout = *
    sources = sources
    sources-dir = js

    [sources]
    cappuccino = git egg=false git://github.com/280north/cappuccino.git


Cappuccino Build Tools
======================

Creates an executable to build whatever is needed for your cappuccino
project(s).


Option: narwhal (required)
--------------------------

The path to the narwhal installation to use. You can easily get the path from
the cappcuccino install parts using ${partname:narwhal-directory}.


Option: name (optional)
-----------------------

The name for the executable (default: the name of the buildout part)


Option: nib2cib (optional)
--------------------------

List of paths to your projects to look for \*.xib files.

Run "nib2cib" for all xib files found.


Option: datamodel (optional)
----------------------------

List of paths to your projects to look for "\*.xcdatamodel" files.

Run
    - /Developer/usr/bin/momc <name.xcdatamodel> name.cxcdatamodel
    - plutil -convert xml1 name.cxcdatamodel
for every xcdatamodel found in and below the path.

