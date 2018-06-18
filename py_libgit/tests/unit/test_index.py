import unittest
from unittest.mock import MagicMock

import os
from py_libgit.core.index import Index
from py_libgit.core.repo import Repo

import py_libgit.settings_tests

class TestIndex(unittest.TestCase):
    def setUp(self):
        self.index_file = '/tmp/index'
        repo = MagicMock()
        repo.get_repo_root = MagicMock(return_value='/tmp')
        self.index = Index(repo)

    def tearDown(self):
        os.remove(self.index_file)

    def test_index_updated_correctly_when_no_entry(self):
        pathname = 'helloworld'
        self.index.update_index(pathname)
        with open(self.index_file, 'r') as f:
            index_content = f.read()

        expected_index_content = '{}\n'.format(pathname)
        self.assertTrue(os.path.exists(self.index_file))
        self.assertEqual(index_content, expected_index_content, 'The index content did not record the proper pathname')

    def test_duplicate_index_update_should_not_occur(self):
        pathname = 'helloworld'
        self.index.update_index(pathname)
        self.index.update_index(pathname)
        with open(self.index_file, 'r') as f:
            index_content = f.read()

        expected_index_content = '{}\n'.format(pathname)
        self.assertTrue(os.path.exists(self.index_file))
        self.assertEqual(index_content, expected_index_content, 'The index content should only contain one entry of the pathname')

    def test_adding_different_index_entry(self):
        pathname1 = 'helloworld'
        pathname2 = 'helloworld2'
        self.index.update_index(pathname1)
        self.index.update_index(pathname2)
        with open(self.index_file, 'r') as f:
            index_content = f.read()

        expected_index_content = '{}\n{}\n'.format(pathname1, pathname2)
        self.assertEqual(index_content, expected_index_content, 'The index content did not record both pathnames')
