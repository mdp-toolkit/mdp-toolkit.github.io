.. _examples:

Examples
========

.. toctree::
   :hidden:
   :maxdepth: 1

   logmap/logmap.rst
   lle/lle.rst
   gng/gng.rst
   convolution/image_convolution.rst
   scikits_learn/digit_classification.rst
   logo/logo_animation.rst
   bayes_guesser/bayes_guesser.rst
   word_generator/word_generator.rst
   slideshow/slideshow.rst
   gradnewton/gradnewton.rst
   binetdbn/dbn.rst
   bimdp_examples/bimdp_inverse.rst
   bimdp_examples/bimdp_hinet_inspection.rst
   bimdp_examples/bimdp_custom_inspection.rst

Here are examples on how to use MDP for typical machine learning
applications:

* :ref:`logmap` — Using Slow Feature Analysis (SFA) for
  processing a non-stationary time series, derived by a logistic map.
* :ref:`gng` — Capture the topological structure of a
  data distribution.
* :ref:`lle` — Approximate data with a low-dimensional surface
  and reduce its dimensionality by learning a mapping to the surface.
* :ref:`convolution2D` — Filter images with 2D wavelets and demonstrate use
  of caching extension.
* :ref:`digit_classification` — Use the combined power of MDP and scikits.learn
  in an applciation for handwritten digit classification

* `hinet_html.py`__ — Get the HTML representation for a simple hinet network.
* `benchmark_parallel.py`__ — Simple benchmark to compare the different
  schedulers in MDP.
* `pp_remote_test.py`__ — Simple test of the remote Parallel Python support,
  using the NetworkPPScheduler.
* :ref:`slideshow` and :ref:`slideshow_double` — Created slideshows of
  matplotlib plots, demonstrates the slideshow module in MDP.
* `hinetplaner`__ — Interactive HTML/JS/AJAX based GUI for constructing special
  hinet networks. This is a complicated example which won't teach you much
  about MDP.
* `mnist`__ — Several more example for handwritten digit classification,
  this time with Fisher Discriminant Analysis and without scikits.learn.

__ https://github.com/mdp-toolkit/mdp-docs/blob/master/source/examples/hinet_html.py
__ https://github.com/mdp-toolkit/mdp-docs/blob/master/source/examples/benchmark_parallel.py
__ https://github.com/mdp-toolkit/mdp-docs/blob/master/source/examples/pp_remote_test.py
__ https://github.com/mdp-toolkit/mdp-docs/tree/master/source/examples/hinetplaner
__ https://github.com/mdp-toolkit/mdp-docs/tree/master/source/examples/mnist

The following examples use and illustrate BiMDP.

* :ref:`bimdp_inverse` — A simple example on the alternative
  mechanism to inverse a BiFlow.
* :ref:`bimdp_hinet_inspection` — Demonstrates the inspection of
  a BiFlow.
* :ref:`bimdp_custom_inspection` — Customization with maptlotlib
  plots of the BiFlow inspection.
* `bimdp_simple_coroutine.py`__ — Minimal example for coroutine decorator.
* :ref:`gradnewton` — Use Newton's method for gradient descent
  with the gradient extension.
* `Backpropagation`__ — Implement backpropagation for a multi layer
  perceptron.
* :ref:`binetdbn` — Proof of concept for a Deep Belief Network.

__ https://github.com/mdp-toolkit/mdp-docs/blob/master/source/examples/bimdp_examples/bimdp_simple_coroutine.py
__ https://github.com/mdp-toolkit/mdp-docs/tree/master/source/examples/backpropagation
