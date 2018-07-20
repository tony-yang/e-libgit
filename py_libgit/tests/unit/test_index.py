import unittest
from unittest.mock import MagicMock

import os, shutil
from py_libgit.core.index import Index
from py_libgit.core.index_entry import IndexEntry
from py_libgit.core.repo import Repo

import py_libgit.settings_tests

class TestIndex(unittest.TestCase):
    def setUp(self):
        self.repo_name = 'repotest'
        self.repo_dir = os.path.join('/tmp', self.repo_name)
        self.git_repo_root = os.path.join(self.repo_dir, '.git')
        os.makedirs(self.git_repo_root)

        repo = MagicMock()
        repo.get_repo_root = MagicMock(return_value=self.git_repo_root)

        self.index = Index(repo)
        self.index_file = os.path.join(self.git_repo_root, 'index')

    def tearDown(self):
        shutil.rmtree(self.repo_dir, ignore_errors=True)

    def test_index_updated_correctly_when_no_entry(self):
        pathname = 'helloworld'
        current_sha1 = '0' * 40
        new_sha1 = '0123456789' * 4
        unix_mode = '10000644'
        staging_content = [IndexEntry(pathname, new_sha1=new_sha1)]
        self.index.update_index(staging_content)
        self.assertTrue(os.path.exists(self.index_file))

        with open(self.index_file, 'r') as f:
            index_content = f.read()
        expected_index_content = '{} {} {} {}\n'.format(pathname, current_sha1, new_sha1, unix_mode)
        self.assertEqual(index_content, expected_index_content, 'The index content did not record the proper pathname')

    def test_duplicate_index_update_should_change_nothing(self):
        pathname = 'helloworld'
        current_sha1 = '0' * 40
        new_sha1 = '0123456789' * 4
        unix_mode = '10000644'
        staging_content = [IndexEntry(pathname, new_sha1=new_sha1)]
        self.index.update_index(staging_content)
        self.index.update_index(staging_content)
        with open(self.index_file, 'r') as f:
            index_content = f.read()

        expected_index_content = '{} {} {} {}\n'.format(pathname, current_sha1, new_sha1, unix_mode)
        self.assertTrue(os.path.exists(self.index_file))
        self.assertEqual(index_content, expected_index_content, 'The index content should only contain one entry of the pathname')

    def test_adding_different_index_entry(self):
        pathname = 'helloworld'
        current_sha1 = '0' * 40
        new_sha1 = '0123456789' * 4
        unix_mode = '10000644'

        pathname_2 = 'helloworld2'
        current_sha1_2 = '0' * 40
        new_sha1_2 = '9876543210' * 4
        unix_mode_2 = '10000644'

        staging_content = [IndexEntry(pathname, new_sha1=new_sha1), IndexEntry(pathname_2, new_sha1=new_sha1_2)]
        self.index.update_index(staging_content)
        with open(self.index_file, 'r') as f:
            index_content = f.read()

        expected_index_content = '{} {} {} {}\n{} {} {} {}\n'.format(pathname, current_sha1, new_sha1, unix_mode, pathname_2, current_sha1_2, new_sha1_2, unix_mode_2)
        self.assertEqual(index_content, expected_index_content, 'The index content did not record both pathnames')

    def test_updaing_index_entry_should_work(self):
        pathname = 'helloworld'
        current_sha1 = '0' * 40
        new_sha1 = '0123456789' * 4
        unix_mode = '10000644'

        new_sha1_2 = '9876543210' * 4

        staging_content = [IndexEntry(pathname, new_sha1=new_sha1)]
        self.index.update_index(staging_content)
        staging_content = [IndexEntry(pathname, new_sha1=new_sha1_2)]
        self.index.update_index(staging_content)
        with open(self.index_file, 'r') as f:
            index_content = f.read()

        expected_index_content = '{} {} {} {}\n'.format(pathname, current_sha1, new_sha1_2, unix_mode)
        self.assertEqual(index_content, expected_index_content, 'The index content did not update the path attributes properly')

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
