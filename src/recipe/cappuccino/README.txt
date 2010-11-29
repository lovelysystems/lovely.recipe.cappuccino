==================================
The ``cappuccino`` Buildout Recipe
==================================


Let's create a sample buildout to install it:

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = cappuccino
    ...
    ... [cappuccino]
    ... recipe = recipe.cappuccino
    ... """)

When running buildout, cappuccino is installed

    >>> print system('bin/buildout')
    Installing cappuccino.

