.. _development:

***********
Development
***********

.. _maintainers:

-----------
Maintainers
-----------

MDP has been originally written by `Pietro Berkes`_ and `Tiziano Zito`_
at the `Institute for Theoretical Biology <http://itb.biologie.hu-berlin.de/>`_
of the `Humboldt University <http://www.hu-berlin.de/>`_, Berlin in 2003.

Since 2017, MDP is primarily maintained by the reasearch group
`Theory of Neural Systems <https://www.ini.rub.de/research/groups/theory_of_neural_systems/>`_
at the `Institute for Neural Computation <https://www.ini.rub.de/>`_
of the `Ruhr University Bochum <https://www.ruhr-uni-bochum.de/en>`_.

Current maintainers are:

*   `Nils Müller <https://www.ini.rub.de/the_institute/people/nils-mller/>`_
*   `Stefan Richthofer <https://www.ini.rub.de/the_institute/people/stefan-richthofer/>`_
*   `Tiziano Zito <https://github.com/otizonaizit>`_


MDP is open to user contributions. Users have already contributed some
of the nodes, and more contributions are currently being reviewed for
inclusion in future releases of the package. The package development
can be followed online on the public git code `repositories`_ or
cloned with::

    git clone git://github.com/mdp-toolkit/mdp-toolkit.git
    git clone git://github.com/mdp-toolkit/mdp-docs.git

.. _repositories: http://github.com/mdp-toolkit


You can install the development version by changing to the newly
created ``mdp-toolkit`` directory and running::	

    pip install -e .

For comments, patches, feature requests, support requests, and bug reports
you can use the users’ `mailing list`_.

If you want to contribute some code or a new algorithm, please do not
hesitate to submit it!

.. _python-mdp: http://packages.debian.org/python-mdp
.. _py25-mdp-toolkit: http://trac.macports.org/browser/trunk/dports/python/py25-mdp-toolkit/Portfile
.. _py26-mdp-toolkit: http://trac.macports.org/browser/trunk/dports/python/py26-mdp-toolkit/Portfile


.. _`mailing list`: https://mail.python.org/mm3/mailman3/lists/mdp-toolkit.python.org/


------------
Contributors
------------
Strictly in alphabetical order:

- `Gabriel Beckers <http://www.gbeckers.nl/>`_
- `Pietro Berkes <http://people.brandeis.edu/~berkes/>`_
- Sven Dähne
- Philip DeBoer
- Kamel Ibn Aziz Derouiche
- `Alberto Escalante <https://www.ini.rub.de/the_institute/people/alberto-escalante/>`_
- `Farzad Farkhooi <https://www.bcp.fu-berlin.de/en/biologie/arbeitsgruppen/neurobiologie/ag_nawrot/people/alumni/farkhooi/index.html>`_
- Mathias Franzius
- `Valentin Haenel <https://github.com/esc>`_
- `Yaroslav Halchenko`_
- `Michael Hanke <https://github.com/mih>`_
- `Konrad Hinsen <http://dirac.cnrs-orleans.fr/~hinsen/>`_
- Christian Hinze
- `Sebastian Höfer <http://www.sebastianhoefer.de>`_
- Michael Hull
- `Zbigniew Jędrzejewski-Szmek <https://github.com/keszybz>`_
- `Samuel John <http://www.samueljohn.de/>`_
- `Varun Kompella <https://varunrajk.gitlab.io/>`_
- Susanne Lezius
- Maximilian Nickel
- `Fabian Pedregosa <http://fseoane.net/blog/>`_
- `José Quesada <https://github.com/quesada>`_
- `Stefan Richthofer <https://www.ini.rub.de/the_institute/people/stefan-richthofer/>`_
- `Ariel Rokem <http://argentum.ucbso.berkeley.edu/ariel.html>`_
- `Michael Schmuker <https://github.com/Huitzilo>`_
- `Benjamin Schrauwen <https://about.me/benjamin_schrauwen>`_
- `Fabian Schönfeld <https://www.ini.rub.de/the_institute/people/fabian-schonfeld/>`_
- `Rike-Benjamin Schuppner <https://github.com/Debilski>`_
- `Henning Sprekeler <https://www.cognition.tu-berlin.de/menue/members/henning_sprekeler/>`_
- `Jake VanderPlas <https://github.com/jakevdp>`_
- `David Verstraeten <https://we.vub.ac.be/en/david-verstraeten>`_
- `Niko Wilbert <https://github.com/nwilbert>`_
- Ben Willmore
- `Katharina Maria Zeiner <http://dgppf.de/dr-katharina-m-zeiner/>`_

.. _`Yaroslav Halchenko`: http://centerforopenneuroscience.org/whoweare#yaroslav_o_halchenko_
 
------------------------------
Information for new developers
------------------------------

We try here to summarize some policies
and best-practices specific to new developers. You should also follow
the `General style guidelines`_, which are applicable to
all developers.

- If you do not already own one, create an account on github.com and tell
  us your username there, so that we can add you to the list of developers
  and give you access to our git repositories

- Since our migration to git, the repository setup consists of
  two separate repositories:

  * ``mdp-toolkit``
  * ``mdp-docs``

- If you want to commit code, it may be easiest to fork the MDP repository
  on github and give us a note on the mailing list. We may then discuss
  how to integrate your modifications.
  For simple fixes that don’t need much discussion, you can also send
  a mail patch to the list using ``git format-patch`` or similar.

- Your code contribution should not have any additional
  dependencies, i.e. they should require only the numpy module to be
  installed. If your code requires some other module, e.g. scipy or
  C/C++ compilation, ask
  mdp-toolkit@python.org
  for assistance.

-------------------
Development process
-------------------

Development takes place on the ``master`` branch, but it doesn't mean
that everything should be immediately commited there.

Small commits and bugfixes and the like should go immediately on the
main branch, if the commiter thinks that nothing will be broken by the
patch::

    git checkout master
    # make a small fix :)
    sed -ir s/develepement/development/g development_process.rst
    git add development_process.rst
    git commit -m 'FIX: correct spelling of development'

More complicated commits should go on a feature branch::

    git checkout -b my_new_feature
    <do some changes>
    git add <some-file> <some-other-file>
    git commit -m 'NEW: add subfeature-1'
    <do some more changes>
    git commit -m 'NEW: implement this and that'

When a developer wants to show the branch to other people, she should
push it into the main repo::

    git push origin my_new_feature


Temporary branches
------------------

If you are about to test something and you’ve got the idea that your
code won’t last long in the repository, (maybe you want to show your
code to another developer or you want to just check, if you can commit
to the server,) you should create another branch for that, the same as
for any new feature.

The advantage is, that it keeps our master branch clean from all those
‘testing some really strange new stuff – please have a look’ commits,
which are likely to be reverted again. When you feel good about your
commit, you can cherry-pick or merge the good stuff to master.

Alternatively, ‘please have a look’ commits may also be pushed to a
separate repository (e.g. a github fork).


Merging feature branches back into the ``master`` branch
--------------------------------------------------------

Development is consensus based, so new features should be posted for
review and gain acceptance before being merged back into the main
branch. After the decision to merge has been made:

#. Check that all tests pass on the feature branch. Ideally, the branch
   should already include tests for all code it introduces or
   significantly changes.

   Some things to test in special circumstances:

   - If the code does anything version specific, it should be tested on
     all supported python versions::

         python2.5 /usr/bin/py.test
         python2.6 /usr/bin/py.test
         python2.7 /usr/bin/py.test
         python3.1 setup.py build
         (cd build/py3k && py.test-3.1)
         (cd build/py3k && python3.2 /usr/bin/py.test-3.1)

     TODO: add windows and mac equivalents

   - If the code does anything platform specific if should also be
     tested on Windows.

   - Code should be tested with both numpy and scipy as backends.
     Since scipy will be selected by default if installed, the extra
     step that can be performed is testing while selecting numpy
     explicitely::

         MDPNUMX=numpy py.test

   Before merging also make sure that the master branch passes tests :)

#. The merge should be performed in a way that preserves the history
   of the branch::

       git checkout master
       git merge --no-ff my_new_feature

   The merge commit should retain the name of the branch in the
   message. E.g. a commit with a message *Merge branch my_new_feature*
   is OK, commit with a message
   *Merge commit 1234567890123456789012345678901234567890* is not so good.

#. After merging, tests should also pass.

   If tests fail and the failures are caused by a problem with the
   merge, the merge commit should be amended::

       <fix code>
       py.test ...
       git commit --amend -a

   If the changes introduced in the branch simply uncovered problems in
   other parts of the codebase, the fixes can be committed as separate
   changesets.

#. Only when tests after the merge execute satisfactorily, changes
   should be pushed to sourceforge. The old branch can be deleted.::

       git push origin :my_new_feature

Git commit messages
-------------------

Commit messages are supposed to start with a prefix that specifies the
type of change:

* ``DOC:`` documentation
* ``FIX:`` fixes something
* ``ERF:`` enhancement, refactoring
* ``NEW:`` a new feature
* ``OTH:`` other (use with care)

The message should consist of a short summary (up to about 70
characters) and a longer explanation after an empty line. The summary
messages will are used to generate a changelog for distribution
tarballs.

History rewriting
-----------------

The developer that created a feature branch is free to rewrite the
history of the branch if she finds it reasonable::

    # do some history cleaning
    git rebase -i $(git merge-base origin/master my_new_feature)
    # upload a new version of the branch and override the old one
    git push --force origin my_new_feature

If multiple developers wants to cooperate on ``feature_branch``, they
should agree between themselves on a history rewriting policy.

------------------------
General Style Guidelines
------------------------

- Read carefully the :ref:`Writing your own 
  nodes: subclassing Node <write-your-own-nodes>`
  section of the :ref:`Tutorial <tutorial>`. 
- Remember to set the supported dtypes for your nodes.
  Example of a node supporting only single and double precision:
  * ``SFANode`` in mdp-toolkit/mdp/nodes/sfa_nodes.py
  Example of a node supporting almost every dtype:
  * ``HitParadeNode`` in mdp-toolkit/mdp/nodes/misc_nodes.py

- If setting ``input_dim``, ``output_dim`` or ``dtype`` has side
  effects, remember to implement that in the ``_set_input_dim``,
  ``_set_output_dim``, ``_set_dtype`` functions.  Several examples are
  available in ``mdp-toolkit/mdp/nodes/``

- Your code should strictly follow the `PEP 8 <http://www.python.org/dev/peps/pep-0008/>`_
  coding conventions. Note that some older code
  sections in MDP do not follow PEP 8 100%, but when the opportunity arises
  (e.g., when we make changes in the code) we are improving this. So new code
  should always follow PEP 8. Additional style guidelines can be learned from
  the famous `Code like a Pythonista <http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html>`_.

- Always import numpy in your code as::

    from mdp import numx

  ``numx`` is a placeholder we use to automatically import scipy
  instead of numpy when scipy is installed on the system.  Similarly,
  import ``numx_fft``, ``numx_linalg``, ``numx_rand``, for the
  corresponding submodules in NumPy or SciPy. This way your code will
  work independently of the numerical backend.

- Only raise ``mdp.NodeException``. If you need custom exceptions, derive
  them from ``mdp.NodeException``.

- Your nodes needs to pass the automatic tests for setting and
  consistency of ``input_dim``, ``output_dim`` and ``dtype`` *and* at
  least one functional test, which should test the algorithm possibly
  in a non-trivial way and compare its results with exact data you can
  derive analytically. If the latter is not possible, you should
  compare results and expected data within a certain precision. Look
  for example at ``testPCANode`` in
  ``mdp-toolkit/mdp/test/test_PCANode.py``.
  For the generic tests, the relevant code is in
  ``mdp-toolkit/mdp/test/test_nodes_generic.py``  in the functions
  ``test_dtype_consistency``, ``test_outputdim_consistency``,
  ``test_dimdtypeset``, ``test_inverse``.

- You nodes must have telling and explicit doc-strings. In
  particular, the class doc-string must cite references (if any) for
  the algorithm, and list the internal attributes of interest for
  the user. Any method not belonging to the base ``Node`` class must be
  clearly documented in its doc-string. Error messages must give an
  hint to the user what’s wrong and possible ways around the
  problem. 
- Any non trivial algorithmic step in the code must be
  commented, so that other developers understand what’s going on. If
  you have doubts, mark the code with ``#???`` or ``#XXX``. 
  If you think a better implementation is possible or additional
  work is needed, mark the code with ``#TODO``.
  Other useful tags are ``#FIXME`` if you know something is broken or
  inefficient, ``#NOTE`` or ``#WARNING`` to remember you or your
  fellow developer about issues, and finally ``#YYY`` as an answer to
  the question marked with ``#???``. 

  Have a look at the ``SFANode`` implementation for an example.

- When you commit your code *always* provide a meaningful log
  message: it will be mailed automatically to all other developers!

- This list is far from being complete, please let us know your
  comments and remarks :-)

