#!/usr/bin/env python
"""
# TempDirectoryContext : Test Suite for test_0000_TemporaryDirectoryContext.py

Summary :
    Testing a context handler wrap around the tempfile module - to enable clean up and close down
Use Case :
    As an application I want to be able to create and tear down temporary files so that I can keep the environment clean

Testable Statements :
    Can I create a temp file area
    Can I clean up the temp file area on close down or exception
"""

import unittest
import os.path
import tempfile
import TempDirectoryContext as TempDirCont

__version__ = "0.1"
__author__ = 'Tony Flury : anthony.flury@btinternet.com'
__created__ = '25 Aug 2015'


class Test00Parameters(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_00_001_TestDefaults(self):
        """Test Directory is created with defaults"""
        with TempDirCont.TempDirectoryContext() as tmp:
            parts = os.path.split(tmp)
            self.assertEqual(parts[0], tempfile.gettempdir())
            self.assertEqual(parts[1].startswith("tmp"), True)
            self.assertEqual(parts[1].endswith("TempDirCont"), True)

    def test_00_010_keep_max0(self):
        """Test keep_max=0 - i.e. directory deleted on exit"""
        with TempDirCont.TempDirectoryContext(keep_max=0) as tmp:
            self.assertEqual(os.path.exists(tmp), True)

        # Since keep_max is zero the directory should be deleted immediately
        self.assertEqual(os.path.exists(tmp), False)

    def test_00_020_prefix(self):
        """Test prefix argument - change start of directory name"""
        with TempDirCont.TempDirectoryContext(prefix="testing", keep_max=0) as tmp:
            self.assertEqual(os.path.exists(tmp), True)
            self.assertEqual(os.path.split(tmp)[1].startswith("testing"), True)
            self.assertEqual(os.path.split(tmp)[1].endswith("TempDirCont"), True)

    def test_00_030_suffix(self):
        """Test suffix argument - change end of directory name"""
        with TempDirCont.TempDirectoryContext(suffix="testing", keep_max=0) as tmp:
            self.assertEqual(os.path.exists(tmp), True)
            self.assertEqual(os.path.split(tmp)[1].startswith("tmp"), True)
            self.assertEqual(os.path.split(tmp)[1].endswith("testing"), True)

    @unittest.skip("Needs reworking to test robsutly in python3")
    def test_00_040_dir(self):
        """Test dir argument - change directory into temp directory is created"""
        tmp_root = tempfile.gettempdir()
        new = os.path.join(tmp_root, "testing")
        os.mkdir(new)
        with TempDirCont.TempDirectoryContext(keep_max=0, root=new) as tmp:
            self.assertEqual(os.path.exists(tmp), True)
            base, tail = os.path.split(tmp)
            self.assertEqual(base, new)
        os.rmdir(new)


class Test01Functionality(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        r = tempfile._get_default_tempdir()
        l = [os.path.join(r, i) for i in os.listdir(r) if i.startswith("tmp") and i.endswith("TempDirCont")]
        self.assertLessEqual(len(l), 3)

    def test_01_001_SimpleCreationOneDirectory(self):
        """Test Single Directory testing - confirm it is kept"""
        # Test that the context manager
        with TempDirCont.TempDirectoryContext() as tmp:
            self.assertEqual(os.path.exists(tmp), True)
        self.assertEqual(os.path.exists(tmp), True)

    def test_01_002_SimpleCreationTwoDirectories(self):
        """Create two directories - confirm both are kept"""
        td = []
        with TempDirCont.TempDirectoryContext() as tmp:
            td.append(tmp)
            self.assertEqual(os.path.exists(tmp), True)

        with TempDirCont.TempDirectoryContext() as tmp:
            td.append(tmp)
            self.assertEqual(os.path.exists(tmp), True)

        td = list(map(os.path.exists, td))
        self.assertEqual(td, [True, True])

    def test_01_003_SimpleCreationThreeDirectories(self):
        """Create three directories - confirm all are kept"""
        td = []

        for i in range(3):
            with TempDirCont.TempDirectoryContext() as tmp:
                td.append(tmp)
                self.assertEqual(os.path.exists(tmp), True)

        td = list(map(os.path.exists, td))

        self.assertEqual(td, [True, True, True])

    def test_01_004_SimpleCreationFourDirectories(self):
        """Create four directories - confirm all but the first is kept"""
        td = []

        for i in range(4):
            with TempDirCont.TempDirectoryContext() as tmp:
                td.append(tmp)
                self.assertEqual(os.path.exists(tmp), True)

        td = list(map(os.path.exists, td))
        self.assertEqual(td, [False, True, True, True])

    def test_01_010_TreeDeletion(self):
        """Tree Deletion - Confirm that the Tree of files are deleted"""
        # Create temp directory with keep_max as 0 - immediate deletion
        with TempDirCont.TempDirectoryContext(keep_max=0) as tmp:
            self.assertEqual(os.path.exists(tmp), True)

            # Create a file with content
            path = os.path.join(tmp, "testing.txt")
            with open(path, "w") as fd:
                fd.write("This is a testing file")

            self.assertEqual(os.path.exists(path), True)

        # Since keep_max is zero the directory should be deleted immediately
        self.assertEqual(os.path.exists(tmp), False)


class Test02Concurrent(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_02_001_two_concurrent(self):
        """Parallel context managers - with different prefixes"""
        with TempDirCont.TempDirectoryContext(prefix="tmp0") as tmp0, \
                TempDirCont.TempDirectoryContext(prefix="tmp1") as tmp1:
            self.assertEqual(os.path.split(tmp0)[1].startswith("tmp0"), True)
            self.assertEqual(os.path.split(tmp1)[1].startswith("tmp1"), True)

    def test_02_010_two_concurrent_inner(self):
        """Nested context managers"""

        # Create an outer context with immediate deletion
        with TempDirCont.TempDirectoryContext(keep_max=0, suffix="Outer") as outer:
            self.assertEqual(os.path.exists(outer), True)

            # Create an inner context with immediate deletion
            with TempDirCont.TempDirectoryContext(keep_max=0, suffix="Inner") as inner:
                self.assertEqual(os.path.exists(inner), True)

            # Inner should be deleted, outer must still exist
            self.assertEqual(os.path.exists(inner), False)
            self.assertEqual(os.path.exists(outer), True)

        # Outer now should be deleted
        self.assertEqual(os.path.exists(outer), False)


# noinspection PyUnusedLocal
def load_tests(loader, tests=None, pattern=None):
    """Test loading - load test cases from each Class"""
    classes = [Test00Parameters, Test01Functionality, Test02Concurrent]
    suite = unittest.TestSuite()
    for test_class in classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite


if __name__ == '__main__':
    ldr = unittest.TestLoader()

    test_suite = load_tests(ldr)

    unittest.TextTestRunner(verbosity=2).run(test_suite)
