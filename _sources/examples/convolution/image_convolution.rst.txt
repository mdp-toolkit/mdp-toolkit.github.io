.. _convolution2D:

Fast image filtering using the caching extension
================================================
.. codesnippet::

Here is an example of how to convolve an image with oriented
filters. 2D convolution is notoriously a slow operation; we'll show
how to improve the filtering speed using the caching extension.

For our example, we'll use the famous image of Lena

    >>> import mdp
    >>> import numpy
    >>> import os
    >>> import matplotlib
    >>> matplotlib.rcParams['examples.directory'] = os.path.join(os.path.dirname(matplotlib.rcParams['datapath']), 'sample_data')
    >>> import pylab
    >>> from matplotlib.cbook import get_sample_data
    >>> im = pylab.imread(get_sample_data("ada.png"))
    >>> # transform to grayscale
    >>> im = numpy.sqrt((im[:,:,:3]**2.).mean(2))

.. image:: lena_gray.png
        :width: 400
        :alt: Lena's famous photograph

First, we create a bank of Gabor filters at different orientations

    >>> # create Gabor filters bank
    >>> pi = numpy.pi
    >>> orientations = [0., pi/4., pi/2., pi*3./4.]
    >>> freq = 1./10    # frequency
    >>> phi = pi/2.     # phase
    >>> size = (20, 20) # in pixels
    >>> sgm = (5., 3.)  # standard deviation of the axes
    >>> 
    >>> nfilters = len(orientations)
    >>> gabors = numpy.empty((nfilters, size[0], size[1]))
    >>> for i, alpha in enumerate(orientations):
    ...     gabors[i,:,:] = mdp.utils.gabor(size, alpha, phi, freq, sgm)
    

.. image:: gabor_filters.png
        :width: 500
        :alt: The four Gabor filters

To convolve the image, we use the ``Convolution2DNode`` as follows

    >>> node = mdp.nodes.Convolution2DNode(gabors, mode='valid', boundary='fill',
    ...                                    fillvalue=0, output_2d=False)
    >>> cim = node.execute(im[numpy.newaxis,:,:])

obtaining these filtered images

.. image:: filtered_lena.png
        :width: 600
        :alt: Lena filtered by Gabors

To demonstrate how to use the caching extension, we'll pretend we have
several images by copying Lena several times, and measure the 
filtering performance with and without cache

    >>> x = mdp.utils.lrep(im, 3)
    >>> # set up a Timer object to measure performance
    >>> from timeit import Timer # doctest: +SKIP
    >>> timer = Timer("node.execute(x)", "from __main__ import node, x") # doctest: +SKIP
    >>> # first uncached execution
    >>> print timer.repeat(1, 1), 'sec' # doctest: +SKIP
    6.91 sec
    >>>
    >>> # now activating the cache on the Convolution2DNode class:
    >>> with mdp.caching.cache(cache_classes=[mdp.nodes.Convolution2DNode]): # doctest: +SKIP
    >>>    # second execution, uncached if it's the first time the script is run
    >>>    print timer.repeat(1, 1), 'sec' # doctest: +SKIP
    >>>    # third execution, this time cached
    >>>    print timer.repeat(1, 1), 'sec' # doctest: +SKIP
    7.05 sec
    39.6 msec

That's a 178 times improvement!




