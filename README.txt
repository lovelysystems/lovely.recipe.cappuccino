This recipe allows you to install cappuccino as a local installation inside
your development environment.


Buildout options
================

path - where to install narwhal (default: parts)
narwhal-user - github user from which to get narwhal (default: 280north)
narwhal-ref - reference of the version/branch to use (default: master)
narwhal-required - additional packages to install into narwhal

cappuccino-develop - path to a cappuccino checkout (default: None)


What happens
============

download narwahl from:
  http://github.com/<narwhal-user>/narwhal/zipball/<narwhal-ref>

The downloaded file is cached using the standard buildout cache.

if the path <path>/narwhal doesn't exist::
  - extract narwhal to <path>/narwhal
  - run "tusk install browserjs jake shrinksafe narwhal-jsc <narwahl-reqired>"
  - run "make webkit" in <path>/narwhal/packages/narwhal-jsc

At this point of the installation we have narwhal insalled at <path>/narwahl
with lates released cappuccino version.


Using a Development Version of cappuccino
=========================================

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

