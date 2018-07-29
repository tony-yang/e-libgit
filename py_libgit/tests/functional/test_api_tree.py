import unittest

import os, shutil
from py_libgit.api.add import Add
from py_libgit.api.init import Init
from py_libgit.api.tree import Tree
from py_libgit.core.tree_entry import TreeEntry, EntryType

import py_libgit.settings_tests

class TestTree(unittest.TestCase):
    def setUp(self):
        os.chdir('/tmp')
        self.repo_name = 'hellogit-testrepo'

        self.init = Init()
        self.init.create_git_repo(self.repo_name)

        self.add = Add()
        filename = 'hello'
        content = 'hello world\n'
        pwd = os.getcwd()
        os.chdir(os.path.join(pwd, self.repo_name))
        with open(filename, 'w') as f:
            f.write(content)
        content_hash = self.add.create_blob(filename)

        self.tree = Tree()

    def tearDown(self):
        os.chdir('/tmp')
        shutil.rmtree(self.repo_name, ignore_errors=True)

    def test_create_tree_successfully(self):
        tree_entry = self.tree.create_tree()
        expected_tree_entry = TreeEntry(self.repo_name, entry_type=EntryType.TREE, sha1='6a98fd9cb9c98a860866e8a309f51c0686baa3e8')
        self.assertEqual(str(tree_entry), str(expected_tree_entry), 'Incorrect tree hash')
