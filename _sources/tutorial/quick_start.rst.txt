.. _quick_start:

Quick Start
===========

.. include:: using_mdp_is_as_easy.rst

MDP requires the numerical Python extensions 
`NumPy <http://numpy.scipy.org/>`_ or `SciPy <http://www.scipy.org/>`_. At
import time MDP will select ``scipy`` if available, otherwise
``numpy`` will be loaded. You can force the use of a numerical
extension by setting the environment variable ``MDPNUMX=numpy`` or
``MDPNUMX=scipy``. 

.. admonition:: An important remark
    
   Input data is assumed to be a two-dimensional numpy array, such that 
   observations of variables are stored in the rows of the array, individual
   variables are stored in the columns. This means that one row contains one 
   particular observation/measurement of all variables, and one column contains
   all observations/measurements of one particular variable. 
   
   For example, let's call ``x``, ``y``, ``z`` the variables you are measuring and 
   ``x1``, ``x2``, ``x3``, ``x4`` different observations/measurements of variable ``x``,
   for example taken at time ``t1``, ``t2``, ``t3``, ``t4``. 
   
   The input 2-D numpy array should look like this: ::

            x1 y1 z1
        X = x2 y2 z2
            x3 y3 z3
            x4 y4 z4

   In this case ``X[:,0]`` gives you all rows corresponding to column ``0``, i.e. all observations
   of variable ``x``: ``x1``, ``x2``, ``x3``, ``x4``.

   On the other hand ``X[0,:]`` gives you al columns corresponding to row ``0``, 
   i.e. all variables as they were measured at time ``1``: ``x1``, ``y1``, ``z1``.
