.. _binetdbn:
.. _dbn:

========================================
Deep Belief Network (DBN) based on BiMDP
========================================

.. toctree::
   :hidden:

   dbn_nodes.rst
   dbn_binodes.rst
   dbn_binodes_coroutine_old.rst
   dbn_binodes_statemachine_old.rst
   test_dbnnodes.rst

.. codesnippet::

written by Pietro Berkes and Niko Wilbert

This is only a proof-of-concept, so don't expect the DBN to actually work!
Its current pupose is to experiment with different binet features.

Run this demo to view an HTML inspection of the DBN training.
This should help with understanding how the implementation works.

:ref:`dbn_nodes` — This is the original non-bimdp DBN node
from Pietro, which is the basis for the BiMDP DBN implementation and
is required for this example to run.

>>> import mdp
>>> import bimdp
>>> import dbn_binodes

create DBN

>>> n_layers = 2
>>> flow = dbn_binodes.get_DBN_flow(2, hidden_dims=[2,2])

create data

>>> n_samples = 10000  # number of data points
>>> n_greedy_reps = 100  # repetitions in greedy phase
>>> x = mdp.numx.zeros((n_samples, 4))
>>> for i in range(n_samples):
...     r = mdp.numx.rand()
...     if r>0.666:
...         x[i,:] = [0.,1.,0.,1.]
...     elif r>0.333:
...         x[i,:] = [1.,0.,1.,0.]

n_layers iterables plus one iterable for the DBNMasterBiNode

>>> data_iterables = [None] + [[x] * n_greedy_reps] * n_layers + [[x]]
>>> msg_iterables = ([None] +
...                  [[{"epsilon": 0.1, "decay": 0.0,
...                     "momentum": 0.0}] * n_greedy_reps] * n_layers +
...                  [[{"top_updates": 3, "epsilon": 0.1, "decay": 0.0,
...                     "momentum": 0.0,
...                     "max_iter": 2, "min_error": -1.0}]])

perform and visualize the training

>>> bimdp.show_training(flow, data_iterables, msg_iterables, debug=True)   # doctest: +ELLIPSIS
'/tmp/.../training_inspection.html'
>>> print "done."
done.

Other files:

:ref:`dbn_nodes`
	This is the original non-bimdp DBN node from Pietro, which is
        the basis for the BiMDP DBN implementation.
:ref:`dbn_binodes`
        The current BiMDP implementation of the DBN,
	based on the coroutine decorator for easy continuation.
:ref:`dbn_binodes_coroutine_old`
        Older version based on a coroutine, but without
	using the coderoator. This might still be useful to understand how the
	codecorator actually works.
:ref:`dbn_binodes_statemachine_old`
	Older version based on a state machine implementation.
