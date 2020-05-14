.. _parallel:

===============
Parallelization
===============
.. codesnippet::

The ``parallel`` package adds the ability to parallelize the training 
and execution of MPD flows. This package is split into two decoupled parts.

The first part consists of a parallel extension for the familiar MDP 
structures of nodes and flows. In principle all MDP nodes aldready 
support parallel execution, since copies of a node can be made and used 
in parallel. Parallelization of the training on the other hand depends 
on the specific node or algorithm. For nodes which can be trained in a 
parallelized way there is the extension class ``ParallelExtensionNode``.
It adds the ``fork`` and ``join`` methods. When providing a parallel 
extension for custom node classes you should implement ``_fork`` and 
``_join``. Secondly there is the ``ParallelFlow`` class, which 
internally splits the training or execution into tasks which are then 
processed in parallel. 

The second part consists of the schedulers. A scheduler takes tasks
and processes them in a more or less parallel way (e.g. in multiple
Python processes). A scheduler deals with the more technical aspects
of the parallelization, but does not need to know anything about
nodes and flows.

Basic Examples
--------------
In the following example we parallelize a simple ``Flow`` consisting of
PCA and quadratic SFA, so that it makes use of multiple cores on a modern CPU:

    >>> node1 = mdp.nodes.PCANode(input_dim=100, output_dim=10)
    >>> node2 = mdp.nodes.SFA2Node(input_dim=10, output_dim=10)
    >>> parallel_flow = mdp.parallel.ParallelFlow([node1, node2])
    >>> parallel_flow2 = parallel_flow.copy()
    >>> parallel_flow3 = parallel_flow.copy()
    >>> n_data_chunks = 10
    >>> data_iterables = [[np.random.random((50, 100))
    ...                    for _ in range(n_data_chunks)]] * 2
    >>> scheduler = mdp.parallel.ProcessScheduler()
    >>> parallel_flow.train(data_iterables, scheduler=scheduler)
    >>> scheduler.shutdown()

Only two additional lines were needed to parallelize the training of the 
flow. All one has to do is use a ``ParallelFlow`` instead of the normal 
``Flow`` and provide a scheduler. The ``ProcessScheduler`` will 
automatically create as many Python processes as there are CPU cores. 
The parallel flow gives the training task for each data chunk over to 
the scheduler, which in turn then distributes them across the available 
worker processes. The results are then returned to the flow, which puts 
them together in the right way. Note that the ``shutdown`` method should 
be always called at the end to make sure that the recources used by the 
scheduler are cleaned up properly. One should therefore put the 
``shutdown`` call into a safe try/finally statement

    >>> scheduler = mdp.parallel.ProcessScheduler()
    >>> try:
    ...     parallel_flow2.train(data_iterables, scheduler=scheduler)
    ... finally:
    ...     scheduler.shutdown()
    
The ``Scheduler`` class also supports the context manager interface of Python.
One can therefore use a ``with`` statement

    >>> with mdp.parallel.ProcessScheduler() as scheduler:
    ...     parallel_flow3.train(data_iterables, scheduler=scheduler)
    
The ``with`` statement ensures that ``scheduler.shutdown`` is automatically
called (even if there is an exception).
 

Scheduler
---------

The scheduler classes in MDP are derived from the ``Scheduler`` base 
class (which itself does not implement any parallelization). The 
standard choice at the moment is the ``ProcessScheduler``, which 
distributes the incoming tasks over multiple Python processes 
(circumventing the global interpreter lock or GIL). The performance gain 
is highly dependent on the specific situation, but can potentially scale 
well with the number of CPU cores (in one real world case we saw a 
speed-up factor of 4.2 on an Intel Core i7 processor with 4 physical / 8 
logical cores). 

MDP has experimental support for the `Parallel Python library 
<http://www.parallelpython.com>`_ in the ``mdp.parallel.pp_support`` 
package. In principle this makes it possible to parallelize across 
multiple machines. Recently we also added the thread based scheduler 
``ThreadScheduler``. While it is limited by the GIL it can still 
achieve a real-world speedup (since NumPy releases the GIL when 
possible) and it causes less overhead compared to the 
``ProcessScheduler``.

(The following information is only releveant for people who want to implement
custom scheduler classes.)

The first important method of the scheduler class is ``add_task``. This 
method takes two arguments: ``data`` and ``task_callable``, which can be 
a function or an object with a ``__call__`` method. The return value of 
the ``task_callable`` is the result of the task. If ``task_callable`` is 
``None`` then the last provided ``task_callable`` will be used. This 
splitting into callable and data makes it possible to implement caching 
of the ``task_callable`` in the scheduler and its workers (caching is 
turned on by default in the ``ProcessScheduler``). To further influence 
caching one can derive from the ``TaskCallable`` class, which has a 
``fork`` method to generate new callables in order to preserve the 
original cached callable. For MDP training and execution there are 
corresponding classes derived from ``TaskCallable`` which are 
automatically used, so normally there is no need to worry about this. 

After submitting all the tasks with ``add_task`` you can then call
the ``get_results`` method. This method returns all the task results,
normally in a list. If there are open tasks in the scheduler then
``get_results`` will wait until all the tasks are finished (it blocks). You can
also check the status of the scheduler by looking at the
``n_open_tasks`` property, which gives you the number of open tasks.
After using the scheduler you should always call the ``shutdown`` method,
otherwise you might get error messages from not properly closed processes.

Internally an instance of the base class ``mdp.parallel.ResultContainer`` is
used for the storage of the results in the scheduler. By providing your own
result container to the scheduler you modify the storage. For example the
default result container is an instance of ``OrderedResultContainer``. The
``ParallelFlow`` class by default makes sure that the right container is
used for the task (this can be overriden manually via the
``overwrite_result_container`` parameter of the ``train`` and ``execute``
methods).

Parallel Nodes
--------------

If you want to parallelize your own nodes you have to provide parallel
extensions for them. The ``ParallelExtensionNode`` base class has
the new template methods ``fork`` and ``join``. 
``fork`` should return a new node instance. This new instance can then be
trained somewhere else (e.g. in a different process) with the usual ``train``
method. Afterwards ``join`` is called on the original node, with the
forked node as the argument. This should be
equivalent to calling ``train`` directly on the original node.

During Execution nodes are not forked by default, instead they are just 
copied (for example they are pickled and send to the Python worker 
processes). It is possible for nodes during execution to 
explicitly request that they are forked and joined (like during 
training). This is done by overriding the ``use_execute_fork`` method, 
which by default returns ``False``. For example nodes that record data 
during execution can use this feature to become compatible with 
parallelization. 

When writing custom parallel node extension you should only overwrite 
the ``_fork`` and ``_join`` methods, which are automatically called by 
``fork`` and ``join``. The ``fork`` and ``join`` take care of the 
standard node attributes like the dimensions. You should also look at 
the source code of a parallel node like ``ParallelPCANode`` to get a 
better idea of how to parallelize nodes. By overwriting 
``use_execute_fork`` to return ``True`` you can force forking and 
joining during execution. Note that the same ``_fork`` and ``_join`` 
implementation is called as during training, so if necessary one should 
add an ``node.is_training()`` check there to determine the correct 
action. 

Currently we provide the following parallel nodes:
``ParallelPCANode``, ``ParallelWhiteningNode``, ``ParallelSFANode``,
``ParallelSFA2Node``, ``ParallelFDANode``, ``ParallelHistogramNode``,
``ParallelAdaptiveCutoffNode``, ``ParallelFlowNode``, ``ParallelLayer``,
``ParallelCloneLayer`` (the last three are derived from the ``hinet``
package).
