.. _install:

.. |gE| unicode:: U+2265

************
Installation
************

You can install using :ref:`pip`, :ref:`binary packages <binary_packages>` or 
from :ref:`source <install_from_source>`.

.. _pip:

pip (Windows, MacOSX, Linux)
============================

MDP is listed in the `Python Package Index <http://pypi.python.org/pypi/MDP>`_ and can be
installed with ``pip``::

    pip install mdp

.. _binary_packages:

Binary packages (Linux)
=======================

Users of some Linux distributions (Debian, Ubuntu, Fedora, ...) can install the ``python3-mdp`` package using 
the distribution package manager.


.. _install_from_source:

Install the development version
===============================
If you want to live on the bleeding edge, check out the MDP git repositories.
You can either `browse the repository <https://github.com/mdp-toolkit/mdp-toolkit>`_
or directly install the development version from the repository with::

    pip install git+https://github.com/mdp-toolkit/mdp-toolkit.git


Optional Libraries
==================
MDP can make use of several additional libraries if they are installed on your
system. They are not required for using MDP, but may give more
functionality. Here a list of optional libraries and the corresponding
additional features in MDP:

* `SciPy <http://www.scipy.org/>`_ : Use the fast and
  efficient LAPACK wrapper for the symmetrical eigensolver, used
  interally by many nodes; use the fast FFT routines in some nodes;
  provide the ``Convolution2DNode``, using the fast convolution routines
  in SciPy.
* `LibSVM <http://www.csie.ntu.edu.tw/~cjlin/libsvm/>`_ :
  provide the ``LibSVMClassifier`` node.
* `joblib <http://packages.python.org/joblib/>`_ : provide the
  ``caching`` extension and the corresponding ``cache`` context
  manager.
* `scikit-learn <http://scikit-learn.org/stable/>`_ : provide
  wrapper nodes to several sklearn algorithms.

You can install all the additional libraries with pip::

    pip install scipy scikit-learn joblib libsvm


Testing
=======
If you have successfully installed MDP, you can test your installation in a
Python shell as follows::

    >>> import mdp
    >>> mdp.test()
    >>> import bimdp
    >>> bimdp.test()

Note that you will need to install `pytest <http://pytest.org>`_ to run the tests.

If some test fails, please file a `bug report
<https://github.com/mdp-toolkit/mdp-toolkit/issues>`_.
Optionally, report it to the `mailing list
<https://mail.python.org/mm3/mailman3/lists/mdp-toolkit.python.org/>`_.

License
=======

MDP is distributed under the open source `BSD license <https://github.com/mdp-toolkit/mdp-toolkit/blob/master/COPYRIGHT>`_.
