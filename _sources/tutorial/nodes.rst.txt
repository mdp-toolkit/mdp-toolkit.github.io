.. _nodes:

=====
Nodes
=====
.. codesnippet::

A *node* is the basic building block of an MDP application.  It
represents a data processing element, for example a learning
algorithm, a data filter, or a visualization step (see the :ref:`node_list` 
section for an exhaustive list and references).

Each node can have one or more *training phases*, during which the
internal structures are learned from training data (e.g. the weights
of a neural network are adapted or the covariance matrix is estimated)
and an *execution phase*, where new data can be processed forwards (by
processing the data through the node) or backwards (by applying the
inverse of the transformation computed by the node if defined).

Nodes have been designed to be applied to arbitrarily long sets of data;
provided the underlying algorithms support it, the internal structures can
be updated incrementally by sending multiple batches of data (this is
equivalent to online learning if the chunks consists of single
observations, or to batch learning if the whole data is sent in a
single chunk). This makes it possible to perform computations on large amounts
of data that would not fit into memory and to generate data on-the-fly.

A :api:`~mdp.Node` also defines some utility methods, for example
:api:`~mdp.Node.copy`, which returns an exact copy of a node,  and
:api:`~mdp.Node.save`, which writes to
in a file. Additional methods may also be present, depending on the
algorithm.

 
Node Instantiation
------------------

A node can be obtained by creating an instance of the ``Node`` class.

Each node is characterized by an input dimension (i.e., the
dimensionality of the input vectors), an output dimension, and a
``dtype``, which determines the numerical type of the internal
structures and of the output signal. By default, these attributes are
inherited from the input data if left unspecified. The constructor of
each node class can require other task-specific arguments. The full
documentation is always available in the doc-string of the node's
class.

Some examples of node instantiation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a node that performs Principal Component Analysis (PCA) 
whose input dimension and ``dtype``
are inherited from the input data during training. Output dimensions
default to input dimensions.

    >>> pcanode1 = mdp.nodes.PCANode()
    >>> pcanode1
    PCANode(input_dim=None, output_dim=None, dtype=None)
      
Setting ``output_dim = 10`` means that the node will keep only the 
first 10 principal components of the input.

    >>> pcanode2 = mdp.nodes.PCANode(output_dim=10)
    >>> pcanode2
    PCANode(input_dim=None, output_dim=10, dtype=None)

The output dimensionality can also be specified in terms of the explained
variance. If we want to keep the number of principal components which can 
account for 80% of the input variance, we set

    >>> pcanode3 = mdp.nodes.PCANode(output_dim=0.8)
    >>> pcanode3.desired_variance
    0.8

If ``dtype`` is set to ``float32`` (32-bit float), the input 
data is cast to single precision when received and the internal 
structures are also stored as ``float32``. ``dtype`` influences the 
memory space necessary for a node and the precision with which the 
computations are performed.

    >>> pcanode4 = mdp.nodes.PCANode(dtype='float32')
    >>> pcanode4
    PCANode(input_dim=None, output_dim=None, dtype='float32')

You can obtain a list of the numerical types supported by a node
looking at its ``supported_dtypes`` property

    >>> pcanode4.supported_dtypes             # doctest: +ELLIPSIS
    [dtype('float32'), dtype('float64')...]

.. supported_dtypes includes float96 on 32 bit, and float128 otherwise

This attribute is a list of ``numpy.dtype`` objects.


A ``PolynomialExpansionNode`` expands its input in the space
of polynomials of a given degree by computing all monomials up
to the specified degree. Its constructor needs as first argument
the degree of the polynomials space (3 in this case):

    >>> expnode = mdp.nodes.PolynomialExpansionNode(3)

Node Training
-------------

Some nodes need to be trained to perform their task. For example, the
Principal Component Analysis (PCA) algorithm requires the computation
of the mean and covariance matrix of a set of training data from which
the principal eigenvectors of the data distribution are estimated.

This can be done during a training phases by calling the ``train``
method.  MDP supports both supervised and unsupervised training, and
algorithms with multiple training phases.

Some examples of node training:

Create some random data to train the node

   >>> x = np.random.random((100, 25))  # 25 variables, 100 observations

Analyzes the batch of data ``x`` and update the estimation of 
mean and covariance matrix

    >>> pcanode1.train(x)

At this point the input dimension and the ``dtype`` have been
inherited from ``x``

    >>> pcanode1
    PCANode(input_dim=25, output_dim=None, dtype='float64')

We can train our node with more than one chunk of data. This
is especially useful when the input data is too long to
be stored in memory or when it has to be created on-the-fly.
(See also the :ref:`iterables` section)

    >>> for i in range(100):
    ...     x = np.random.random((100, 25))
    ...     pcanode1.train(x)

Some nodes don't need to or cannot be trained

    >>> expnode.is_trainable()
    False
  
Trying to train them anyway would raise 
an ``IsNotTrainableException``.

The training phase ends when the ``stop_training``, ``execute``,
``inverse``, and possibly some other node-specific methods are called.
For example we can finalize the PCA algorithm by computing and selecting
the principal eigenvectors

    >>> pcanode1.stop_training()

If the ``PCANode`` was declared to have a number of output components 
dependent on the input variance to be explained, we can check after
training the number of output components and the actually explained variance

    >>> pcanode3.train(x)
    >>> pcanode3.stop_training()
    >>> pcanode3.output_dim # doctest: +SKIP
    16
    >>> pcanode3.explained_variance # doctest: +SKIP
    0.85261144755506446 

It is now possible to access the trained internal data. In general,
a list of the interesting internal attributes can be found in the
class documentation.

    >>> avg = pcanode1.avg            # mean of the input data
    >>> v = pcanode1.get_projmatrix() # projection matrix

Some nodes, namely the one corresponding to supervised algorithms, e.g.
Fisher Discriminant Analysis (FDA), may need some labels or other
supervised signals to be passed
during training. Detailed information about the signature of the 
``train`` method can be read in its doc-string.

    >>> fdanode = mdp.nodes.FDANode()
    >>> for label in ['a', 'b', 'c']:
    ...     x = np.random.random((100, 25))
    ...     fdanode.train(x, label)


A node could also require multiple training phases. For example, the
training of ``fdanode`` is not complete yet, since it has two
training phases: The first one computing the mean of the data
conditioned on the labels, and the second one computing the overall
and within-class covariance matrices and solving the FDA
problem. The first phase must be stopped and the second one trained

    >>> fdanode.stop_training()
    >>> for label in ['a', 'b', 'c']:
    ...     x = np.random.random((100, 25))
    ...     fdanode.train(x, label)

The easiest way to train multiple phase nodes is using flows,
which automatically handle multiple phases (see the :ref:`flows` section).


Node Execution
--------------

Once the training is finished, it is possible to execute the node:

The input data is projected on the principal components learned
in the training phase

    >>> x = np.random.random((100, 25))
    >>> y_pca = pcanode1.execute(x)

Calling a node instance is equivalent to executing it

    >>> y_pca = pcanode1(x)

The input data is expanded in the space of polynomials of
degree 3

    >>> x = np.random.random((100, 5))
    >>> y_exp = expnode(x)

The input data is projected to the directions learned by FDA

    >>> x = np.random.random((100, 25))
    >>> y_fda = fdanode(x)

Some nodes may allow for optional arguments in the ``execute`` method. 
As always the complete information can be found in the doc-string.

Node Inversion
-------------- 

If the operation computed by the node is invertible, the node can also
be executed *backwards*, thus computing the inverse transformation:

In the case of PCA, for example, this corresponds to projecting a
vector in the principal components space back to the original data
space

    >>> pcanode1.is_invertible()
    True
    >>> x = pcanode1.inverse(y_pca)


The expansion node in not invertible

    >>> expnode.is_invertible()
    False
  
Trying to compute the inverse would raise an ``IsNotInvertibleException``.


.. _write-your-own-nodes:

Writing your own nodes: subclassing ``Node``
--------------------------------------------

MDP tries to make it easy to write new nodes that interface with the
existing data processing elements. 

The ``Node`` class is designed to make the implementation of new
algorithms easy and intuitive. This base class takes care of setting
input and output dimension and casting the data to match the numerical
type (e.g. ``float`` or ``double``) of the internal variables, and offers
utility methods that can be used by the developer.

To expand the MDP library of implemented nodes with user-made nodes,
it is sufficient to subclass ``Node``, overriding some of
the methods according to the algorithm one wants to implement,
typically the ``_train``, ``_stop_training``, and ``_execute``
methods.

In its namespace MDP offers references to the main modules ``numpy``
or ``scipy``, and the subpackages ``linalg``, ``random``, and ``fft``
as ``mdp.numx``, ``mdp.numx_linalg``, ``mdp.numx_rand``, and
``mdp.numx_fft``. This is done to possibly support additional
numerical extensions in the future. For this reason it is recommended
to refer to the ``numpy`` or ``scipy`` numerical extensions through
the MDP aliases ``mdp.numx``, ``mdp.numx_linalg``, ``mdp.numx_fft``,
and ``mdp.numx_rand`` when writing ``Node`` subclasses. This shall
ensure that your nodes can be used without modifications should MDP
support alternative numerical extensions in the future.

We'll illustrate all this with some toy examples.

We start by defining a node that multiplies its input by 2.
  
Define the class as a subclass of ``Node``::
  
    >>> class TimesTwoNode(mdp.Node):

This node cannot be trained. To specify this, one has to overwrite
the ``is_trainable`` method to return False::
  
    ...     def is_trainable(self):
    ...         return False
  
Execute only needs to multiply ``x`` by 2::

    ...     def _execute(self, x):
    ...         return 2*x

Note that the ``execute`` method, which should never be overwritten
and which is inherited from the ``Node`` parent class, will perform
some tests, for example to make sure that ``x`` has the right rank,
dimensionality and casts it to have the right ``dtype``.  After that
the user-supplied ``_execute`` method is called.  Each subclass has
to handle the ``dtype`` defined by the user or inherited by the
input data, and make sure that internal structures are stored
consistently. To help with this the ``Node`` base class has a method
called ``_refcast(array)`` that casts the input ``array`` only when its
``dtype`` is different from the ``Node`` instance's ``dtype``.

The inverse of the multiplication by 2 is of course the division by 2
::

    ...     def _inverse(self, y): 
    ...         return y/2 


Test the new node
    
    >>> class TimesTwoNode(mdp.Node):
    ...      def is_trainable(self): 
    ...          return False
    ...      def _execute(self, x):
    ...          return 2*x
    ...      def _inverse(self, y):
    ...          return y/2
    >>> node = TimesTwoNode(dtype = 'float32')
    >>> x = mdp.numx.array([[1.0, 2.0, 3.0]])
    >>> y = node(x)
    >>> print x, '* 2 =  ', y
    [[ 1.  2.  3.]] * 2 =   [[ 2.  4.  6.]]
    >>> print y, '/ 2 =', node.inverse(y)
    [[ 2.  4.  6.]] / 2 = [[ 1.  2.  3.]]

We then define a node that raises the input to the power specified
in the initialiser::

    >>> class PowerNode(mdp.Node): 

We redefine the init method to take the power as first argument.
In general one should always give the possibility to set the ``dtype``
and the input dimensions. The default value is ``None``, which means that
the exact value is going to be inherited from the input data::

    ...     def __init__(self, power, input_dim=None, dtype=None): 
  
Initialize the parent class::

    ...         super(PowerNode, self).__init__(input_dim=input_dim, dtype=dtype) 

Store the power::

    ...         self.power = power 

``PowerNode`` is not trainable::

    ...     def is_trainable(self):  
    ...         return False 

nor invertible::

    ...     def is_invertible(self):  
    ...         return False 

It is possible to overwrite the function ``_get_supported_dtypes``
to return a list of ``dtype`` supported by the node::

    ...     def _get_supported_dtypes(self): 
    ...         return ['float32', 'float64'] 

The supported types can be specified in any format allowed by the
``numpy.dtype`` constructor. The interface method ``get_supported_dtypes``
converts them and sets the property ``supported_dtypes``, which is
a list of ``numpy.dtype`` objects.

The ``_execute`` method::

    ...     def _execute(self, x): 
    ...         return self._refcast(x**self.power) 
 
Test the new node

    >>> class PowerNode(mdp.Node):
    ...     def __init__(self, power, input_dim=None, dtype=None):
    ...         super(PowerNode, self).__init__(input_dim=input_dim, dtype=dtype)
    ...         self.power = power
    ...     def is_trainable(self): 
    ...         return False
    ...     def is_invertible(self): 
    ...         return False
    ...     def _get_supported_dtypes(self):
    ...         return ['float32', 'float64']
    ...     def _execute(self, x):
    ...         return self._refcast(x**self.power)
    >>> node = PowerNode(3)
    >>> x = mdp.numx.array([[1.0, 2.0, 3.0]])
    >>> y = node(x)
    >>> print x, '**', node.power, '=', node(x)
    [[ 1.  2.  3.]] ** 3 = [[  1.   8.  27.]]

We now define a node that needs to be trained. The ``MeanFreeNode``
computes the mean of its training data and subtracts it from the input
during execution::

    >>> class MeanFreeNode(mdp.Node): 
    ...     def __init__(self, input_dim=None, dtype=None): 
    ...         super(MeanFreeNode, self).__init__(input_dim=input_dim,  
    ...                                            dtype=dtype) 

We store the mean of the input data in an attribute. We initialize it
to ``None`` since we still don't know how large is an input vector::

    ...         self.avg = None 

Same for the number of training points::

    ...         self.tlen = 0 
    
The subclass only needs to overwrite the ``_train`` method, which
will be called by the parent ``train`` after some testing and casting has
been done::

    ...     def _train(self, x): 
    ...         # Initialize the mean vector with the right  
    ...         # size and dtype if necessary: 
    ...         if self.avg is None: 
    ...             self.avg = mdp.numx.zeros(self.input_dim, 
    ...                                       dtype=self.dtype) 
         
Update the mean with the sum of the new data::

    ...         self.avg += mdp.numx.sum(x, axis=0) 
 
Count the number of points processed::

    ...         self.tlen += x.shape [0]

Note that the ``train`` method can have further arguments, which might be
useful to implement algorithms that require supervised learning.
For example, if you want to define a node that performs some form
of classification you can define a ``_train(self, data, labels)``
method. The parent ``train`` checks ``data`` and takes care to pass
the ``labels`` on (cf. for example ``mdp.nodes.FDANode``).

The ``_stop_training`` function is called by the parent ``stop_training`` 
method when the training phase is over. We divide the sum of the training 
data by the number of training vectors to obtain the mean::

    ...     def _stop_training(self): 
    ...         self.avg /= self.tlen 
    ...         if self.output_dim is None: 
    ...             self.output_dim = self.input_dim 

Note that we ``input_dim`` are set automatically by the ``train`` method,
and we want to ensure that the node has ``output_dim`` set after training.
For nodes that do not need training, the setting is performed automatically
upon execution. The ``_execute`` and ``_inverse`` methods::

    ...     def _execute(self, x): 
    ...         return x - self.avg 
    ...     def _inverse(self, y): 
    ...         return y + self.avg 

Test the new node

    >>> class MeanFreeNode(mdp.Node):
    ...     def __init__(self, input_dim=None, dtype=None):
    ...         super(MeanFreeNode, self).__init__(input_dim=input_dim, 
    ...                                            dtype=dtype)
    ...         self.avg = None
    ...         self.tlen = 0
    ...     def _train(self, x):
    ...         # Initialize the mean vector with the right 
    ...         # size and dtype if necessary:
    ...         if self.avg is None:
    ...             self.avg = mdp.numx.zeros(self.input_dim,
    ...                                       dtype=self.dtype)
    ...         self.avg += mdp.numx.sum(x, axis=0)
    ...         self.tlen += x.shape[0]
    ...     def _stop_training(self):
    ...         self.avg /= self.tlen
    ...         if self.output_dim is None:
    ...             self.output_dim = self.input_dim
    ...     def _execute(self, x):
    ...         return x - self.avg
    ...     def _inverse(self, y):
    ...         return y + self.avg
    >>> node = MeanFreeNode()
    >>> x = np.random.random((10,4))
    >>> node.train(x)
    >>> y = node(x)
    >>> print 'Mean of y (should be zero):\n', np.abs(np.around(np.mean(y, 0), 15))
    Mean of y (should be zero):
    [ 0.  0.  0.  0.]

It is also possible to define nodes with multiple training phases.
In such a case, calling the ``train`` and ``stop_training`` functions
multiple times is going to execute successive training phases
(this kind of node is much easier to train using :ref:`flows`).
Here we'll define a node that returns a meanfree, unit variance signal.
We define two training phases: first we compute the mean of the
signal and next we sum the squared, meanfree input to compute
the standard deviation  (of course it is possible to solve this
problem in one single step - remember this is just a toy example).
::

    >>> class UnitVarianceNode(mdp.Node):
    ...     def __init__(self, input_dim=None, dtype=None):
    ...         super(UnitVarianceNode, self).__init__(input_dim=input_dim, 
    ...                                                dtype=dtype)
    ...         self.avg = None # average
    ...         self.std = None # standard deviation
    ...         self.tlen = 0

The training sequence is defined by the user-supplied method
``_get_train_seq``, that returns a list of tuples, one for each
training phase. The tuples contain references to the training
and stop-training methods of each of them. The default output
of this method is ``[(_train, _stop_training)]``, which explains
the standard behavior illustrated above. We overwrite the method to
return the list of our training/stop_training methods::

    ...     def _get_train_seq(self):
    ...         return [(self._train_mean, self._stop_mean),
    ...                 (self._train_std, self._stop_std)]

Next we define the training methods. The first phase is identical
to the one in the previous example::

    ...     def _train_mean(self, x):
    ...         if self.avg is None:
    ...             self.avg = mdp.numx.zeros(self.input_dim,
    ...                                       dtype=self.dtype)
    ...         self.avg += mdp.numx.sum(x, 0)
    ...         self.tlen += x.shape[0]
    ...     def _stop_mean(self):
    ...         self.avg /= self.tlen

The second one is only marginally different and does not require many
explanations::

    ...     def _train_std(self, x):
    ...         if self.std is None:
    ...             self.tlen = 0
    ...             self.std = mdp.numx.zeros(self.input_dim,
    ...                                       dtype=self.dtype)
    ...         self.std += mdp.numx.sum((x - self.avg)**2., 0)
    ...         self.tlen += x.shape[0]
    ...     def _stop_std(self):
    ...         # compute the standard deviation
    ...         self.std = mdp.numx.sqrt(self.std/(self.tlen-1))

The ``_execute`` and ``_inverse`` methods are not surprising, either::

    ...     def _execute(self, x):
    ...         return (x - self.avg)/self.std
    ...     def _inverse(self, y):
    ...         return y*self.std + self.avg


Test the new node

    >>> class UnitVarianceNode(mdp.Node):
    ...     def __init__(self, input_dim=None, dtype=None):
    ...         super(UnitVarianceNode, self).__init__(input_dim=input_dim, 
    ...                                                 dtype=dtype)
    ...         self.avg = None # average
    ...         self.std = None # standard deviation
    ...         self.tlen = 0
    ...     def _get_train_seq(self):
    ...         return [(self._train_mean, self._stop_mean),
    ...                 (self._train_std, self._stop_std)]
    ...     def _train_mean(self, x):
    ...         if self.avg is None:
    ...             self.avg = mdp.numx.zeros(self.input_dim,
    ...                                       dtype=self.dtype)
    ...         self.avg += mdp.numx.sum(x, 0)
    ...         self.tlen += x.shape[0]
    ...     def _stop_mean(self):
    ...         self.avg /= self.tlen
    ...     def _train_std(self, x):
    ...         if self.std is None:
    ...             self.tlen = 0
    ...             self.std = mdp.numx.zeros(self.input_dim,
    ...                                       dtype=self.dtype)
    ...         self.std += mdp.numx.sum((x - self.avg)**2., 0)
    ...         self.tlen += x.shape[0]
    ...     def _stop_std(self):
    ...         # compute the standard deviation
    ...         self.std = mdp.numx.sqrt(self.std/(self.tlen-1))
    ...     def _execute(self, x):
    ...         return (x - self.avg)/self.std
    ...     def _inverse(self, y):
    ...         return y*self.std + self.avg
    >>> node = UnitVarianceNode()
    >>> x = np.random.random((10,4))
    >>> # loop over phases
    ... for phase in range(2):
    ...     node.train(x)
    ...     node.stop_training()
    ...
    ...
    >>> # execute
    ... y = node(x)
    >>> print 'Standard deviation of y (should be one): ', mdp.numx.std(y, axis=0, ddof=1)
    Standard deviation of y (should be one):  [ 1.  1.  1.  1.]
    

In our last example we'll define a node that returns two copies of its input.
The output is going to have twice as many dimensions.
::

    >>> class TwiceNode(mdp.Node):
    ...     def is_trainable(self): return False
    ...     def is_invertible(self): return False

When ``Node`` inherits the input dimension, output dimension, and ``dtype``
from the input data, it calls the methods ``set_input_dim``, 
``set_output_dim``, and ``set_dtype``. Those are the setters for
``input_dim``, ``output_dim`` and ``dtype``, which are Python 
`properties <http://www.python.org/download/releases/2.2/descrintro/#property>`_. 
If a subclass needs to change the default behavior, the internal methods
``_set_input_dim``, ``_set_output_dim`` and ``_set_dtype`` can
be overwritten. The property setter will call the internal method after
some basic testing and internal settings. The private methods 
``_set_input_dim``, ``_set_output_dim`` and ``_set_dtype`` are responsible
for setting the private attributes ``_input_dim``, ``_output_dim``,
and ``_dtype`` that contain the actual value.
  
Here we overwrite
``_set_input_dim`` to automatically set the output dimension to be twice the
input one, and ``_set_output_dim`` to raise an exception, since
the output dimension should not be set explicitly.
::

    ...     def _set_input_dim(self, n):
    ...         self._input_dim = n
    ...         self._output_dim = 2*n
    ...     def _set_output_dim(self, n):
    ...         raise mdp.NodeException, "Output dim can not be set explicitly!"

The ``_execute`` method::

    ...     def _execute(self, x):
    ...         return mdp.numx.concatenate((x, x), 1)


Test the new node

    >>> class TwiceNode(mdp.Node):
    ...     def is_trainable(self): return False
    ...     def is_invertible(self): return False
    ...     def _set_input_dim(self, n):
    ...         self._input_dim = n
    ...         self._output_dim = 2*n
    ...     def _set_output_dim(self, n):
    ...         raise mdp.NodeException, "Output dim can not be set explicitly!"
    ...     def _execute(self, x):
    ...         return mdp.numx.concatenate((x, x), 1)
    >>> node = TwiceNode()
    >>> x = mdp.numx.zeros((5,2))
    >>> x
    array([[ 0.,  0.],
           [ 0.,  0.],
           [ 0.,  0.],
           [ 0.,  0.],
           [ 0.,  0.]])
    >>> node.execute(x)
    array([[ 0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.]])
