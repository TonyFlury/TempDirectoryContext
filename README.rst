====================
TempDirectoryContext
====================

The TempDirectoryContext provides a simple to use library that provides a context manager around the creation and deletion of temporary directories.

The module provides a context manager around the ``tempfile.mkdtemp`` library calls, and providing automated clean up of the directories. By default the context manager keeps up to 3 historic temporary directories - especially useful for testing and debugging. It is possible to configure the following properties :
 - The Directory name Prefix and Suffix.
 - The number of historic directories to be kept
 - Whether to delete historic directories at all - *here be dragons - be careful*

As an example

.. code-block:: python

    import TempDirectoryContext as TempDirCont

    with TempDirCont.TempDirectoryContext() as tmp:
        #
        # A temporary directory is created under the standard tmp directory - probably /tmp
        # The directory will be named : /tmp/tmp<xxxxxx>TempDirCont - where <xxxxxx> is a random 6 character string
        # (Assuming that the standard tmp directory is /tmp
        #

The context manager accept the following arguments:
    - prefix : The first characters of the directory name (defaults to ``tmp``)
    - suffix : The end characters of the directory name (defaults to ``TempDirCont``)
    - dir : The directory into which the temporary directory is created (defaults to tempfile.gettempdir() )
    - delete_historic : A Boolean to determine if previous directories are deleted (defaults to ``True``)
    - keep_max : The maximum number of historic directories to keep (defaults to 3)

As indicated the context manager keeps track of historically created temporary directory and attempts to clean them up. The clean up action takes place when the context manager exits.
Historic directories are deleted in date order, and are counted based on the suffix and prefix values.
The delete historic and keep_max arguments are applied on the basis of the prefix and suffix as well - allowing you to apply different deletion strategies to different sets of temporary directories.

*Note* : The delete_historic and keep_max arguments are re-applied when the context manager is exited. This could lead to directories being deleted, despite the directory being seemingly protected when it was created: An example :

.. code-block:: python

    import TempDirectoryContext as TempDirCont


    def funca():
        with TempDirCont.TempDirectoryContext(delete_historic=False) as tmp:
            # Some code
        # Nothing will be deleted when the above context manager exits

    def funcb():
        with TempDirCont.TempDirectoryContext(keep_max=1, delete_historic=True) as tmp:
            # Some code
        # All historic temp directories will be deleted when the above context manager exits
        # with the exception of the last directory created (i.e. the one created by the context manager above).


    funca()
    funcb()
    # At this point the directory created in funca() will be deleted
    # despite the argument ``delete_historic`` being False when the context manager is invoked.


To avoid this, you should ensure that the ``delete_historic`` and ``keep_max`` settings are kept consistent when the same prefix and suffix are used, as the deletion process is applied on the basis of the prefix and suffix, rather than across all temporary directories.

Use Case
========
The main use case for this library is for testing, where you might want to create a sandbox directory (which can be safely deleted), but which is retained for debugging purposes. By using different prefixes and suffixes you can create multiple sets of sandboxed directories with different prefixes and suffixes - so it is clear what files pertain to which tests.