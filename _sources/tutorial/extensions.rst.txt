.. _extensions:

===============
Node Extensions
===============
.. codesnippet::

The node extension mechanism is an advanced topic, so you might want to
skip this section at first. The examples here partly use the ``parallel``
and ``hinet`` packages, which are explained later in the tutorial.

The node extension mechanism makes it possible to dynamically add methods or
class attributes for specific features to node classes (e.g. for
parallelization the nodes need a ``_fork`` and ``_join`` method). Note that
methods are just a special case of class attributes, the extension mechanism
treats them like any other class attributes.
It is also possible for users to define custom extensions
to introduce new functionality for MDP nodes without having to directly modify
any MDP code. The node extension mechanism basically enables some
form of *Aspect-oriented programming* (AOP) to deal with *cross-cutting
concerns* (i.e., you want to add a new aspect to node classes which are
spread all over MDP and possibly your own code). In the AOP terminology any
new methods you introduce contain *advice* and the *pointcut* is effectively
defined by the calling of these methods.

Without the extension mechanism the adding of new aspects to nodes would
be done through inheritance, deriving new node classes that implement
the aspect for the parent node class. This is fine unless one wants to use
multiple aspects, requiring multiple inheritance for every combination of
aspects one wants to use. Therefore this approach does not scale well with
the number of aspects.

The node extension mechanism does not directly depend on inheritance, 
instead it adds the methods or class attributes to the node classes 
dynamically at runtime (like *method injection*). This makes it possible 
to activate extensions just when they are needed, reducing the risk of 
interference between different extensions. One can also use multiple 
extensions at the same time, as long as there is no interference, i.e., 
both extensions do not use any attributes with the same name. 

The node extension mechanism uses a special Metaclass, which allows it to  
define the node extensions as classes derived from nodes (bascially just what
one would do without the extension mechanism).
This keeps the code readable and avoids some problems when using automatic
code checkers (like the background pylint checks in the
Eclipse IDE with PyDev).

In MDP the node extension mechanism is currently used by the ``parallel``
package and for the the HTML representation in the ``hinet`` package,
so the best way to learn more is to look there.
We also use these packages in the following examples.

Using Extensions
----------------

First of all you can get all the available node extensions by calling
the ``get_extensions`` function, or to get just a list of their names use
``get_extensions().keys()``. Be careful not to modify the dict returned
by ``get_extensions``, since this will actually modify the registered
extensions. The currently activated extensions are returned
by ``get_active_extensions``. To activate an extension use
``activate_extension``, e.g. to activate the parallel extension
write:

    >>> mdp.activate_extension("parallel")
    >>> # now you can use the added attributes / methods
    >>> mdp.deactivate_extension("parallel")
    >>> # the additional attributes are no longer available

.. Note::
    As a user you will never have to activate the parallel extension yourself,
    this is done automatically by the ``ParallelFlow`` class. The parallel
    package will be explained later, it is used here only as an example.
    
Activating an extension adds the available extensions attributes to the 
supported nodes. MDP also provides a context manager for the 
``with`` statement:

    >>> with mdp.extension("parallel"):
    ...     pass

The ``with`` statement ensures that the activated extension is deactivated
after the code block, even if there is an exception.
But the deactivation at the end happens only for the extensions that were
activated by this context manager (not for those that were already active
when the context was entered). This prevents unintended side effects.

Finally there is also a function decorator:

    >>> @mdp.with_extension("parallel")
    ... def f():
    ...     pass
    
Again this ensures that the extension is deactivated after the function 
call, even in the case of an exception. The deactivation happens only if 
the extension was activated by the decorator (not if it was already 
active before).

Writing Extension Nodes
-----------------------

Suppose you have written your own nodes and would like to make them compatible
with a particular extension (e.g. add the required methods).
The first way to do this is by using multiple inheritance to derive from
the base class of this extension and your custom node class. For example
the parallel extension of the SFA node is defined in a class

    >>> class ParallelSFANode(mdp.parallel.ParallelExtensionNode, # doctest: +SKIP
    ...                       mdp.nodes.SFANode):
    ...     def _fork(self):
    ...         # implement the forking for SFANode
    ...         return ...
    ...     def _join(self):
    ...         # implement the joining for SFANode
    ...         return ...

Here ``ParallelExtensionNode`` is the base class of the extension. Then 
you define the required methods or attributes just like in a normal 
class. If you want you could even use the new ``ParallelSFANode`` class 
like a normal class, ignoring the extension mechanism. Note that your 
extension node is automatically registered in the extension mechanism 
(through a little metaclass magic). 

For methods you can alternatively use the ``extension_method`` function
decorator. You define the extension method like a normal function, but add
the function decorator on top. For example to define the ``_fork`` method
for the ``SFANode`` we could have also used

    >>> @mdp.extension_method("parallel", mdp.nodes.SFANode) # doctest: +SKIP
    ... def _fork(self):
    ...     return ...

The first decorator argument is the name of the extension, the second is the
class you want to extend. You can also specify the method name as a third
argument, then the name of the function is ignored (this allows you to get
rid of warnings about multiple functions with the same name).

Creating Extensions
-------------------

To create a new node extension you have to create a new extension base
class (unless you only use the extension decorators to define the extension
methods). For example, the HTML representation extension in ``mdp.hinet``
is created with

    >>> class  HTMLExtensionNode(mdp.ExtensionNode, mdp.Node): # doctest: +SKIP
    ...     """Extension node for HTML representations of individual nodes."""
    ...     extension_name = "html2"
    ...     def html_representation(self):
    ...         pass
    ...     def _html_representation(self):
    ...         pass

Note that you must derive from ``ExtensionNode``. If you also derive 
from ``mdp.Node`` then the methods (and attributes) in this class are 
the default implementation for the ``mdp.Node`` class. So they will be 
used by all nodes without a more specific implementation. If you do not 
derive from ``mdp.Node`` then there is no such default implementation. 
You can also derive from a more specific node class if your extension 
only applies to these specific nodes. 

When you define a new extension then you must define the ``extension_name``
attribute. This magic attribute is used to register the new extension and you
can activate or deactivate the extension by using this name.

Note that extensions can override attributes and methods that are 
defined in a node class. The original attributes can still be accessed 
by prefixing the name with ``_non_extension_`` (the prefix string is 
also available as ``mdp.ORIGINAL_ATTR_PREFIX``). On the other hand one 
extension is not allowed to override attributes that were defined by 
another currently active extension.

The extension mechanism uses some magic to make the behavior more 
intuitive with respect to inheritance. Basically methods or attributes 
defined by extensions shadow those which are not defined in the 
extension. Here is an example

    >>> class TestExtensionNode(mdp.ExtensionNode):
    ...     extension_name = "test"
    ...     def _execute(self):
    ...         return 0
    >>> class TestNode(mdp.Node):
    ...     def _execute(self):
    ...         return 1
    >>> class ExtendedTestNode(TestExtensionNode, TestNode):
    ...     pass

After this extension is activated any calls of ``_execute`` in instances 
of ``TestNode`` will return 0 instead of 1. The ``_execute`` from the 
extension base-class shadows the method from ``TestNode``. This makes it 
easier to share behavior for different classes. Without this magic one 
would have to explicitly override ``_execute`` in ``ExtendedTestNode`` 
(or derive the extension base-class from ``Node``, but that would give 
this behavior to all node classes). Note that there is a ``verbose`` 
argument in ``activate_extension`` which can help with debugging.

Extension Setup and Teardown Functions
--------------------------------------

If needed you can define a setup and/or teardown function for your extension.
The setup function is called when the extension is activated (before the
node classes are modified) and can be used for global modifications. The
teardown function is called when the extension is deactivated (after all
the node class modifications have been removed). In the following simple
example we set a global variable when the extension is actived

    >>> is_extension_active = False
    >>> @mdp.extension_setup("test")
    ... def _test_extension_setup():
    ...     global is_extension_active
    ...     is_extension_active = True
    >>> @mdp.extension_teardown("test")
    ... def _test_extension_teardown():
    ...     global is_extension_active
    ...     is_extension_active = False
