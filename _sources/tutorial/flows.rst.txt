.. _flows:

=====
Flows
=====
.. codesnippet::

A *flow* is a sequence of nodes that are trained and executed
together to form a more complex algorithm.  Input data is sent to the
first node and is successively processed by the subsequent nodes along
the sequence.

Using a flow as opposed to handling manually a set of nodes has a
clear advantage: The general flow implementation automatizes the
training (including supervised training and multiple training phases),
execution, and inverse execution (if defined) of the whole sequence.

Crash recovery is optionally available: in case of failure the current
state of the flow is saved for later inspection. A subclass of the
basic flow class (``CheckpointFlow``) allows user-supplied checkpoint
functions to be executed at the end of each phase, for example to save
the internal structures of a node for later analysis.
Flow objects are Python containers. Most of the builtin ``list``
methods are available. A ``Flow`` can be saved or copied using the
corresponding ``save`` and ``copy`` methods.


Flow instantiation, training and execution
------------------------------------------

For example, suppose we need to analyze a very
high-dimensional input signal using Independent Component Analysis
(ICA). To reduce the computational load, we would like to reduce the
input dimensionality of the data using PCA. Moreover, we would like to
find the data that produces local maxima in the output of the ICA
components on a new test set (this information could be used
for instance to characterize the ICA filters).

We start by generating some input signal at random (which makes the
example useless, but it's just for illustration...).  Generate 1000
observations of 20 independent source signals

    >>> inp = np.random.random((1000, 20))

Rescale x to have zero mean and unit variance

    >>> inp = (inp - np.mean(inp, 0))/np.std(inp, axis=0, ddof=0)

We reduce the variance of the last 15 components, so that they are
going to be eliminated by PCA

    >>> inp[:,5:] /= 10.0

Mix the input signals linearly

    >>> x = mdp.utils.mult(inp,np.random.random((20, 20)))

``x`` is now the training data for our simulation. In the same way
we also create a test set ``x_test``.

    >>> inp_test = np.random.random((1000, 20))
    >>> inp_test = (inp_test - np.mean(inp_test, 0))/np.std(inp_test, 0)
    >>> inp_test[:,5:] /= 10.0
    >>> x_test = mdp.utils.mult(inp_test, np.random.random((20, 20)))

We could now perform our analysis using only nodes, that's the lengthy way...
  
1. Perform PCA

    >>> pca = mdp.nodes.PCANode(output_dim=5)
    >>> pca.train(x)
    >>> out1 = pca(x)

2. Perform ICA using CuBICA algorithm

    >>> ica = mdp.nodes.CuBICANode()
    >>> ica.train(out1)
    >>> out2 = ica(out1)

3. Find the three largest local maxima in the output of the ICA node
   when applied to the test data, using a ``HitParadeNode``

    >>> out1_test = pca(x_test)
    >>> out2_test = ica(out1_test)
    >>> hitnode = mdp.nodes.HitParadeNode(3)
    >>> hitnode.train(out2_test)
    >>> maxima, indices = hitnode.get_maxima()

or we could use flows, which is the best way

    >>> flow = mdp.Flow([mdp.nodes.PCANode(output_dim=5), mdp.nodes.CuBICANode()])


Note that flows can be built simply by concatenating nodes
  
    >>> flow = mdp.nodes.PCANode(output_dim=5) + mdp.nodes.CuBICANode()
      
Train the resulting flow

    >>> flow.train(x)
  
Now the training phase of PCA and ICA are completed. Next we append
a ``HitParadeNode`` which we want to train on the test data

    >>> flow.append(mdp.nodes.HitParadeNode(3))
    
As before, new nodes can be appended to an existing flow by adding
them ot it

    >>> flow += mdp.nodes.HitParadeNode(3)
  
Train the ``HitParadeNode`` on the test data

    >>> flow.train(x_test)
    >>> maxima, indices = flow[2].get_maxima()

A single call to the ``flow``'s ``train`` method will automatically
take care of training nodes with multiple training phases, if such
nodes are present.  

Just to check that everything works properly, we
can calculate covariance between the generated sources and the output
(should be approximately 1)

    >>> out = flow.execute(x)
    >>> cov = np.amax(abs(mdp.utils.cov2(inp[:,:5], out)), axis=1)
    >>> print cov
    [ 0.9957042   0.98482351  0.99557617  0.99680391  0.99232424]

The ``HitParadeNode`` is an analysis node and as such does not
interfere with the data flow.
  
Note that flows can be executed by calling the ``Flow`` instance
directly
     
   >>> out = flow(x)

Flow inversion
--------------

Flows can be inverted by calling their ``inverse`` method.
In the case where the flow contains non-invertible nodes,
trying to invert it would raise an exception.
In this case, however, all nodes are invertible.
We can reconstruct the mix by inverting the flow

    >>> rec = flow.inverse(out)

Calculate covariance between input mix and reconstructed mix:
(should be approximately 1)

    >>> cov = np.amax(abs(mdp.utils.cov2(x/np.std(x,axis=0),
    ...                                  rec/np.std(rec,axis=0))))
    >>> print cov
    0.999622205447

Flows are container type objects
--------------------------------

``Flow`` objects are defined as Python containers, and thus are endowed with
most of the methods of Python lists.

You can loop through a ``Flow``

    >>> for node in flow:
    ...     print repr(node)
    PCANode(input_dim=20, output_dim=5, dtype='float64')
    CuBICANode(input_dim=5, output_dim=5, dtype='float64')
    HitParadeNode(input_dim=5, output_dim=5, dtype='float64')
    HitParadeNode(input_dim=5, output_dim=5, dtype='float64')

You can get slices, ``pop``, ``insert``, and ``append`` nodes

    >>> len(flow)
    4
    >>> print flow[::2]
    [PCANode, HitParadeNode]
    >>> nodetoberemoved = flow.pop(-1)
    >>> nodetoberemoved
    HitParadeNode(input_dim=5, output_dim=5, dtype='float64')
    >>> len(flow)
    3

Finally, you can concatenate flows

    >>> dummyflow = flow[1:].copy()
    >>> longflow = flow + dummyflow
    >>> len(longflow)
    5

The returned flow must always be consistent, i.e. input and
output dimensions of successive nodes always have to match. If 
you try to create an inconsistent flow you'll get an exception.


Crash recovery
--------------

If a node in a flow fails, you'll get a traceback that tells you which
node has failed. You can also switch the crash recovery capability on. If
something goes wrong you'll end up with a pickle dump of the flow, that 
can be later inspected.

To see how it works let's define a bogus node that always throws an 
``Exception`` and put it into a flow

    >>> class BogusExceptNode(mdp.Node):
    ...    def train(self,x):
    ...        self.bogus_attr = 1
    ...        raise Exception, "Bogus Exception"
    ...    def execute(self,x):
    ...        raise Exception, "Bogus Exception"
    ...
    >>> flow = mdp.Flow([BogusExceptNode()])

Switch on crash recovery
    
    >>> flow.set_crash_recovery(1)

Attempt to train the flow

    >>> flow.train(x) # doctest: +SKIP
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
      [...]
    mdp.linear_flows.FlowExceptionCR: 
    ----------------------------------------
    ! Exception in node #0 (BogusExceptNode):
    Node Traceback:
    Traceback (most recent call last):
      [...]
    Exception: Bogus Exception
    ----------------------------------------
    A crash dump is available on: "/tmp/MDPcrash_LmISO_.pic"

You can give a file name to tell the flow where to save the dump::

    >>> flow.set_crash_recovery('/home/myself/mydumps/MDPdump.pic')
