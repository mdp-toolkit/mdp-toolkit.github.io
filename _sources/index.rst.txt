.. toctree::
   :hidden:
   :maxdepth: 3

   install.rst
   documentation.rst
   how_to_cite_mdp.rst
   contact.rst

.. admonition:: News

  01.05.2020
     
     MDP 3.6 released!
     Some of the most compelling new features of MDP 3.6 are

     - A new online mode to enable use of MDP in reinforcement learning using
       OnlineNode, OnlineFlow and other new nodes.
       This notably includes incremental Slow Feature Analysis in IncSFANode.
     - SFA-based supervised learning, specifically graph-based SFA nodes
       GSFANode as well as iGSFANode, and hierarchical GSFA (HGSFA).
     - New solvers in SFA-node that are robust against rank deficiencies in the
       covariance matrix. This cures the common issue
       SymeigException ('Covariance matrices may be singular').
     - A new family of expansion nodes, including Legendre, Hermite and
       Chebyshev polynomials allows for numerically stable data expansion
       to high	 degrees.
     - VartimeSFANode supports SFA on data with non-constant time increments.
       This node is a pilot effort to support non-constant time increments in
       various mdp nodes.

     MDP 3.6 supports the newest versions of Python, NumPy, SciPy and
     scikit-learn. More specifically, it supports Python 3.5-3.8 and 2.7. It is
     the last release that officially supports Python 2.7.

     
.. middle-description-string::

.. include:: tutorial/using_mdp_is_as_easy.rst

To learn more about MDP, read through the :ref:`documentation`.
