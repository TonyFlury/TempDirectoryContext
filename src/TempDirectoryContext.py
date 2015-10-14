#!/usr/bin/env python
#
# TempDirectoryContext : Implementation for tempfileContext
# 
#     A context handler wrap around the tempfile module - to enable clean up and close down
#

__version__ = "0.1"
__author__ = 'Tony Flury : anthony.flury@btinternet.com'
__created__ = '25 Aug 2015'

"""
# TimeWarp : Implementation of tempfileContext

Summary : 
    A context handler wrap around the tempfile module - to enable clean up and close down
Use Case :
    As an application I want to be able to create and tear down temporary files so that
    I can keep the environment clean

Testable Statements :
    Can I create a temp file area
    Can I clean up the temp file area on close down or exception
    Can the context manager clean up historic directories left by previous invocations
    Can the context manager delay clean-up to allow for debugging
    Can multiple context manager be used by the same application without clashing.


Example :
    from TempDirectoryContext import TempDirectoryContext

    with TempDirectoryContext() as tmp_path:
        # A directory is created as /tmp/tmp******TempDirCont - where ****** is a random 6 character string
        # The directory is created with full read/write access for the current user
        # Your code can now work with temp files under tmp_path

    # More code outside the Context block
    # Under default behaviour the temporary directory is queued for deletion - in theory files can still be used

options :
    Before invocation :
    TempDirectoryContext.keep_max

"""

import tempfile
import shutil
import os
import os.path

class TempDirectoryContext(object):

    _to_be_deleted = {}

    def __init__(self, suffix="TempDirCont", prefix="tmp", dir=None, delete_historic=True, keep_max=3):
        self._suffix = suffix
        self._prefix = prefix
        self._keep_max = keep_max
        self._root = tempfile.gettempdir() if not dir else dir
        self._delete_historic = delete_historic

        if not TempDirectoryContext._to_be_deleted.get((self._root, suffix, prefix), []):
            TempDirectoryContext._to_be_deleted[(self._root, suffix, prefix)] = []

        self._delete_queue = TempDirectoryContext._to_be_deleted.get((self._root, suffix, prefix), [])

        # Check if we have already initiated the to_be_deleted queue for entries for this (or similar instances)
        if delete_historic and (not self._delete_queue):
            # Sort the queue based on creation date - oldest first
            self._delete_queue += sorted([os.path.join(self._root, path) for path in os.listdir(self._root)
                                          if (os.path.split(path)[1].startswith(self._prefix)) and
                                          (os.path.split(path)[1].endswith(self._suffix))],
                                         key=lambda x: os.stat(x).st_ctime,
                                         reverse=False)

    def __enter__(self):
        self._dtemp = tempfile.mkdtemp(suffix=self._suffix, prefix=self._prefix)
        return self._dtemp

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Add the file to the to_be_deleted list - don't delete immediately
        self._delete_queue.append(self._dtemp)
        self._dtemp = None

        while len(self._delete_queue) >  self._keep_max:
            name = self._delete_queue[0]
            try:
                shutil.rmtree(os.path.join(tempfile.gettempdir(), name))
                del self._delete_queue[0]
            except Exception as e:
                del self._delete_queue[0]
                return False
        return False
