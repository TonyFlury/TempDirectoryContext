============================
TempDirectoryContext Details
============================

.. automethod:: TempDirectoryContext.TempDirectoryContext.__init__

Usage
=====

Default parameters:
-------------------

.. _ Example1:

.. code-block:: python
    :caption: Example 1: Default Parameters

    from TempDirectoryContext import TemporaryDirectorContext as TDC

    with TDC() as tmp_dir:

        <code block>

In the :ref:``Example1`` tmp_dir is a temporary directory - by default it will be:
    `/tmp/tmp<sig>TempDirCont/`

Where sig is a unique string provided by the tempfile standard library

By default the directory will not be deleted immediately the context manager exits; The context manager ensures that a total of 3 directories are kept (with the same prefix and suffix, and in the same root directory). This limit is imposed on context manager exits. This includes any previous directories created by this or any other process with the same suffix and prefix in the same root.


Ensuring immediate deletion:
----------------------------

.. _ Example2:

.. code-block:: python
    :caption: Example 2: Immediation deletion

    from TempDirectoryContext import TemporaryDirectorContext as TDC

    with TDC(keep_max=0) as tmp_dir:

        <code block>

With keep_max as 0, this will ensure that this directory (and any other historic directories, with the same Suffix, Prefix and in the same root directory) will be deleted.

Preventing deletion:
--------------------

.. _ Example2:

.. code-block:: python
    :caption: Example 3: Preventing Deletion

    from TempDirectoryContext import TemporaryDirectorContext as TDC

    with TDC(delete_historic=False) as tmp_dir:

        <code block>

With delete_historic as False, this prevents any deletion of any directories (with this suffix, prefix and in this root directory).