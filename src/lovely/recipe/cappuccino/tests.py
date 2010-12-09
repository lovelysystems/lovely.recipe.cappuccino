import doctest
import unittest
import zc.buildout.testing


def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install_develop('lovely.recipe.cappuccino', test)


def test_suite():
    return doctest.DocFileSuite(
        'README.txt',
        setUp=setUp, tearDown=zc.buildout.testing.buildoutTearDown,
        optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
        )

