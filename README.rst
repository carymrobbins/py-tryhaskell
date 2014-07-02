tryhaskell
==========

Python client for http://tryhaskell.org/

Installation
------------

.. code-block:: bash

    pip install tryhaskell`

Usage
-----

.. code-block:: python

    >>> from tryhaskell import TryHaskell
    >>> TryHaskell.eval('1+2')
    u'3'
    >>> TryHaskell.get('liftM2 (+)')
    Result(ok=True, expr=u'liftM2 (+)', files={}, stdout=[], type=u'(Monad m, Num r) => m r -> m r -> m r', value=u'')
    >>> TryHaskell.raw('[x*2 | x <- [1,2,3]]')
    {u'success': {
        u'expr': u'[x*2 | x <- [1,2,3]]',
        u'files': {},
        u'stdout': [],
        u'type': u'Num t => [t]',
        u'value': u'[2,4,6]'
    }}
    >>> TryHaskell.eval('foobar')
    u"Not in scope: `foobar'"
    >>> TryHaskell.get('foobar')
    Result(ok=False, expr='', files={}, stdout='', type='', value=u"Not in scope: `foobar'\n")
    >>> TryHaskell.raw('foobar')
    {u'error': u"Not in scope: `foobar'\n"}


You can test expressions easily using the repl -

.. code-block:: haskell

    $ python -m tryhaskell
    λ 1+2
    3
    λ liftM2 (+)
    liftM2 (+) :: (Monad m, Num r) => m r -> m r -> m r
    λ [x*2 | x <- [1..5], even x]
    [4,8]
    λ foobar
    Not in scope: `foobar'
