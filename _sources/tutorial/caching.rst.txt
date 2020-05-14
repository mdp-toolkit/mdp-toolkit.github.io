.. _caching:

=========================
Caching execution results
=========================
.. codesnippet::

Introduction
------------

It is relatively common for nodes to process the same data several
times. Usually this happens when training a long sequence of nodes
using a fixed data set: to train the nodes at end of the sequence, the
data has to be processed by all the preceding ones. This duplication
of efforts may be costly, for example in image processing, when one
needs to repeatedly filter the images (:ref:`as in this
example<convolution2D>`).

MDP offers a :ref:`node extension <extensions>` that automatically
caches the result of the ``execute`` method, which can boost the speed
of an application considerably in such scenarios. The cache can be
activated globally (i.e., for all node instances), for some node
classes only, or for specific instances.

The caching mechanism is based on the library 
`joblib <http://packages.python.org/joblib/>`_, version 0.4.3 or higher.

Activating the caching extension
--------------------------------

It is possible to activate the caching extension as for regular
extension using the extension name ``'cache_execute'``. By default,
the cached results will be stored in a database created in a
temporary directory for the duration of the Python session. To
change the caching directory, which may be useful to create a
permanent cache over multiple sessions, one can call the function
``mdp.caching.set_cachedir``.

We will illustrate the caching extension using a simple but relatively
large Principal Component Analysis problem:

    >>> # set up a relatively large PCA run
    >>> import mdp
    >>> import numpy as np
    >>> from timeit import Timer
    >>> x = np.random.rand(3000,1000)
    >>> # create a PCANode and train it using the random data in 'x'
    >>> pca_node = mdp.nodes.PCANode()
    >>> pca_node.train(x)
    >>> pca_node.stop_training()

The time for projecting the data ``x`` on the principal components
drops dramatically after the caching extension is activated:

    >>> # we will use this timer to measure the speed of 'pca_node.execute'
    >>> timer = Timer("pca_node.execute(x)", "from __main__ import pca_node, x")
    >>> mdp.caching.set_cachedir("/tmp/my_cache")
    >>> mdp.activate_extension("cache_execute")
    >>> # all calls to the 'execute' method will now be cached in 'my_cache'
    >>> # the first time execute is called, the method is run
    >>> # and the result is cached
    >>> print timer.repeat(1, 1)[0], 'sec' # doctest: +SKIP
    1.188946008682251 sec
    >>> # the second time, the result is retrieved from the cache
    >>> print timer.repeat(1, 1)[0], 'sec' # doctest: +SKIP
    0.112375974655 sec
    >>> mdp.deactivate_extension("cache_execute")
    >>> # when the cache extension is deactivated, the 'execute' method is
    >>> # called as usual
    >>> print timer.repeat(1, 1)[0], 'sec' # doctest: +SKIP
    0.801102161407 sec

Alternative ways to activate the caching extension, which also expose
more functionalities, can be found in the ``mdp.caching`` module.
The functions ``activate_caching`` and ``deactivate_caching`` allow
activating the cache only on certain Node classes, or specific
instances. For example, the following line starts the cache extension,
caching only instances of the classes ``SFANode`` and ``FDANode``,
and the instance ``pca_node``.

    >>> mdp.caching.activate_caching(cachedir='/tmp/my_cache',
    ...     cache_classes=[mdp.nodes.SFANode, mdp.nodes.FDANode],
    ...     cache_instances=[pca_node])
    >>> # all calls to the 'execute' method of instances of 'SFANode' and
    >>> # 'FDANode', and of 'pca_node' will now be cached in 'my_cache'
    >>> mdp.caching.deactivate_caching()

Make sure to call the ``deactivate_caching`` method before the end of
the session, or the cache directory may remain in a broken state.

Finally, the module ``mdp.caching`` also defines a context manager
that closes the cache properly at the end of the block:

    >>> with mdp.caching.cache(cachedir='/tmp/my_cache', cache_instances=[pca_node]):
    ...     # in the block, the cache is active
    ...     print timer.repeat(1, 1)[0], 'sec' # doctest: +SKIP
    ... 
    0.101263999939 sec
    >>> # at the end of the block, the cache is deactivated
    >>> print timer.repeat(1, 1)[0], 'sec' # doctest: +SKIP
    0.801436901093 sec

