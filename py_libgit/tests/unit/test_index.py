import unittest
from unittest.mock import MagicMock

import os, shutil
from py_libgit.core.index import Index
from py_libgit.core.repo import Repo

import py_libgit.settings_tests

class TestIndex(unittest.TestCase):
    def setUp(self):
        repo = MagicMock()
        self.repo_name = 'repotest'
        self.repo_dir = os.path.join('/tmp', self.repo_name)
        self.git_repo_root = os.path.join(self.repo_dir, '.git')
        os.makedirs(self.git_repo_root)
        repo.get_repo_root = MagicMock(return_value=self.git_repo_root)
        self.index = Index(repo)
        self.index_file = os.path.join(self.repo_dir, '.git', 'index')

    def tearDown(self):
        shutil.rmtree(self.repo_dir, ignore_errors=True)

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

    def test_normalize_pathname_removes_single_dot_path(self):
        pathname = os.path.join(self.repo_dir, 'abc/./test')
        normalized_pathname = self.index.normalize_pathname(pathname)
        expected_pathname = os.path.join(self.repo_name, 'abc/test')
        self.assertEqual(normalized_pathname, expected_pathname, 'The single dot in the normalized path is not properly handled')

    def test_normalize_pathname_removes_double_dots_with_same_path(self):
        pathname = os.path.join(self.repo_dir, 'abc/test/../test')
        normalized_pathname = self.index.normalize_pathname(pathname)
        expected_pathname = os.path.join(self.repo_name, 'abc/test')
        self.assertEqual(normalized_pathname, expected_pathname, 'The double dot in the normalized path is not properly handled')

    def test_normalize_pathname_removes_double_dots_with_different_path(self):
        pathname = os.path.join(self.repo_dir, 'abc/test1/../test2')
        normalized_pathname = self.index.normalize_pathname(pathname)
        expected_pathname = os.path.join(self.repo_name, 'abc/test2')
        self.assertEqual(normalized_pathname, expected_pathname, 'The double dot in the normalized path is not properly handled')

    def test_normalize_pathname_removes_multiple_double_dots(self):
        pathname = os.path.join(self.repo_dir, 'abc/test1/test2/../../test3')
        normalized_pathname = self.index.normalize_pathname(pathname)
        expected_pathname = os.path.join(self.repo_name, 'abc/test3')
        self.assertEqual(normalized_pathname, expected_pathname, 'The double dot in the normalized path is not properly handled')

    def test_normalize_pathname_removes_multiple_double_dots_separately(self):
        pathname = os.path.join(self.repo_dir, 'abc/test1/../test2/../test3')
        normalized_pathname = self.index.normalize_pathname(pathname)
        expected_pathname = os.path.join(self.repo_name, 'abc/test3')
        self.assertEqual(normalized_pathname, expected_pathname, 'The double dot in the normalized path is not properly handled')
