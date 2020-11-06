.. _additional_utilities:

====================
Additional utilities
====================

MDP offers some additional utilities of general interest
in the ``mdp.utils`` module. Refer to the
`API <http://mdp-toolkit.sourceforge.net/docs/api/index.html>`_
for the full documentation and interface description.

:api:`mdp.utils.CovarianceMatrix`
     This class stores an empirical covariance matrix that can be updated
     incrementally. A call to the ``fix`` method returns the current state
     of the covariance matrix, the average and the number of observations,
     and resets the internal data.

     Note that the internal sum is a standard ``__add__`` operation. We are not
     using any of the fancy sum algorithms to avoid round off errors when
     adding many numbers. If you want to contribute a ``CovarianceMatrix``
     class that uses such algorithms we would be happy to include it in
     MDP.  For a start see the `Python recipe
     <http://code.activestate.com/recipes/393090/>`_
     by Raymond Hettinger. For a
     review about floating point arithmetic and its pitfalls see
     *What every computer scientist should know about floating-point
     arithmetic* by David Goldberg, ACM Computing Surveys, Vol 23, No
     1, March 1991.

:api:`mdp.utils.VartimeCovarianceMatrix`
     This class stores an empirical covariance matrix that can be updated
     incrementally. A call to the ``fix`` method returns the current state
     of the covariance matrix, the average and the number of observations,
     and resets the internal data.

     As compared to the ``CovarianceMatrix`` class, this class accepts sampled
     input in conjunction with a non-constant time increment between samples.
     The covariance matrix is then computed as a (centered) scalar product
     between functions, that is sampled unevenly, using the trapezoid rule.

:api:`mdp.utils.DelayCovarianceMatrix`
     This class stores an empirical covariance matrix between the signal and
     time delayed signal that can be updated incrementally.

:api:`mdp.utils.MultipleCovarianceMatrices`
     Container class for multiple covariance matrices to easily
     execute operations on all matrices at the same time.

:api:`mdp.utils.dig_node` (node)
    Crawl recursively an MDP ``Node`` looking for arrays.
    Return (dictionary, string), where the dictionary is:
    { attribute_name: (size_in_bytes, array_reference)}
    and string is a nice string representation of it.

:api:`mdp.utils.get_node_size` (node)
    Get ``node`` total byte-size using ``cPickle`` with protocol=2.
    (The byte-size is related the memory needed by the node).

:api:`mdp.utils.progressinfo` (sequence, length, style, custom)
    A fully configurable text-mode progress info box tailored to the
    command-line die-hards.
    To get a progress info box for your loops use it like this::

         >>> for i in progressinfo(sequence):
         ...     do_something(i)

    You can also use it with generators, files or any other iterable object,
    but in this case you have to specify the total length of the sequence::

        >>> for line in progressinfo(open_file, nlines):
        ...     do_something(line)

    A few examples of the available layouts::

        [===================================73%==============>...................]

        Progress:  67%[======================================>                   ]

        23% [02:01:28] - [00:12:37]

:api:`mdp.utils.QuadraticForm`
    Define an inhomogeneous quadratic form as ``1/2 x'Hx + f'x + c``.
    This class implements the quadratic form analysis methods
    presented in:
    Berkes, P. and Wiskott, L. On the analysis and interpretation
    of inhomogeneous quadratic forms as receptive fields. *Neural
    Computation*, 18(8): 1868-1895. (2006).


:api:`mdp.utils.refcast` (array, dtype)
    Cast the array to ``dtype`` only if necessary,
    otherwise return a reference.

:api:`mdp.utils.rotate` (mat, angle, columns, units)
    Rotate in-place a NxM data matrix in the plane defined by the ``columns``
    when observation are stored on rows. Observations are rotated
    counterclockwise. This corresponds to the following matrix-multiplication
    for each data-point (unchanged elements omitted)::

         [  cos(angle) -sin(angle)     [ x_i ]
            sin(angle)  cos(angle) ] * [ x_j ]

:api:`mdp.utils.random_rot` (dim, dtype)
    Return a random rotation matrix, drawn from the Haar distribution
    (the only uniform distribution on SO(n)).
    The algorithm is described in the paper
    Stewart, G.W., *The efficient generation of random orthogonal
    matrices with an application to condition estimators*, SIAM Journal
    on Numerical Analysis, 17(3), pp. 403-409, 1980.
    For more information see this `Wikipedia entry
    <http://en.wikipedia.org/wiki/Orthogonal_matrix#Randomization>`_.

:api:`mdp.utils.symeig_semidefinite_ldl` (A, B, eigenvectors, turbo, rng, type, overwrite, rank_threshold, dfc_out)
    LDL-based routine to solve generalized symmetric positive semidefinite
    eigenvalue problems.
    This can be used in case the normal ``symeig()`` call in 
    ``_stop_training()`` throws
    ``SymeigException ('Covariance matrices may be singular')``.

    This solver uses SciPy's raw LAPACK interface to access LDL decomposition.

    Roughly as efficient as ordinary eigenvalue solving. Can exploit range
    parameter for performance just as well as the backend for ordinary symmetric
    eigenvalue solving enables. This is the recommended and most efficient
    approach, but it requires SciPy 1.0 or newer.

:api:`mdp.utils.symeig_semidefinite_pca` (A, B, eigenvectors, turbo, range, type, overwrite, rank_threshold, dfc_out)
    PCA-based routine to solve generalized symmetric positive semidefinite
    eigenvalue problems.
    This can be used in case the normal ``symeig()``
    call in ``_stop_training()`` throws
    ``SymeigException ('Covariance matrices may be singular')``.

    It applies PCA to B and filters out rank deficit before it applies
    symeig() to A.
    It is roughly twice as expensive as the ordinary eigh implementation.

    One of the most stable and accurate approaches.
    Roughly twice as expensive as ordinary symmetric eigenvalue solving as
    it solves two symmetric eigenvalue problems.
    Only the second one can exploit range parameter for performance.

:api:`mdp.utils.symeig_semidefinite_reg` (A, B, eigenvectors, turbo, range, type, overwrite, rank_threshold, dfc_out)
    Regularization-based routine to solve generalized symmetric positive
    semidefinite eigenvalue problems.
    This can be used in case the normal ``symeig()``
    call in ``_stop_training()`` throws
    ``SymeigException ('Covariance matrices may be singular')``.

    This solver applies a moderate regularization to B before applying
    eigh/symeig. Afterwards it properly detects the rank deficit and
    filters out malformed features.
    For full range, this procedure is (approximately) as efficient as the
    ordinary eigh implementation, because all additional steps are
    computationally cheap.
    For shorter range, the LDL method should be preferred.

    Roughly as efficient as ordinary eigenvalue solving if no range is given.
    If range is given, depending on the backend for ordinary symmetric
    eigenvalue solving, this method can be much slower than an ordinary
    symmetric eigenvalue solver that can exploit range for performance.

:api:`mdp.utils.symeig_semidefinite_svd` (A, B, eigenvectors, turbo, range, type, overwrite, rank_threshold, dfc_out)
    SVD-based routine to solve generalized symmetric positive semidefinite
    eigenvalue problems.
    This can be used in case the normal ``symeig()``
    call in ``_stop_training()`` throws
    ``SymeigException ('Covariance matrices may be singular')``.

    One of the most stable and accurate approaches.
    Involves solving two svd problems. Computational cost can vary greatly
    depending on the backends used. E.g. SVD from SciPy appears to be much
    faster than SVD from NumPy. Based on this it can be faster or slower
    than the PCA based approach.

:api:`mdp.utils.symrand` (dim_or_eigv, dtype)
    Return a random symmetric (Hermitian) matrix with eigenvalues
    uniformly distributed on (0,1].

HTML Slideshows
---------------

The ``mdp.utils`` module contains some classes and helper function to
display animated results in a Webbrowser. This works by creating an
HTML file with embedded JavaScript code, which dynamically loads
image files (the images contain the content that you want to animate
and can for example be created with matplotlib).
MDP internally uses the open source `Templete templating libray,
written by David Bau <http://davidbau.com/downloads/templet.py>`_.

The easiest way to create a slideshow it to use one of these two helper
function:

:api:`mdp.utils.show_image_slideshow` (filenames, image_size, filename=None, title=None, \*\*kwargs)
    Write the slideshow into a HTML file, open it in the browser and
    return the file name. ``filenames`` is a list of the images files
    that you want to display in the slideshow. ``image_size`` is a
    2-tuple containing the width and height at which the images should
    be displayed. There are also a couple of additional arguments,
    which are documented in the docstring.

:api:`mdp.utils.image_slideshow` (filenames, image_size, title=None, \*\*kwargs)
    This function is similar to ``show_image_slideshow``, but it simply
    returns the slideshow HTML code (including the JavaScript code)
    which you can then embed into your own HTML file. Note that
    the default slideshow CSS code is not included, but it can be
    accessed in ``mdp.utils.IMAGE_SLIDESHOW_STYLE``.

Note that there are also two demos in the Examples section :ref:`slideshow`.

Graph module
------------

MDP contains ``mdp.graph``, a lightweight package to handle directed graphs.

:api:`mdp.graph.Graph`
    Represent a directed graph. This class contains several methods
    to create graph structures and manipulate them, among which

    - ``add_tree``: Add a tree to the graph.
        The tree is specified with a nested list of tuple, in a LISP-like
        notation. The values specified in the list become the values of
        the single nodes.
        Return an equivalent nested list with the nodes instead of the values.

        Example:::

          >>> g = mdp.graph.Graph()
          >>> a = b = c = d = e = None
          >>> nodes = g.add_tree( (a, b, (c, d ,e)) )

        Graph ``g`` corresponds to this tree, with all node values
        being ``None``::

                  a
                 / \
                b   c
                   / \
                  d   e

    - ``topological_sort``: Perform a topological sort of the nodes.

    - ``dfs``, ``undirected_dfs``: Perform Depth First sort.

    - ``bfs``, ``undirected_bfs``: Perform Breadth First sort.

    - ``connected_components``: Return a list of lists containing
      the nodes of all connected components of the graph.

    - ``is_weakly_connected``: Return True if the graph is weakly connected.

:api:`mdp.graph.GraphEdge`
    Represent a graph edge and all information attached to it.

:api:`mdp.graph.GraphNode`
    Represent a graph node and all information attached to it.

:api:`mdp.graph.recursive_map` (fun, seq)
    Apply a function recursively on a sequence and all subsequences.

:api:`mdp.graph.recursive_reduce` (func, seq, \*argv)
    Apply ``reduce(func, seq)`` recursively to a sequence and all its
    subsequences.
