.. _iterables:

=========
Iterables
=========
.. codesnippet::

Python allows user-defined classes to support iteration,
as described in the `Python docs 
<http://docs.python.org/library/stdtypes.html#iterator-types>`_. A class is a 
so called iterable if it defines a method ``__iter__`` that returns an 
iterator instance. An iterable is typically some kind of container or 
collection (e.g. ``list`` and ``tuple`` are iterables).

The iterator instance must have a ``next`` method that returns the next 
element in the iteration. In Python an iterable also has to have an 
``__iter__`` method itself that returns ``self`` instead of a new iterator. 
It is important to understand that an iterator only manages a single iteration. 
After this iteration it is spend and cannot be used for a second iteration 
(it cannot be restarted). An iterable on the other hand can create as many 
iterators as needed and therefore supports multiple iterations. Even though 
both iterables and iterators have an ``__iter__`` method they are 
semantically very different (duck-typing can be misleading in this case).

In the context of MDP this means that an iterator can only be used for a 
single training phase, while iterables also support multiple training phases. 
So if you use a node with multiple training phases and train it in a flow 
make sure that you provide an iterable for this node (otherwise an exception 
will be raised). For nodes with a single training phase you can use 
either an iterable or an iterator.

A convenient implementation of the iterator protocol is provided
by generators:
see `this article <http://linuxgazette.net/100/pramode.html>`__ for an
introduction, and the official `PEP 255 <http://www.python.org/dev/peps/pep-0255/>`_
for a complete description.

Let us define two bogus node classes to be used as examples of nodes

    >>> class BogusNode(mdp.Node):
    ...     """This node does nothing."""
    ...     def _train(self, x):
    ...         pass
    >>> class BogusNode2(mdp.Node):
    ...     """This node does nothing. But it's neither trainable nor invertible.
    ...     """
    ...     def is_trainable(self): return False
    ...     def is_invertible(self): return False

This generator generates ``blocks`` input blocks to be used as training set.
In this example one block is a 2-dimensional time series. The first variable
is [2,4,6,....,1000] and the second one [0,1,3,5,...,999].
All blocks are equal, this of course would not be the case in a real-life
example.

In this example we use a progress bar to get progress information.

    >>> def gen_data(blocks):
    ...     for i in mdp.utils.progressinfo(xrange(blocks)):
    ...         block_x = np.atleast_2d(np.arange(2.,1001,2))
    ...         block_y = np.atleast_2d(np.arange(1.,1001,2))
    ...         # put variables on columns and observations on rows
    ...         block = np.transpose(np.concatenate([block_x,block_y]))
    ...         yield block

The ``progressinfo`` function is a fully configurable text-mode
progress info box tailored to the command-line die-hards. Have a look
at its doc-string and prepare to be amazed!

Let's define a bogus flow consisting of 2 ``BogusNode``\ s

    >>> flow = mdp.Flow([BogusNode(),BogusNode()], verbose=1)

Train the first node with 5000 blocks and the second node with 3000 blocks. 
Note that the only allowed argument to ``train`` is a sequence (list or 
tuple) of iterables or iterators. In case you don't want or need to use 
incremental learning and want to do a one-shot training, you can use as 
argument to ``train`` a single array of data.

Block-mode training
-------------------

    >>> flow.train([gen_data(5000),gen_data(3000)]) # doctest: +SKIP
    Training node #0 (BogusNode)
    <BLANKLINE>
    [===================================100%==================================>]  
    <BLANKLINE>
    Training finished
    Training node #1 (BogusNode)
    [===================================100%==================================>]  
    <BLANKLINE>
    Training finished
    Close the training phase of the last node

One-shot training using one single set of data for both nodes
-------------------------------------------------------------

    >>> flow = BogusNode() + BogusNode()
    >>> block_x = np.atleast_2d(np.arange(2.,1001,2))
    >>> block_y = np.atleast_2d(np.arange(1.,1001,2))
    >>> single_block = np.transpose(np.concatenate([block_x,block_y]))
    >>> flow.train(single_block)

If your flow contains non-trainable nodes, you must specify a ``None``
for the non-trainable nodes

    >>> flow = mdp.Flow([BogusNode2(),BogusNode()], verbose=1)
    >>> flow.train([None, gen_data(5000)]) # doctest: +SKIP
    Training node #0 (BogusNode2)
    Training finished
    Training node #1 (BogusNode)
    [===================================100%==================================>]  
    <BLANKLINE>
    Training finished
    Close the training phase of the last node

You can use the one-shot training

    >>> flow = mdp.Flow([BogusNode2(),BogusNode()], verbose=1)
    >>> flow.train(single_block) # doctest: +SKIP
    Training node #0 (BogusNode2)
    Training finished
    Training node #1 (BogusNode)
    Training finished
    Close the training phase of the last node

Iterators can always be safely used for execution and inversion, since only a 
single iteration is needed

    >>> flow = mdp.Flow([BogusNode(),BogusNode()], verbose=1)
    >>> flow.train([gen_data(1), gen_data(1)])                     # doctest: +SKIP
    Training node #0 (BogusNode)
    Training finished
    Training node #1 (BosgusNode)
    [===================================100%==================================>]
    <BLANKLINE>
    Training finished
    Close the training phase of the last node
    >>> output = flow.execute(gen_data(1000))                      # doctest: +SKIP
    [===================================100%==================================>]
    >>> output = flow.inverse(gen_data(1000))                      # doctest: +SKIP
    [===================================100%==================================>]

.. doctests must be skipped, because doctest doesn’t cope with carriage returns
.. in console output

Execution and inversion can be done in one-shot mode also. Note that
since training is finished you are not going to get a warning

    >>> output = flow(single_block)
    >>> output = flow.inverse(single_block)

If a node requires multiple training phases (e.g., 
``GaussianClassifierNode``), ``Flow`` automatically takes care of using the 
iterable multiple times. In this case generators (and iterators) are not 
allowed, since they are spend after yielding the last data block.

However, it is fairly easy to wrap a generator in a simple iterable if you need to

    >>> class SimpleIterable(object):
    ...     def __init__(self, blocks):
    ...         self.blocks = blocks
    ...     def __iter__(self):
    ...         # this is a generator
    ...         for i in range(self.blocks):
    ...             yield generate_some_data()

Note that if you use random numbers within the generator, you usually
would like to reset the random number generator to produce the
same sequence every time

    >>> class RandomIterable(object):
    ...     def __init__(self):
    ...         self.state = None
    ...     def __iter__(self):
    ...         if self.state is None:
    ...             self.state = np.random.get_state()
    ...         else:
    ...             np.random.set_state(self.state)
    ...         for i in range(2):
    ...             yield np.random.random((1,4))
    >>> iterable = RandomIterable()
    >>> for x in iterable:
    ...     print x
    [[ 0.5488135   0.71518937  0.60276338  0.54488318]]
    [[ 0.4236548   0.64589411  0.43758721  0.891773  ]]
    >>> for x in iterable:
    ...     print x
    [[ 0.5488135   0.71518937  0.60276338  0.54488318]]
    [[ 0.4236548   0.64589411  0.43758721  0.891773  ]]
