import unittest
from unittest.mock import MagicMock

import hashlib, os, shutil
from py_libgit.core.index_entry import IndexEntry
from py_libgit.core.objects import Objects
from py_libgit.core.tree_entry import TreeEntry, EntryType

import py_libgit.settings_tests

class TestCommitTree(unittest.TestCase):
    def setUp(self):
        self.git_repo_name = 'objects-repo'
        self.git_repo = os.path.join('/tmp', self.git_repo_name)
        self.git_root_dir = os.path.join(self.git_repo, '.git')
        self.objects_dir = os.path.join(self.git_root_dir, 'objects')
        repo = MagicMock()
        repo.get_repo_root = MagicMock(return_value=self.git_root_dir)
        os.makedirs(self.objects_dir)
        os.chdir(self.objects_dir)

        self.index = MagicMock()
        self.objects = Objects(repo, self.index)

    def tearDown(self):
        shutil.rmtree(self.git_repo, ignore_errors=True)

    def test_create_objects_on_non_exist_file_should_return_without_error(self):
        result = self.objects.create_objects('non_exist')
        self.assertIsNone(result)

    def test_commit_one_file_returns_correct_tree(self):
        path = os.path.join(self.git_repo_name, 'hello')
        new_sha1 = '0123456789'*4
        tracked_index = {
            path: IndexEntry(path, current_sha1='0'*40, new_sha1=new_sha1)
        }
        self.index.build_tracked_index = MagicMock(return_value=tracked_index)
        root_tree_entry = self.objects.commit_cached_tree_objects()

        tree_content = '{},{},{},{}\n'.format('hello', '10000644', EntryType.BLOB, new_sha1)
        expected_tree_sha = hashlib.sha1(tree_content.encode()).hexdigest()
        expected_root_tree_entry = TreeEntry(self.git_repo_name, entry_type=EntryType.TREE, sha1=expected_tree_sha)
        self.assertEqual(str(root_tree_entry), str(expected_root_tree_entry), 'Commit cached tree object for one file failed with incorrect tree entry returned')

    def test_commit_one_dir_and_one_file_returns_correct_tree(self):
        path = os.path.join(self.git_repo_name, 'hellodir/hello')
        hello_sha1 = '0123456789'*4
        tracked_index = {
            path: IndexEntry(path, current_sha1='0'*40, new_sha1=hello_sha1)
        }
        self.index.build_tracked_index = MagicMock(return_value=tracked_index)
        root_tree_entry = self.objects.commit_cached_tree_objects()

        tree_content = '{},{},{},{}\n'.format('hello', '10000644', EntryType.BLOB, hello_sha1)
        expected_tree_sha1 = hashlib.sha1(tree_content.encode()).hexdigest()

        tree_content2 = '{},{},{},{}\n'.format('hellodir', '10000644', EntryType.TREE, expected_tree_sha1)
        expected_tree_sha1_hellodir = hashlib.sha1(tree_content2.encode()).hexdigest()

        expected_root_tree_entry = TreeEntry(self.git_repo_name, entry_type=EntryType.TREE, sha1=expected_tree_sha1_hellodir)

        self.assertEqual(str(root_tree_entry), str(expected_root_tree_entry), 'Commit cached tree object for one dir and one file failed with incorrect tree entry returned')
