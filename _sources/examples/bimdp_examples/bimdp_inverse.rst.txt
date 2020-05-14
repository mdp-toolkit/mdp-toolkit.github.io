.. _bimdp_inverse:

====================
BiMDP flow inversion
====================

.. codesnippet::

Example on how calculate the inverse of a BiFlow.

A BiFlow does inherit the 'inverse' method from the :api:`mdp.Flow` class, but
this doesn't support BiMDP features like messages. If these features are
needed then one can use an alternative way to calucalte the inverse, which
is presented here.

>>> import numpy as np
>>> import bimdp

Create a simple pointless flow

>>> pca_node = bimdp.nodes.PCABiNode()
>>> sfa_node = bimdp.nodes.SFABiNode()
>>> flow = pca_node + sfa_node
>>> x = np.random.random((50,5))
>>> flow.train(x)

>>> x = np.random.random((3,5))
>>> y, msg = flow.execute(x)

The target value 1 is the absolute index of the sfa_node,
alternatively one could have used a node_id

>>> inv_x, _ = flow.execute(y, {"method": "inverse"}, 1)
>>> #_, (inv_x, _) = bimdp.show_execution(flow, y, {"method": "inverse"}, 1)
>>> assert np.all(np.abs(x - inv_x) < 0.0000001)

Compare the result to the standard inverse

>>> inv2_x = flow.inverse(y)
>>> assert np.all(np.abs(inv2_x - inv_x) < 0.0000001)
